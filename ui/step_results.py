"""
Step 4 — Results Dashboard.
Readiness score, charts, per-skill breakdown.
"""
import streamlit as st
from agents.gap_analyzer import analyze
from utils.charts import radar_chart, gap_bar, claimed_vs_assessed, readiness_gauge
from core import state
from ui.styles import badge
import config


def render():
    st.markdown(
        '<div class="sp-section-title">📊 Your Assessment Results</div>',
        unsafe_allow_html=True,
    )

    results       = state.get("assessment_results")
    jd_parsed     = state.get("jd_parsed")
    resume_parsed = state.get("resume_parsed")
    skill_map     = state.get("skill_map")

    if not results:
        st.error("No results found. Please complete the assessment first.")
        return

    # ── Run gap analysis once ──────────────────────────────────────
    if state.get("gap_analysis") is None:
        with st.spinner("Computing your results..."):
            try:
                gap = analyze(skill_map, results, jd_parsed, resume_parsed)
                state.set("gap_analysis", gap)
            except Exception as e:
                st.error(f"Gap analysis failed: {e}")
                return

    gap = state.get("gap_analysis")

    # ── Hero: Readiness Score ──────────────────────────────────────
    score = gap["readiness_score"]
    pct   = round(score * 100)
    color = "#10B981" if score >= 0.70 else "#F59E0B" if score >= 0.50 else "#EF4444"
    weeks = gap["hire_ready_weeks"]

    st.markdown(
        f'<div class="sp-card-highlight" style="text-align:center;padding:2rem">'
        f'<div style="color:#64748B;font-size:0.8rem;text-transform:uppercase;'
        f'letter-spacing:1.5px;font-weight:600">Overall Job Readiness</div>'
        f'<div class="sp-readiness-label" style="color:{color}">{pct}%</div>'
        f'<div class="sp-readiness-sub">'
        f'Estimated time to hire-ready: <strong style="color:{color}">'
        f'{weeks} week{"s" if weeks != 1 else ""}</strong></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── 4 key metrics ──────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        (len(gap["strengths"]),     "#10B981", "Strengths"),
        (len(gap["critical_gaps"]), "#EF4444", "Critical Gaps"),
        (len(gap["quick_wins"]),    "#F59E0B", "Quick Wins"),
        (len(results),              "#6366F1", "Skills Tested"),
    ]
    for col, (val, clr, lbl) in zip([c1, c2, c3, c4], metrics):
        with col:
            st.markdown(
                f'<div class="sp-metric">'
                f'<div class="sp-metric-value" style="color:{clr}">{val}</div>'
                f'<div class="sp-metric-label">{lbl}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown('<div class="sp-divider"></div>', unsafe_allow_html=True)

    # ── Overall observation ────────────────────────────────────────
    st.markdown(
        f'<div class="sp-card">'
        f'<div style="color:#6366F1;font-size:0.75rem;font-weight:700;'
        f'text-transform:uppercase;letter-spacing:1px;margin-bottom:0.6rem">'
        f'Assessment Summary</div>'
        f'<div style="color:#E2E8F0;line-height:1.7">'
        f'{gap.get("overall_observation","")}</div>'
        f'<div style="color:#64748B;font-size:0.82rem;margin-top:0.8rem">'
        f'Claim accuracy: {gap.get("claim_accuracy_summary","")}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sp-divider"></div>', unsafe_allow_html=True)

    # ── Charts ─────────────────────────────────────────────────────
    skills_list  = [r["skill"]               for r in results]
    req_list     = [r["required_proficiency"] for r in results]
    claimed_list = [r["claimed_proficiency"]  for r in results]
    assessed_list= [r["assessed_proficiency"] for r in results]
    gap_list     = [r["required_proficiency"] - r["assessed_proficiency"] for r in results]

    # Gauge + Radar side by side
    cg, cr = st.columns([1, 2])
    with cg:
        st.plotly_chart(readiness_gauge(score), use_container_width=True)
    with cr:
        if len(skills_list) >= 3:
            st.plotly_chart(
                radar_chart(skills_list, req_list, claimed_list, assessed_list),
                use_container_width=True,
            )
        else:
            st.info("Need 3+ skills for radar chart.")

    # Gap + Claim accuracy
    cb1, cb2 = st.columns(2)
    with cb1:
        st.plotly_chart(gap_bar(skills_list, gap_list), use_container_width=True)
    with cb2:
        st.plotly_chart(
            claimed_vs_assessed(skills_list, claimed_list, assessed_list),
            use_container_width=True,
        )

    st.markdown('<div class="sp-divider"></div>', unsafe_allow_html=True)

    # ── Skill Breakdown ────────────────────────────────────────────
    st.markdown(
        '<div class="sp-section-title">🔬 Skill-by-Skill Breakdown</div>',
        unsafe_allow_html=True,
    )

    for s in gap.get("skill_breakdown", []):
        gap_val  = s.get("gap", 0)
        assessed = s.get("assessed", 0)
        clr      = (
            "#10B981" if gap_val <= 0.10 else
            "#F59E0B" if gap_val <= 0.25 else
            "#EF4444"
        )
        label    = config.get_proficiency_label(assessed)

        with st.expander(
            f"{s['skill']}  —  {assessed:.0%} assessed  •  {gap_val:.0%} gap  •  {s['claim_accuracy']}"
        ):
            ca, cb, cc, cd = st.columns(4)
            for col, val, lbl, c in zip(
                [ca, cb, cc, cd],
                [s["required"], s["claimed"], s["assessed"], s.get("confidence", 0)],
                ["Required", "Claimed", "Assessed", "Confidence"],
                [config.COLOR_REQUIRED, config.COLOR_CLAIMED, config.COLOR_ASSESSED, "#6366F1"],
            ):
                with col:
                    st.markdown(
                        f'<div class="sp-metric">'
                        f'<div class="sp-metric-value" style="color:{c};font-size:1.4rem">'
                        f'{val:.0%}</div>'
                        f'<div class="sp-metric-label">{lbl}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

            st.markdown(
                f'<div style="margin-top:0.8rem">'
                f'<span style="color:#64748B;font-size:0.8rem">Importance: </span>'
                f'{badge(s["importance"].replace("_"," "), kind=s["importance"])}'
                f'<span style="color:#64748B;font-size:0.8rem;margin-left:1rem">'
                f'Questions asked: {s.get("questions_asked",0)} &nbsp;|&nbsp; '
                f'Max difficulty: Level {s.get("max_difficulty",0)}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

            if s.get("observation"):
                st.markdown(
                    f'<div style="color:#94A3B8;font-size:0.88rem;'
                    f'margin-top:0.7rem;font-style:italic">'
                    f'"{s["observation"]}"</div>',
                    unsafe_allow_html=True,
                )

    st.markdown('<div class="sp-divider"></div>', unsafe_allow_html=True)

    # ── Strengths / Gaps / Quick Wins ──────────────────────────────
    cs, cg2, cq = st.columns(3)

    with cs:
        st.markdown(
            '<div style="color:#10B981;font-weight:700;margin-bottom:0.5rem">'
            '💪 Strengths</div>',
            unsafe_allow_html=True,
        )
        for s in gap.get("strengths", []):
            st.markdown(
                f'<div style="color:#E2E8F0;padding:0.3rem 0;'
                f'border-bottom:1px solid #1E1E35;font-size:0.88rem">✅ {s}</div>',
                unsafe_allow_html=True,
            )
        if not gap.get("strengths"):
            st.markdown('<div style="color:#64748B;font-size:0.85rem">None identified</div>', unsafe_allow_html=True)

    with cg2:
        st.markdown(
            '<div style="color:#EF4444;font-weight:700;margin-bottom:0.5rem">'
            '⚠️ Critical Gaps</div>',
            unsafe_allow_html=True,
        )
        for s in gap.get("critical_gaps", []):
            st.markdown(
                f'<div style="color:#E2E8F0;padding:0.3rem 0;'
                f'border-bottom:1px solid #1E1E35;font-size:0.88rem">🔴 {s}</div>',
                unsafe_allow_html=True,
            )
        if not gap.get("critical_gaps"):
            st.markdown('<div style="color:#64748B;font-size:0.85rem">None</div>', unsafe_allow_html=True)

    with cq:
        st.markdown(
            '<div style="color:#F59E0B;font-weight:700;margin-bottom:0.5rem">'
            '⚡ Quick Wins</div>',
            unsafe_allow_html=True,
        )
        for s in gap.get("quick_wins", []):
            st.markdown(
                f'<div style="color:#E2E8F0;padding:0.3rem 0;'
                f'border-bottom:1px solid #1E1E35;font-size:0.88rem">🟡 {s}</div>',
                unsafe_allow_html=True,
            )
        if not gap.get("quick_wins"):
            st.markdown('<div style="color:#64748B;font-size:0.85rem">None</div>', unsafe_allow_html=True)

    st.markdown('<div class="sp-divider"></div>', unsafe_allow_html=True)

    if st.button(
        "Build My Learning Plan →", type="primary", use_container_width=True
    ):
        state.go_to_step(5)
        st.rerun()