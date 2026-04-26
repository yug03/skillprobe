"""
Step 1 — Input
Premium candidate intake screen for SkillProbe.
"""
import streamlit as st
from utils.file_parser import extract_text
from core import state
import config


def render():
    # ── Hero ───────────────────────────────────────────────────────────────────
    st.markdown(
        '<div style="padding:1.1rem 0 0.8rem 0;text-align:center">'
        '<div style="display:inline-flex;align-items:center;gap:10px;background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.2);border-radius:999px;padding:6px 16px;margin-bottom:1rem">'
        '<span style="width:8px;height:8px;border-radius:50%;background:#10B981;display:inline-block;box-shadow:0 0 12px rgba(16,185,129,0.7)"></span>'
        '<span style="font-size:0.72rem;font-weight:800;letter-spacing:0.12em;text-transform:uppercase;color:#A5B4FC">Adaptive skill verification agent</span>'
        '</div>'
        '<div style="font-size:3.1rem;font-weight:900;line-height:1.02;letter-spacing:-2px;background:linear-gradient(135deg,#6366F1 0%,#8B5CF6 55%,#06B6D4 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:0.7rem">Know where you stand.<br>Know how to close the gap.</div>'
        '<div style="max-width:760px;margin:0 auto;color:#64748B;font-size:1rem;line-height:1.7">Paste a job description and your resume. SkillProbe verifies your skills through an adaptive assessment and turns the result into an evidence-based learning roadmap.</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Feature pills ──────────────────────────────────────────────────────────
    p1, p2, p3, p4 = st.columns(4)
    pills = [
        ("🧠", "Adaptive questions"),
        ("📊", "Explainable scoring"),
        ("🗺️", "Phased learning plan"),
        ("📄", "PDF report"),
    ]
    for col, (icon, label) in zip([p1, p2, p3, p4], pills):
        with col:
            st.markdown(
                f'<div style="background:#0F0F18;border:1px solid #1A1A2E;border-radius:999px;padding:0.65rem 0.9rem;text-align:center">'
                f'<span style="font-size:0.85rem">{icon}</span> '
                f'<span style="font-size:0.8rem;color:#94A3B8;font-weight:600">{label}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown('<div style="height:1.2rem"></div>', unsafe_allow_html=True)

    # ── Sample loader ──────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns([3, 2, 3])
    with c2:
        if st.button("📥 Load Sample Inputs", key="load_sample_inputs", use_container_width=True):
            try:
                with open("sample_inputs/sample_jd.txt", "r", encoding="utf-8") as f:
                    st.session_state["jd_textarea"] = f.read()
                with open("sample_inputs/sample_resume.txt", "r", encoding="utf-8") as f:
                    st.session_state["cv_textarea"] = f.read()
                st.rerun()
            except FileNotFoundError:
                st.error("Sample files not found. Check sample_inputs/ folder exists.")

    st.markdown(
        '<div style="text-align:center;color:#475569;font-size:0.76rem;margin:0.5rem 0 1.4rem 0">Use demo data for a quick walkthrough, or paste your own inputs below.</div>',
        unsafe_allow_html=True,
    )

    # ── Input panels ───────────────────────────────────────────────────────────
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown(
            '<div style="background:#12121E;border:1px solid #1A1A2E;border-radius:16px;padding:1.2rem 1.2rem 1rem 1.2rem;margin-bottom:0.8rem">'
            '<div style="display:flex;align-items:center;gap:10px;margin-bottom:0.2rem">'
            '<div style="width:34px;height:34px;border-radius:10px;background:rgba(99,102,241,0.14);display:flex;align-items:center;justify-content:center">📋</div>'
            '<div><div style="font-size:1.05rem;font-weight:800;color:#E2E8F0">Job Description</div><div style="font-size:0.75rem;color:#64748B">Paste the target role requirements</div></div>'
            '</div>'
            '<div style="margin-top:0.9rem"></div>',
            unsafe_allow_html=True,
        )

        jd_file = st.file_uploader(
            "Upload JD file",
            type=["pdf", "docx", "txt"],
            key="jd_upload",
            help="Upload PDF, DOCX, or TXT",
        )

        jd_text = st.text_area(
            "Job Description",
            key="jd_textarea",
            label_visibility="collapsed",
            height=300,
            placeholder="Paste the full job description here...\n\nInclude the role title, required skills, responsibilities, experience requirements, and preferred tools.",
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown(
            '<div style="background:#12121E;border:1px solid #1A1A2E;border-radius:16px;padding:1.2rem 1.2rem 1rem 1.2rem;margin-bottom:0.8rem">'
            '<div style="display:flex;align-items:center;gap:10px;margin-bottom:0.2rem">'
            '<div style="width:34px;height:34px;border-radius:10px;background:rgba(16,185,129,0.14);display:flex;align-items:center;justify-content:center">👤</div>'
            '<div><div style="font-size:1.05rem;font-weight:800;color:#E2E8F0">Your Resume</div><div style="font-size:0.75rem;color:#64748B">Paste your experience and claimed skills</div></div>'
            '</div>'
            '<div style="margin-top:0.9rem"></div>',
            unsafe_allow_html=True,
        )

        cv_file = st.file_uploader(
            "Upload Resume file",
            type=["pdf", "docx", "txt"],
            key="cv_upload",
            help="Upload PDF, DOCX, or TXT",
        )

        cv_text = st.text_area(
            "Resume",
            key="cv_textarea",
            label_visibility="collapsed",
            height=300,
            placeholder="Paste your resume here...\n\nInclude your summary, skills, experience, projects, and education.",
        )

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Resolve final values ───────────────────────────────────────────────────
    final_jd = ""
    final_cv = ""

    if jd_file:
        try:
            final_jd = extract_text(jd_file)
        except Exception as e:
            st.error(f"Could not read JD file: {e}")
            final_jd = st.session_state.get("jd_textarea", "")
    else:
        final_jd = st.session_state.get("jd_textarea", "")

    if cv_file:
        try:
            final_cv = extract_text(cv_file)
        except Exception as e:
            st.error(f"Could not read resume file: {e}")
            final_cv = st.session_state.get("cv_textarea", "")
    else:
        final_cv = st.session_state.get("cv_textarea", "")

    jd_ok = len(final_jd.strip()) > 50
    cv_ok = len(final_cv.strip()) > 50
    api_ok = bool(config.GEMINI_API_KEY or config.GROQ_API_KEY)
    all_ok = jd_ok and cv_ok and api_ok

    # ── Readiness status ───────────────────────────────────────────────────────
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(
            f'<div style="background:#0F0F18;border:1px solid {"rgba(16,185,129,0.25)" if jd_ok else "#1A1A2E"};border-radius:12px;padding:0.9rem 1rem;text-align:center">'
            f'<div style="font-size:0.75rem;color:{"#6EE7B7" if jd_ok else "#64748B"};font-weight:700">{("✅ Ready" if jd_ok else "○ Waiting")}</div>'
            f'<div style="font-size:0.72rem;color:#475569;margin-top:0.2rem">Job description</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with s2:
        st.markdown(
            f'<div style="background:#0F0F18;border:1px solid {"rgba(16,185,129,0.25)" if cv_ok else "#1A1A2E"};border-radius:12px;padding:0.9rem 1rem;text-align:center">'
            f'<div style="font-size:0.75rem;color:{"#6EE7B7" if cv_ok else "#64748B"};font-weight:700">{("✅ Ready" if cv_ok else "○ Waiting")}</div>'
            f'<div style="font-size:0.72rem;color:#475569;margin-top:0.2rem">Resume</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with s3:
        st.markdown(
            f'<div style="background:#0F0F18;border:1px solid {"rgba(16,185,129,0.25)" if api_ok else "rgba(239,68,68,0.25)"};border-radius:12px;padding:0.9rem 1rem;text-align:center">'
            f'<div style="font-size:0.75rem;color:{"#6EE7B7" if api_ok else "#FCA5A5"};font-weight:700">{("✅ Connected" if api_ok else "⚠ Missing")}</div>'
            f'<div style="font-size:0.72rem;color:#475569;margin-top:0.2rem">API configuration</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

    # ── CTA ────────────────────────────────────────────────────────────────────
    cta_l, cta_m, cta_r = st.columns([3, 4, 3])
    with cta_m:
        if st.button(
            "Analyze My Readiness →",
            key="analyze_readiness",
            type="primary",
            use_container_width=True,
            disabled=not all_ok,
        ):
            state.set("jd_text", final_jd)
            state.set("resume_text", final_cv)
            state.go_to_step(2)
            st.rerun()

    if not api_ok:
        st.markdown(
            '<div style="text-align:center;color:#F87171;font-size:0.78rem;margin-top:0.7rem">No API key found. Add GEMINI_API_KEY or GROQ_API_KEY to your environment configuration.</div>',
            unsafe_allow_html=True,
        )
    elif not all_ok:
        st.markdown(
            '<div style="text-align:center;color:#475569;font-size:0.78rem;margin-top:0.7rem">Paste enough content in both inputs to begin the assessment.</div>',
            unsafe_allow_html=True,
        )
        
