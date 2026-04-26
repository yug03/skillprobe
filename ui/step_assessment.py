"""
Step 3 — Adaptive Assessment.
Focus mode. One question at a time. No chat bubbles.
"""
import time
import streamlit as st
from core import state
from ui.styles import diff_pill
import config


def render():
    engine = state.get("assessment_engine")
    if engine is None:
        st.error("Engine not found. Please go back to Step 2.")
        return

    # ── Check completion ───────────────────────────────────────────
    if engine.done:
        state.set("assessment_results", engine.get_results())
        state.set("assessment_complete", True)
        state.go_to_step(4)
        st.rerun()
        return

    skill = engine.current_skill()
    est   = engine.current_state()

    if skill is None or est is None:
        state.set("assessment_results", engine.get_results())
        state.go_to_step(4)
        st.rerun()
        return

    # ── Progress ───────────────────────────────────────────────────
    total   = len(engine.queue)
    current = engine.index + 1
    pct     = current / total

    st.markdown(
        f'<div style="display:flex;justify-content:space-between;'
        f'align-items:center;margin-bottom:0.5rem">'
        f'<span style="color:#6366F1;font-weight:700;font-size:0.85rem">'
        f'SKILL {current} OF {total}</span>'
        f'<span style="color:#64748B;font-size:0.8rem">'
        f'Question {len(est.history) + 1} of {config.MAX_QUESTIONS} max</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.progress(pct)

    # ── Skill + difficulty header ──────────────────────────────────
    diff_label = config.DIFFICULTY_LEVELS.get(est.difficulty, "")
    st.markdown(
        f'<div style="margin:1.2rem 0 0.5rem 0">'
        f'<span style="color:#E2E8F0;font-size:1.1rem;font-weight:700">'
        f'{skill}</span>'
        f'{diff_pill(est.difficulty, diff_label)}'
        f'<span style="color:#64748B;font-size:0.78rem;margin-left:0.8rem">'
        f'Confidence: {est.confidence:.0%}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sp-divider"></div>', unsafe_allow_html=True)

    # ── Previous answers for this skill ───────────────────────────
    if est.history:
        with st.expander(
            f"Previous answers this skill ({len(est.history)})",
            expanded=False
        ):
            for i, h in enumerate(est.history, 1):
                quality = h.get("quality", "weak")
                color   = {
                    "strong":    "#10B981",
                    "moderate":  "#F59E0B",
                    "weak":      "#EF4444",
                    "no_answer": "#64748B",
                }.get(quality, "#64748B")
                st.markdown(
                    f'<div style="padding:0.6rem 0;'
                    f'border-bottom:1px solid #1E1E35">'
                    f'<span style="color:#94A3B8;font-size:0.8rem">'
                    f'Q{i} (Level {h["difficulty"]}): </span>'
                    f'<span style="color:#E2E8F0;font-size:0.85rem">'
                    f'{h["question"][:100]}...</span><br>'
                    f'<span style="color:{color};font-size:0.8rem;font-weight:600">'
                    f'{quality.title()} • {h["score"]:.0%}</span>'
                    f'<span style="color:#64748B;font-size:0.78rem">'
                    f' — {h["reasoning"][:120]}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    # ── Generate question if needed ────────────────────────────────
    if state.get("current_question") is None:
        with st.spinner(f"Preparing question for {skill}..."):
            try:
                q = engine.generate_question()
                if q is None:
                    state.set("assessment_results", engine.get_results())
                    state.go_to_step(4)
                    st.rerun()
                    return
                state.set("current_question", q)
            except Exception as e:
                st.error(f"Failed to generate question: {e}")
                return

    q = state.get("current_question")

    # ── Question display ───────────────────────────────────────────
    st.markdown(
        f'<div class="sp-question-box">'
        f'<div class="sp-skill-label">'
        f'{q["skill"]} &nbsp;•&nbsp; '
        f'{q["difficulty_label"]} &nbsp;•&nbsp; '
        f'Question {q["question_number"]}'
        f'</div>'
        f'<div class="sp-question-text">{q["question"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Answer input ───────────────────────────────────────────────
    answer_key = (
        f"ans_{q['skill']}_{q['question_number']}_{len(est.history)}"
    )

    answer = st.text_area(
        "Your answer",
        height=160,
        placeholder=(
            "Type your answer here. "
            "Be as specific as you can — depth matters."
        ),
        key=answer_key,
        label_visibility="collapsed",
    )

    col_sub, col_skip, col_end = st.columns([3, 1, 1])
    with col_sub:
        submitted = st.button(
            "Submit Answer →",
            type="primary",
            use_container_width=True,
        )
    with col_skip:
        skipped = st.button("Skip ⏭", use_container_width=True)
    with col_end:
        ended = st.button("End 🏁", use_container_width=True)

    # ── End early ──────────────────────────────────────────────────
    if ended:
        state.set("assessment_results", engine.get_results())
        state.go_to_step(4)
        st.rerun()
        return

    # ── Handle submit / skip ───────────────────────────────────────
    if submitted or skipped:
        final_answer = "skip" if skipped else answer

        if not skipped and not final_answer.strip():
            st.warning("Please type an answer or click Skip.")
            return

        with st.spinner("Evaluating..."):
            try:
                result = engine.submit_answer(
                    question   = q["question"],
                    answer     = final_answer,
                    difficulty = q["difficulty"],
                )

                ev      = result.get("evaluation", {})
                quality = ev.get("quality", "weak")
                color   = {
                    "strong":    "#10B981",
                    "moderate":  "#F59E0B",
                    "weak":      "#EF4444",
                    "no_answer": "#64748B",
                }.get(quality, "#64748B")

                # Show instant feedback
                st.markdown(
                    f'<div class="sp-card" '
                    f'style="border-color:{color};margin-top:1rem">'
                    f'<span style="color:{color};font-weight:700;'
                    f'font-size:0.95rem">{quality.upper()}</span>'
                    f'<span style="color:#E2E8F0;font-size:0.88rem">'
                    f' — {ev.get("reasoning", "")}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                # Log the exchange
                log = state.get("conversation_log") or []
                log.append({
                    "skill":            q["skill"],
                    "question":         q["question"],
                    "answer":           final_answer,
                    "difficulty":       q["difficulty"],
                    "difficulty_label": q["difficulty_label"],
                    "evaluation":       ev,
                })
                state.set("conversation_log", log)

                # Skill complete notification
                if result.get("skill_done"):
                    ss = result.get("skill_summary", {})
                    assessed = ss.get("assessed_proficiency", 0)
                    obs      = ss.get("observation", "")
                    st.success(
                        f"✅ {q['skill']} assessed — "
                        f"{assessed:.0%} proficiency | {obs}"
                    )
                    time.sleep(1.5)

                # Clear pending question
                state.set("current_question", None)

                # Navigate if done
                if result.get("assessment_done"):
                    state.set("assessment_results", engine.get_results())
                    state.go_to_step(4)

                st.rerun()

            except Exception as e:
                st.error(f"Evaluation error: {e}")
                import traceback
                st.code(traceback.format_exc())