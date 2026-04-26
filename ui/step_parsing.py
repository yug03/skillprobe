"""
Step 2 — Parsing & Skill Mapping.
Shows what was found, builds the assessment queue.
"""
import streamlit as st
from agents.parser_agent import parse_all
from agents.assessment_engine import AssessmentEngine
from core import state
from ui.styles import badge


def render():
    st.markdown('<div class="sp-section-title">🔍 Parsing Your Documents</div>', unsafe_allow_html=True)

    # ── Run parsing only once ──────────────────────────────────────
    if not state.get("parsing_done"):
                with st.status("Analysing documents...", expanded=True) as status:
            try:
                st.write("📋 Reading job description and resume...")
                jd_parsed, resume_parsed, skill_map = parse_all(
                    state.get("jd_text"),
                    state.get("resume_text"),
                )
                state.set("jd_parsed",     jd_parsed)
                state.set("resume_parsed", resume_parsed)
                state.set("skill_map",     skill_map)
                state.set("parsing_done",  True)
                status.update(label="✅ Analysis complete!", state="complete")
            except Exception as e:
                status.update(label="❌ Parsing failed", state="error")
                st.error(f"Error during parsing: {e}")
                if st.button("← Go Back"):
                    state.go_to_step(1)
                    st.rerun()
                return

    jd_parsed     = state.get("jd_parsed")
    resume_parsed = state.get("resume_parsed")
    skill_map     = state.get("skill_map")

    # ── JD summary ─────────────────────────────────────────────────
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(f"""
<div class="sp-card">
  <div style="color:#6366F1; font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:1px">Target Role</div>
  <div style="color:#E2E8F0; font-size:1.3rem; font-weight:700; margin:0.4rem 0">{jd_parsed.get('title','')}</div>
  <div style="color:#94A3B8; font-size:0.85rem">{jd_parsed.get('role_summary','')}</div>
  <div style="margin-top:0.8rem; color:#64748B; font-size:0.8rem">Experience required: {jd_parsed.get('experience_years','N/A')} years</div>
</div>
""", unsafe_allow_html=True)

        st.markdown("**Required Skills:**")
        for s in jd_parsed.get("required_skills", []):
            imp  = s.get("importance", "important")
            prof = s.get("required_proficiency", 0.5)
            st.markdown(
                badge(f"{s['skill']} • {prof:.0%}", kind=imp),
                unsafe_allow_html=True,
            )

    with col2:
        st.markdown(f"""
<div class="sp-card">
  <div style="color:#10B981; font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:1px">Candidate</div>
  <div style="color:#E2E8F0; font-size:1.3rem; font-weight:700; margin:0.4rem 0">{resume_parsed.get('name','')}</div>
  <div style="color:#94A3B8; font-size:0.85rem">{resume_parsed.get('summary','')}</div>
  <div style="margin-top:0.8rem; color:#64748B; font-size:0.8rem">Experience: {resume_parsed.get('experience_years','N/A')} years | {resume_parsed.get('education','')}</div>
</div>
""", unsafe_allow_html=True)

        st.markdown("**Claimed Skills:**")
        for s in resume_parsed.get("skills", [])[:14]:
            prof = s.get("claimed_proficiency", 0)
            st.markdown(
                badge(f"{s['skill']} • {prof:.0%}", kind="skill"),
                unsafe_allow_html=True,
            )

    st.markdown('<div class="sp-divider"></div>', unsafe_allow_html=True)

    # ── Skill Map summary ──────────────────────────────────────────
    matched = skill_map.get("matched_skills", [])
    missing = skill_map.get("missing_skills", [])
    extra   = skill_map.get("extra_skills",   [])
    queue   = skill_map.get("assessment_queue", [])

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
<div class="sp-metric">
  <div class="sp-metric-value" style="color:#10B981">{len(matched)}</div>
  <div class="sp-metric-label">Skills Matched</div>
</div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
<div class="sp-metric">
  <div class="sp-metric-value" style="color:#EF4444">{len(missing)}</div>
  <div class="sp-metric-label">Skills Missing</div>
</div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
<div class="sp-metric">
  <div class="sp-metric-value" style="color:#6366F1">{len(queue)}</div>
  <div class="sp-metric-label">Skills to Assess</div>
</div>""", unsafe_allow_html=True)

    st.markdown('<div class="sp-divider"></div>', unsafe_allow_html=True)

    # ── Assessment queue ───────────────────────────────────────────
    st.markdown('<div class="sp-section-title">🎯 Assessment Queue</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="color:#64748B; font-size:0.88rem; margin-bottom:1rem">'
        'The agent will assess you on these skills in this order. '
        'Critical skills first.</div>',
        unsafe_allow_html=True,
    )

    all_matched = {s["skill"]: s for s in matched}
    for i, skill in enumerate(queue, 1):
        s   = all_matched.get(skill, {})
        imp = s.get("importance", "important")
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:0.8rem;padding:0.5rem 0;border-bottom:1px solid #1E1E35">'
            f'<span style="color:#6366F1;font-weight:700;width:20px">{i}</span>'
            f'{badge(skill, kind=imp)}'
            f'<span style="color:#64748B;font-size:0.8rem;margin-left:auto">{imp.replace("_"," ")}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="sp-divider"></div>', unsafe_allow_html=True)

    if st.button("Start Assessment →", type="primary", use_container_width=True):
        engine = AssessmentEngine(
            skill_map     = skill_map,
            jd_parsed     = jd_parsed,
            resume_parsed = resume_parsed,
        )
        state.set("assessment_engine",  engine)
        state.set("conversation_log",   [])
        state.set("current_question",   None)
        state.go_to_step(3)
        st.rerun()
