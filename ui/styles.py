"""
Global CSS for SkillProbe.
Dark, focused, aesthetic — not a typical LLM chatbot.
"""

GLOBAL_CSS = """
<style>
/* ── Reset & Base ─────────────────────────────────────── */
* { box-sizing: border-box; }

/* Hide Streamlit chrome */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }

/* Main container */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 900px;
}

/* ── Typography ───────────────────────────────────────── */
.sp-hero-title {
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #06B6D4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    letter-spacing: -1px;
    line-height: 1.1;
    margin-bottom: 0.3rem;
}

.sp-tagline {
    text-align: center;
    color: #64748B;
    font-size: 1.05rem;
    margin-bottom: 2.5rem;
    letter-spacing: 0.3px;
}

.sp-section-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #E2E8F0;
    margin: 1.5rem 0 0.8rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Cards ────────────────────────────────────────────── */
.sp-card {
    background: #12121E;
    border: 1px solid #1E1E35;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.sp-card:hover {
    border-color: #6366F1;
}

.sp-card-highlight {
    background: linear-gradient(135deg, #12121E 0%, #1a1a30 100%);
    border: 1px solid #6366F1;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}

/* ── Metric cards ─────────────────────────────────────── */
.sp-metric {
    background: #12121E;
    border: 1px solid #1E1E35;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}
.sp-metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #6366F1;
    line-height: 1;
}
.sp-metric-label {
    font-size: 0.8rem;
    color: #64748B;
    margin-top: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Skill badges ─────────────────────────────────────── */
.sp-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 2px;
}
.sp-badge-critical {
    background: rgba(239,68,68,0.15);
    color: #F87171;
    border: 1px solid rgba(239,68,68,0.3);
}
.sp-badge-important {
    background: rgba(245,158,11,0.15);
    color: #FCD34D;
    border: 1px solid rgba(245,158,11,0.3);
}
.sp-badge-nice {
    background: rgba(16,185,129,0.15);
    color: #34D399;
    border: 1px solid rgba(16,185,129,0.3);
}
.sp-badge-skill {
    background: rgba(99,102,241,0.15);
    color: #A5B4FC;
    border: 1px solid rgba(99,102,241,0.3);
}

/* ── Assessment focus mode ────────────────────────────── */
.sp-question-box {
    background: linear-gradient(135deg, #12121E 0%, #15152A 100%);
    border: 1px solid #6366F1;
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin: 1.5rem 0;
    position: relative;
}
.sp-question-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #6366F1, #8B5CF6, #06B6D4);
    border-radius: 16px 16px 0 0;
}
.sp-question-text {
    font-size: 1.15rem;
    color: #E2E8F0;
    line-height: 1.7;
    font-weight: 400;
}
.sp-skill-label {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #6366F1;
    font-weight: 700;
    margin-bottom: 0.8rem;
}
.sp-diff-pill {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    margin-left: 0.5rem;
}
.diff-1 { background: rgba(16,185,129,0.15);  color: #34D399; }
.diff-2 { background: rgba(99,102,241,0.15);  color: #A5B4FC; }
.diff-3 { background: rgba(245,158,11,0.15);  color: #FCD34D; }
.diff-4 { background: rgba(239,68,68,0.15);   color: #F87171; }

/* ── Evaluation feedback ──────────────────────────────── */
.eval-strong   { color: #10B981; font-weight: 600; }
.eval-moderate { color: #F59E0B; font-weight: 600; }
.eval-weak     { color: #EF4444; font-weight: 600; }
.eval-info     { color: #6366F1; font-weight: 600; }

/* ── Progress bar override ────────────────────────────── */
.stProgress > div > div {
    background: linear-gradient(90deg, #6366F1, #8B5CF6) !important;
    border-radius: 4px;
}

/* ── Buttons ──────────────────────────────────────────── */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
    border: none !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.4) !important;
}

/* ── Text areas ───────────────────────────────────────── */
.stTextArea textarea {
    background: #12121E !important;
    border: 1px solid #1E1E35 !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
    font-size: 0.93rem !important;
}
.stTextArea textarea:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.15) !important;
}

/* ── File uploader ────────────────────────────────────── */
.stFileUploader {
    background: #12121E !important;
    border: 1px dashed #1E1E35 !important;
    border-radius: 10px !important;
}

/* ── Divider ──────────────────────────────────────────── */
.sp-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1E1E35, transparent);
    margin: 2rem 0;
}

/* ── Phase card ───────────────────────────────────────── */
.sp-phase-header {
    background: linear-gradient(135deg, #12121E, #1a1a30);
    border-left: 3px solid #6366F1;
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.5rem;
    margin-bottom: 0.8rem;
}

/* ── Resource link card ───────────────────────────────── */
.sp-resource {
    background: #0A0A0F;
    border: 1px solid #1E1E35;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    margin: 0.4rem 0;
}
.sp-resource a {
    color: #6366F1 !important;
    text-decoration: none;
    font-weight: 500;
}
.sp-resource a:hover { color: #A5B4FC !important; }
.sp-resource-desc {
    color: #64748B;
    font-size: 0.8rem;
    margin-top: 0.2rem;
}

/* ── Expander override ────────────────────────────────── */
.streamlit-expanderHeader {
    background: #12121E !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
}

/* ── Readiness bar ────────────────────────────────────── */
.sp-readiness-label {
    font-size: 4rem;
    font-weight: 900;
    text-align: center;
    line-height: 1;
}
.sp-readiness-sub {
    text-align: center;
    color: #64748B;
    font-size: 0.9rem;
    margin-top: 0.3rem;
}
</style>
"""


def inject():
    """Call this once at app startup."""
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def card(content: str, highlight: bool = False):
    """Render an HTML card."""
    cls = "sp-card-highlight" if highlight else "sp-card"
    return f'<div class="{cls}">{content}</div>'


def badge(text: str, kind: str = "skill") -> str:
    kind_map = {
        "critical":    "sp-badge sp-badge-critical",
        "important":   "sp-badge sp-badge-important",
        "nice_to_have":"sp-badge sp-badge-nice",
        "skill":       "sp-badge sp-badge-skill",
    }
    cls = kind_map.get(kind, "sp-badge sp-badge-skill")
    return f'<span class="{cls}">{text}</span>'


def diff_pill(level: int, label: str) -> str:
    return f'<span class="sp-diff-pill diff-{level}">{label}</span>'


def divider() -> str:
    return '<div class="sp-divider"></div>'