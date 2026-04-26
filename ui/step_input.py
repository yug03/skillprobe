"""
Step 1 — Input page.
Clean, focused, minimal. User pastes JD + resume, clicks go.
"""
import streamlit as st
from utils.file_parser import extract_text
from core import state
import config


def render():
    # ── Hero ──────────────────────────────────────────────────────
    st.markdown('<div class="sp-hero-title">SkillProbe</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sp-tagline">Know where you stand. Know exactly how to get there.</div>',
        unsafe_allow_html=True,
    )

    # ── How it works ───────────────────────────────────────────────
    st.markdown("""
<div class="sp-card">
<div style="display:grid;grid-template-columns:1fr 24px 1fr 24px 1fr;
gap:0.5rem;text-align:center;align-items:center">
  <div>
    <div style="font-size:1.6rem">📄</div>
    <div style="color:#A5B4FC;font-size:0.72rem;font-weight:700;
    margin-top:0.3rem;text-transform:uppercase;letter-spacing:1px">Upload</div>
    <div style="color:#64748B;font-size:0.7rem">JD + Resume</div>
  </div>
  <div style="color:#1E1E35;font-size:1.1rem">→</div>
  <div>
    <div style="font-size:1.6rem">🎯</div>
    <div style="color:#A5B4FC;font-size:0.72rem;font-weight:700;
    margin-top:0.3rem;text-transform:uppercase;letter-spacing:1px">Assess</div>
    <div style="color:#64748B;font-size:0.7rem">Adaptive test</div>
  </div>
  <div style="color:#1E1E35;font-size:1.1rem">→</div>
  <div>
    <div style="font-size:1.6rem">📚</div>
    <div style="color:#A5B4FC;font-size:0.72rem;font-weight:700;
    margin-top:0.3rem;text-transform:uppercase;letter-spacing:1px">Plan</div>
    <div style="color:#64748B;font-size:0.7rem">Your roadmap</div>
  </div>
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="sp-divider"></div>', unsafe_allow_html=True)

    # ── Sample loader ──────────────────────────────────────────────
    # KEY FIX: set the widget keys directly so text areas update
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        if st.button("📥 Load Sample Inputs (Demo)", use_container_width=True):
            try:
                with open("sample_inputs/sample_jd.txt", "r", encoding="utf-8") as f:
                    st.session_state["jd_textarea"] = f.read()
                with open("sample_inputs/sample_resume.txt", "r", encoding="utf-8") as f:
                    st.session_state["cv_textarea"] = f.read()
                st.rerun()
            except FileNotFoundError:
                st.error("Sample files not found. Check sample_inputs/ folder exists.")

    # ── Input columns ──────────────────────────────────────────────
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            '<div class="sp-section-title">📋 Job Description</div>',
            unsafe_allow_html=True,
        )
        jd_file = st.file_uploader(
            "Upload JD",
            type=["pdf", "docx", "txt"],
            key="jd_upload",
            label_visibility="collapsed",
        )
        jd_text = st.text_area(
            "Paste job description",
            height=320,
            placeholder="Paste the full job description here...",
            key="jd_textarea",
            label_visibility="collapsed",
        )

    with col2:
        st.markdown(
            '<div class="sp-section-title">📄 Your Resume</div>',
            unsafe_allow_html=True,
        )
        cv_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "docx", "txt"],
            key="cv_upload",
            label_visibility="collapsed",
        )
        cv_text = st.text_area(
            "Paste resume",
            height=320,
            placeholder="Paste your resume here...",
            key="cv_textarea",
            label_visibility="collapsed",
        )

    # ── Resolve final text ─────────────────────────────────────────
    final_jd = ""
    final_cv = ""

    if jd_file:
        try:
            final_jd = extract_text(jd_file)
            st.success(f"✅ JD loaded from file ({len(final_jd):,} chars)")
        except Exception as e:
            st.error(f"Could not read JD file: {e}")
    else:
        final_jd = st.session_state.get("jd_textarea", "")

    if cv_file:
        try:
            final_cv = extract_text(cv_file)
            st.success(f"✅ Resume loaded from file ({len(final_cv):,} chars)")
        except Exception as e:
            st.error(f"Could not read resume file: {e}")
    else:
        final_cv = st.session_state.get("cv_textarea", "")

    # ── Show character counts if loaded ───────────────────────────
    if final_jd and not jd_file:
        st.caption(f"JD: {len(final_jd):,} characters")
    if final_cv and not cv_file:
        st.caption(f"Resume: {len(final_cv):,} characters")

    st.markdown('<div class="sp-divider"></div>', unsafe_allow_html=True)

    # ── CTA ────────────────────────────────────────────────────────
    if st.button(
        "Analyze My Readiness →",
        type="primary",
        use_container_width=True,
    ):
        errors = []
        if not final_jd.strip():
            errors.append("Please provide a Job Description.")
        if not final_cv.strip():
            errors.append("Please provide your Resume.")
        if not config.GEMINI_API_KEY and not config.GROQ_API_KEY:
            errors.append(
                "No API key found. Add GEMINI_API_KEY to your .env file."
            )

        if errors:
            for e in errors:
                st.error(e)
        else:
            state.set("jd_text",     final_jd)
            state.set("resume_text", final_cv)
            state.go_to_step(2)
            st.rerun()