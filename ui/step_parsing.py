"""
Step 2 — Parsing & Skill Mapping.
Shows what was found and builds the assessment queue.
"""
import streamlit as st
from agents.parser_agent import parse_jd, parse_resume
from agents.skill_mapper import map_skills
from agents.assessment_engine import AssessmentEngine
from core import state
from ui import styles


def _skill_name(item):
    if isinstance(item, dict):
        return item.get("skill", "Unknown")
    return str(item)


def _importance_of(item):
    if isinstance(item, dict):
        return str(item.get("importance", "important")).lower()
    return "important"


def _required_prof(item):
    if isinstance(item, dict):
        val = item.get("required_proficiency", item.get("required", None))
        if isinstance(val, (int, float)):
            return f"{val:.0%}" if val <= 1 else str(val)
    return None


def _claimed_prof(item):
    if isinstance(item, dict):
        val = item.get("claimed_proficiency", item.get("claimed", None))
        if isinstance(val, (int, float)):
            return f"{val:.0%}" if val <= 1 else str(val)
    return None


def _importance_kind(value):
    value = str(value).lower()
    if "critical" in value:
        return "critical"
    if "important" in value:
        return "important"
    return "nice_to_have"


def render():
    st.markdown(styles.section_title("🔍", "Parsing & Skill Mapping"), unsafe_allow_html=True)

    jd_text = state.get("jd_text") or ""
    resume_text = state.get("resume_text") or ""

    if not jd_text.strip() or not resume_text.strip():
        st.error("Missing Job Description or Resume. Please go back and provide both.")
        if st.button("← Back to Input", use_container_width=True):
            state.go_to_step(1)
            st.rerun()
        return

    # ── Run parsing only once ─────────────────────────────────────────────────
    if not state.get("parsing_done"):
        with st.status("Analysing documents...", expanded=True) as status:
            try:
                st.write("📋 Parsing job description...")
                jd_parsed = parse_jd(jd_text)

                st.write("📄 Parsing resume...")
                resume_parsed = parse_resume(resume_text)

                st.write("🧩 Mapping required vs claimed skills...")
                skill_map = map_skills(jd_parsed, resume_parsed)

                state.set("jd_parsed", jd_parsed)
                state.set("resume_parsed", resume_parsed)
                state.set("skill_map", skill_map)
                state.set("parsing_done", True)

                status.update(label="✅ Analysis complete!", state="complete")
            except Exception as e:
                status.update(label="❌ Parsing failed", state="error")
                st.error(f"Error during parsing: {e}")
                if st.button("← Go Back", use_container_width=True):
                    state.go_to_step(1)
                    st.rerun()
                return

        st.rerun()

    jd_parsed = state.get("jd_parsed") or {}
    resume_parsed = state.get("resume_parsed") or {}
    skill_map = state.get("skill_map") or {}

    required_skills = jd_parsed.get("required_skills", [])
    claimed_skills = resume_parsed.get("skills", [])
    matched = skill_map.get("matched_skills", [])
    missing = skill_map.get("missing_skills", [])
    extra = skill_map.get("extra_skills", [])
    queue = skill_map.get("assessment_queue", [])

    # ── Top summary card ──────────────────────────────────────────────────────
    st.markdown(
        '<div class="sp-card-highlight">'
        '<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;flex-wrap:wrap">'
        '<div>'
        '<div class="sp-label">Analysis Complete</div>'
        '<div style="font-size:1.28rem;font-weight:800;color:#E2E8F0;margin-bottom:0.35rem">Your profile has been mapped against the target role</div>'
        '<div style="color:#94A3B8;font-size:0.9rem;line-height:1.6;max-width:860px">SkillProbe extracted the target role requirements, identified your claimed skills, and prepared a priority queue for adaptive verification.</div>'
        '</div>'
        '<div style="display:flex;gap:0.5rem;flex-wrap:wrap">'
        f'{styles.badge(f"{len(queue)} queued", "cyan")}'
        f'{styles.badge(f"{len(matched)} matched", "match")}'
        f'{styles.badge(f"{len(missing)} missing", "gap")}'
        '</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Metrics ───────────────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(styles.metric_card(str(len(required_skills)), "Required Skills", color="cyan"), unsafe_allow_html=True)
    with m2:
        st.markdown(styles.metric_card(str(len(claimed_skills)), "Claimed Skills", color="green"), unsafe_allow_html=True)
    with m3:
        st.markdown(styles.metric_card(str(len(matched)), "Skills Matched", color="green"), unsafe_allow_html=True)
    with m4:
        st.markdown(styles.metric_card(str(len(queue)), "Skills To Assess", color="amber"), unsafe_allow_html=True)

    # ── Two-column comparison ─────────────────────────────────────────────────
    col1, col2 = st.columns(2, gap="large")

    with col1:
        title = jd_parsed.get("title") or jd_parsed.get("job_title") or "Target Role"
        role_summary = jd_parsed.get("role_summary") or jd_parsed.get("summary") or "No summary extracted."
        experience = jd_parsed.get("experience_years", "N/A")

        st.markdown(
            f'<div class="sp-card">'
            f'<div class="sp-label">Target Role</div>'
            f'<div style="font-size:1.22rem;font-weight:800;color:#E2E8F0;margin-bottom:0.45rem">{title}</div>'
            f'<div style="color:#94A3B8;font-size:0.88rem;line-height:1.65;margin-bottom:0.9rem">{role_summary}</div>'
            f'<div style="color:#64748B;font-size:0.78rem;margin-bottom:0.8rem">Experience required: {experience}</div>'
            f'<div class="sp-label">Required Skills</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        if required_skills:
            for item in required_skills:
                skill_name = _skill_name(item)
                importance = _importance_kind(_importance_of(item))
                prof = _required_prof(item)
                suffix = f" • {prof}" if prof else ""
                st.markdown(styles.badge(f"{skill_name}{suffix}", importance), unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#64748B;font-size:0.85rem">No required skills extracted.</div>', unsafe_allow_html=True)

    with col2:
        name = resume_parsed.get("name") or "Candidate"
        summary = resume_parsed.get("summary") or "No summary extracted."
        experience = resume_parsed.get("experience_years", "N/A")
        education = resume_parsed.get("education", "")

        st.markdown(
            f'<div class="sp-card">'
            f'<div class="sp-label">Candidate Profile</div>'
            f'<div style="font-size:1.22rem;font-weight:800;color:#E2E8F0;margin-bottom:0.45rem">{name}</div>'
            f'<div style="color:#94A3B8;font-size:0.88rem;line-height:1.65;margin-bottom:0.9rem">{summary}</div>'
            f'<div style="color:#64748B;font-size:0.78rem;margin-bottom:0.2rem">Experience: {experience}</div>'
            f'<div style="color:#64748B;font-size:0.78rem;margin-bottom:0.8rem">Education: {education if education else "N/A"}</div>'
            f'<div class="sp-label">Claimed Skills</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        if claimed_skills:
            for item in claimed_skills[:16]:
                skill_name = _skill_name(item)
                prof = _claimed_prof(item)
                suffix = f" • {prof}" if prof else ""
                st.markdown(styles.badge(f"{skill_name}{suffix}", "skill"), unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#64748B;font-size:0.85rem">No claimed skills extracted.</div>', unsafe_allow_html=True)

    st.markdown(styles.divider(), unsafe_allow_html=True)

    # ── Mapping summary ───────────────────────────────────────────────────────
    b1, b2, b3 = st.columns(3)

    with b1:
        matched_html = "".join([styles.badge(_skill_name(s), "match") for s in matched]) if matched else '<span style="color:#64748B;font-size:0.84rem">No matched skills</span>'
        st.markdown(f'<div class="sp-card-success"><div class="sp-label" style="color:#6EE7B7">Matched Skills</div><div style="margin-top:0.35rem">{matched_html}</div></div>', unsafe_allow_html=True)

    with b2:
        missing_html = "".join([styles.badge(_skill_name(s), "gap") for s in missing]) if missing else '<span style="color:#64748B;font-size:0.84rem">No missing skills</span>'
        st.markdown(f'<div class="sp-card-danger"><div class="sp-label" style="color:#FCA5A5">Missing Skills</div><div style="margin-top:0.35rem">{missing_html}</div></div>', unsafe_allow_html=True)

    with b3:
        extra_html = "".join([styles.badge(_skill_name(s), "skill") for s in extra]) if extra else '<span style="color:#64748B;font-size:0.84rem">No extra skills</span>'
        st.markdown(f'<div class="sp-card-warning"><div class="sp-label" style="color:#FDE68A">Extra Claimed Skills</div><div style="margin-top:0.35rem">{extra_html}</div></div>', unsafe_allow_html=True)

    st.markdown(styles.divider(), unsafe_allow_html=True)

    # ── Assessment queue ──────────────────────────────────────────────────────
    st.markdown(styles.section_title("🎯", "Assessment Queue"), unsafe_allow_html=True)
    st.markdown(
        '<div style="color:#64748B;font-size:0.88rem;margin-bottom:1rem">The adaptive assessment will verify these skills in priority order. Higher-impact role requirements are assessed first.</div>',
        unsafe_allow_html=True,
    )

    if queue:
        matched_lookup = {}
        for item in matched:
            matched_lookup[_skill_name(item)] = item

        for i, skill in enumerate(queue, 1):
            source = matched_lookup.get(skill, {})
            kind = _importance_kind(_importance_of(source))
            importance_text = str(_importance_of(source)).replace("_", " ").title()

            st.markdown(
                f'<div style="display:flex;align-items:center;gap:0.8rem;padding:0.8rem 1rem;border:1px solid #1A1A2E;border-radius:12px;background:#0F0F18;margin-bottom:0.5rem">'
                f'<span style="color:#A5B4FC;font-weight:800;width:24px">{i}</span>'
                f'{styles.badge(skill, kind=kind)}'
                f'<span style="color:#64748B;font-size:0.8rem;margin-left:auto">{importance_text}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown('<div class="sp-card"><div style="color:#64748B">No skills available for assessment.</div></div>', unsafe_allow_html=True)

    st.markdown('<div style="height:0.8rem"></div>', unsafe_allow_html=True)

    # ── CTA ───────────────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns([3, 4, 3])
    with c2:
        if st.button("Start Assessment →", type="primary", use_container_width=True, key="start_assessment"):
            engine = AssessmentEngine(skill_map)
            state.set("assessment_engine", engine)
            state.set("conversation_log", [])
            state.set("current_question", None)
            state.go_to_step(3)
            st.rerun()
