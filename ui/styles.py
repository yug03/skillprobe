"""
Global CSS for SkillProbe.
Dark, focused, aesthetic — not a typical LLM chatbot.
"""

GLOBAL_CSS = """
<style>
/* ── Reset & Base ─────────────────────────────────────────────────── */
* { box-sizing: border-box; }

/* Hide Streamlit chrome */
#MainMenu                         { visibility: hidden; }
footer                            { visibility: hidden; }
header                            { visibility: hidden; }
[data-testid="collapsedControl"]  { display: none !important; }
section[data-testid="stSidebar"]  { display: none !important; }

/* Remove default top padding */
.main .block-container {
    padding-top: 0.8rem;
    padding-bottom: 4rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
    max-width: 100% !important;
}

/* Scrollbar */
::-webkit-scrollbar              { width: 6px; height: 6px; }
::-webkit-scrollbar-track        { background: #0A0A0F; }
::-webkit-scrollbar-thumb        { background: #1E1E35; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover  { background: #6366F1; }

/* ── Typography ───────────────────────────────────────────────────── */
.sp-hero-title {
    font-size: 3.4rem;
    font-weight: 900;
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 45%, #06B6D4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    letter-spacing: -1.5px;
    line-height: 1.08;
    margin-bottom: 0.4rem;
}

.sp-hero-sub {
    text-align: center;
    color: #475569;
    font-size: 1.05rem;
    letter-spacing: 0.2px;
    margin-bottom: 0.2rem;
}

.sp-tagline {
    text-align: center;
    color: #334155;
    font-size: 0.85rem;
    letter-spacing: 0.06em;
    font-weight: 600;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
}

.sp-section-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #CBD5E1;
    margin: 2rem 0 0.8rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    letter-spacing: -0.02em;
}

.sp-section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1E1E35, transparent);
    margin-left: 0.5rem;
}

.sp-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 0.4rem;
}

/* ── Cards ────────────────────────────────────────────────────────── */
.sp-card {
    background: #12121E;
    border: 1px solid #1A1A2E;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    transition: border-color 0.25s, box-shadow 0.25s;
}
.sp-card:hover {
    border-color: #2D2D50;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}

.sp-card-highlight {
    background: linear-gradient(135deg, #12121E 0%, #14142A 100%);
    border: 1px solid #6366F1;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    box-shadow: 0 0 24px rgba(99,102,241,0.08);
}

.sp-card-success {
    background: linear-gradient(135deg, #0A1A12 0%, #0D1F16 100%);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
}

.sp-card-warning {
    background: linear-gradient(135deg, #1A1200 0%, #1F1600 100%);
    border: 1px solid rgba(245,158,11,0.3);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
}

.sp-card-danger {
    background: linear-gradient(135deg, #1A0A0A 0%, #1F0D0D 100%);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
}

.sp-glass {
    background: rgba(18,18,30,0.7);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid #1E1E35;
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1rem;
}

/* ── Metric Cards ─────────────────────────────────────────────────── */
.sp-metric {
    background: #12121E;
    border: 1px solid #1A1A2E;
    border-radius: 14px;
    padding: 1.4rem 1rem;
    text-align: center;
    transition: border-color 0.2s, transform 0.2s;
    position: relative;
    overflow: hidden;
}
.sp-metric::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #6366F1, #8B5CF6);
    opacity: 0.6;
}
.sp-metric:hover {
    border-color: #6366F1;
    transform: translateY(-2px);
}
.sp-metric-value {
    font-size: 2.2rem;
    font-weight: 900;
    color: #6366F1;
    line-height: 1;
    letter-spacing: -1px;
}
.sp-metric-label {
    font-size: 0.68rem;
    color: #475569;
    margin-top: 0.4rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 700;
}
.sp-metric-sub {
    font-size: 0.75rem;
    color: #334155;
    margin-top: 0.2rem;
}

/* ── Metric accent colors ─────────────────────────────────────────── */
.sp-metric-green  .sp-metric-value { color: #10B981; }
.sp-metric-green::before           { background: linear-gradient(90deg, #10B981, #059669); }
.sp-metric-amber  .sp-metric-value { color: #F59E0B; }
.sp-metric-amber::before           { background: linear-gradient(90deg, #F59E0B, #D97706); }
.sp-metric-red    .sp-metric-value { color: #EF4444; }
.sp-metric-red::before             { background: linear-gradient(90deg, #EF4444, #DC2626); }
.sp-metric-cyan   .sp-metric-value { color: #06B6D4; }
.sp-metric-cyan::before            { background: linear-gradient(90deg, #06B6D4, #0891B2); }

/* ── Skill Badges ─────────────────────────────────────────────────── */
.sp-badge {
    display: inline-block;
    padding: 3px 11px;
    border-radius: 20px;
    font-size: 0.74rem;
    font-weight: 700;
    margin: 2px 3px;
    letter-spacing: 0.02em;
}
.sp-badge-critical {
    background: rgba(239,68,68,0.12);
    color: #FCA5A5;
    border: 1px solid rgba(239,68,68,0.25);
}
.sp-badge-important {
    background: rgba(245,158,11,0.12);
    color: #FDE68A;
    border: 1px solid rgba(245,158,11,0.25);
}
.sp-badge-nice {
    background: rgba(16,185,129,0.12);
    color: #6EE7B7;
    border: 1px solid rgba(16,185,129,0.25);
}
.sp-badge-skill {
    background: rgba(99,102,241,0.12);
    color: #C7D2FE;
    border: 1px solid rgba(99,102,241,0.25);
}
.sp-badge-cyan {
    background: rgba(6,182,212,0.12);
    color: #A5F3FC;
    border: 1px solid rgba(6,182,212,0.25);
}
.sp-badge-gap {
    background: rgba(239,68,68,0.12);
    color: #FCA5A5;
    border: 1px solid rgba(239,68,68,0.25);
}
.sp-badge-match {
    background: rgba(16,185,129,0.12);
    color: #6EE7B7;
    border: 1px solid rgba(16,185,129,0.25);
}

/* ── Difficulty Pills ─────────────────────────────────────────────── */
.sp-diff-pill {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.04em;
}
.diff-1 { background: rgba(16,185,129,0.12);  color: #6EE7B7;  border: 1px solid rgba(16,185,129,0.2); }
.diff-2 { background: rgba(99,102,241,0.12);  color: #C7D2FE;  border: 1px solid rgba(99,102,241,0.2); }
.diff-3 { background: rgba(245,158,11,0.12);  color: #FDE68A;  border: 1px solid rgba(245,158,11,0.2); }
.diff-4 { background: rgba(239,68,68,0.12);   color: #FCA5A5;  border: 1px solid rgba(239,68,68,0.2);  }

/* ── Assessment Focus Mode ────────────────────────────────────────── */
.sp-question-box {
    background: linear-gradient(160deg, #0E0E1E 0%, #12122A 100%);
    border: 1px solid #6366F1;
    border-radius: 20px;
    padding: 2.2rem 2.5rem;
    margin: 1.2rem 0 1.5rem 0;
    position: relative;
    box-shadow: 0 0 40px rgba(99,102,241,0.07), inset 0 1px 0 rgba(99,102,241,0.1);
}
.sp-question-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6366F1 0%, #8B5CF6 50%, #06B6D4 100%);
    border-radius: 20px 20px 0 0;
}
.sp-question-number {
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #6366F1;
    margin-bottom: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.sp-question-text {
    font-size: 1.18rem;
    color: #E2E8F0;
    line-height: 1.75;
    font-weight: 400;
}

.sp-skill-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 30px;
    padding: 5px 14px;
    font-size: 0.8rem;
    font-weight: 700;
    color: #A5B4FC;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.sp-eval-box {
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    margin-top: 1rem;
    border-left: 3px solid;
}
.sp-eval-strong  { background: rgba(16,185,129,0.07); border-color: #10B981; }
.sp-eval-moderate{ background: rgba(245,158,11,0.07); border-color: #F59E0B; }
.sp-eval-weak    { background: rgba(239,68,68,0.07);  border-color: #EF4444; }

.eval-strong   { color: #34D399; font-weight: 700; }
.eval-moderate { color: #FCD34D; font-weight: 700; }
.eval-weak     { color: #F87171; font-weight: 700; }
.eval-info     { color: #A5B4FC; font-weight: 700; }

/* ── Progress Bar ─────────────────────────────────────────────────── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #6366F1, #8B5CF6) !important;
    border-radius: 4px !important;
}

/* ── Buttons ──────────────────────────────────────────────────────── */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
    font-size: 0.9rem !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
    border: none !important;
    box-shadow: 0 2px 12px rgba(99,102,241,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(99,102,241,0.45) !important;
}
.stButton > button[kind="secondary"] {
    background: #12121E !important;
    border: 1px solid #1E1E35 !important;
    color: #94A3B8 !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: #6366F1 !important;
    color: #E2E8F0 !important;
}

/* ── Text Areas ───────────────────────────────────────────────────── */
.stTextArea textarea {
    background: #0D0D1A !important;
    border: 1px solid #1A1A2E !important;
    border-radius: 12px !important;
    color: #CBD5E1 !important;
    font-size: 0.9rem !important;
    line-height: 1.6 !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
    outline: none !important;
}

/* ── File Uploader ────────────────────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: #0D0D1A !important;
    border: 1px dashed #1A1A2E !important;
    border-radius: 12px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #6366F1 !important;
}

/* ── Expanders ────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: #12121E !important;
    border: 1px solid #1A1A2E !important;
    border-radius: 12px !important;
    margin-bottom: 0.5rem !important;
    overflow: hidden !important;
}
[data-testid="stExpander"]:hover {
    border-color: #2D2D50 !important;
}
.streamlit-expanderHeader {
    background: #12121E !important;
    border-radius: 12px !important;
    color: #CBD5E1 !important;
    font-weight: 600 !important;
    padding: 0.8rem 1rem !important;
}
.streamlit-expanderContent {
    background: #0E0E1A !important;
    border-top: 1px solid #1A1A2E !important;
    padding: 1rem !important;
}

/* ── Dividers ─────────────────────────────────────────────────────── */
.sp-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, #1E1E35 30%, #1E1E35 70%, transparent 100%);
    margin: 2rem 0;
    border: none;
}
.sp-divider-subtle {
    height: 1px;
    background: #0F0F1E;
    margin: 1rem 0;
    border: none;
}

/* ── Phase / Roadmap Cards ────────────────────────────────────────── */
.sp-phase-header {
    background: linear-gradient(135deg, #12121E 0%, #14142A 100%);
    border-left: 4px solid #6366F1;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.5rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.sp-phase-title {
    font-size: 1.05rem;
    font-weight: 800;
    color: #E2E8F0;
    letter-spacing: -0.02em;
}
.sp-phase-meta {
    font-size: 0.75rem;
    color: #475569;
    font-weight: 600;
}
.sp-phase-1 { border-color: #10B981; }
.sp-phase-2 { border-color: #6366F1; }
.sp-phase-3 { border-color: #F59E0B; }

/* ── Adjacent Foundation Box (KEY FEATURE) ────────────────────────── */
.sp-adjacent-box {
    background: linear-gradient(135deg, #0D1220 0%, #0F1428 100%);
    border: 1px solid rgba(6,182,212,0.35);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    position: relative;
    overflow: hidden;
}
.sp-adjacent-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #06B6D4, #0EA5E9);
}
.sp-adjacent-label {
    font-size: 0.65rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #06B6D4;
    margin-bottom: 0.4rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.sp-adjacent-text {
    font-size: 0.88rem;
    color: #94A3B8;
    line-height: 1.6;
}

/* ── Resource Link Cards ──────────────────────────────────────────── */
.sp-resource {
    background: #0A0A15;
    border: 1px solid #1A1A2E;
    border-radius: 10px;
    padding: 0.8rem 1.1rem;
    margin: 0.4rem 0;
    transition: border-color 0.2s, transform 0.2s;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}
.sp-resource:hover {
    border-color: #6366F1;
    transform: translateX(3px);
}
.sp-resource a {
    color: #818CF8 !important;
    text-decoration: none !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
}
.sp-resource a:hover {
    color: #C7D2FE !important;
    text-decoration: underline !important;
}
.sp-resource-desc {
    color: #475569;
    font-size: 0.77rem;
    line-height: 1.5;
}

/* ── Score Display ────────────────────────────────────────────────── */
.sp-big-score {
    font-size: 5rem;
    font-weight: 900;
    text-align: center;
    line-height: 1;
    letter-spacing: -3px;
}
.sp-score-label {
    font-size: 1rem;
    font-weight: 700;
    text-align: center;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 0.3rem;
}
.sp-readiness-sub {
    text-align: center;
    color: #475569;
    font-size: 0.85rem;
    margin-top: 0.4rem;
}

/* ── Skill Breakdown Row ──────────────────────────────────────────── */
.sp-skill-row {
    background: #0E0E1A;
    border: 1px solid #1A1A2E;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin: 0.35rem 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: border-color 0.2s;
}
.sp-skill-row:hover {
    border-color: #2D2D50;
}

/* ── Info Box ─────────────────────────────────────────────────────── */
.sp-info-box {
    background: rgba(99,102,241,0.06);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    font-size: 0.88rem;
    color: #94A3B8;
    line-height: 1.65;
}

/* ── Milestone List ───────────────────────────────────────────────── */
.sp-milestone {
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    padding: 0.35rem 0;
    font-size: 0.86rem;
    color: #94A3B8;
    line-height: 1.5;
}
.sp-milestone::before {
    content: '◆';
    color: #6366F1;
    font-size: 0.5rem;
    margin-top: 0.35rem;
    flex-shrink: 0;
}

/* ── Strength / Gap / Win tags ────────────────────────────────────── */
.sp-tag-strength {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 8px;
    padding: 0.45rem 0.9rem;
    font-size: 0.82rem;
    color: #6EE7B7;
    font-weight: 600;
    margin: 0.25rem;
}
.sp-tag-gap {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.2);
    border-radius: 8px;
    padding: 0.45rem 0.9rem;
    font-size: 0.82rem;
    color: #FCA5A5;
    font-weight: 600;
    margin: 0.25rem;
}
.sp-tag-win {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.2);
    border-radius: 8px;
    padding: 0.45rem 0.9rem;
    font-size: 0.82rem;
    color: #FDE68A;
    font-weight: 600;
    margin: 0.25rem;
}

/* ── Stat Row ─────────────────────────────────────────────────────── */
.sp-stat-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid #0F0F1E;
    font-size: 0.85rem;
}
.sp-stat-key   { color: #475569; font-weight: 600; }
.sp-stat-value { color: #E2E8F0; font-weight: 700; }

/* ── Step Track ───────────────────────────────────────────────────── */
.step-track {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    padding: 6px 0;
}
</style>
"""


def inject():
    """Inject global CSS once at app startup."""
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ── HTML helpers ───────────────────────────────────────────────────────────────

def card(content: str, highlight: bool = False) -> str:
    cls = "sp-card-highlight" if highlight else "sp-card"
    return f'<div class="{cls}">{content}</div>'


def badge(text: str, kind: str = "skill") -> str:
    kind_map = {
        "critical":     "sp-badge sp-badge-critical",
        "important":    "sp-badge sp-badge-important",
        "nice_to_have": "sp-badge sp-badge-nice",
        "skill":        "sp-badge sp-badge-skill",
        "cyan":         "sp-badge sp-badge-cyan",
        "gap":          "sp-badge sp-badge-gap",
        "match":        "sp-badge sp-badge-match",
    }
    cls = kind_map.get(kind, "sp-badge sp-badge-skill")
    return f'<span class="{cls}">{text}</span>'


def diff_pill(level: int, label: str) -> str:
    return f'<span class="sp-diff-pill diff-{level}">{label}</span>'


def divider() -> str:
    return '<div class="sp-divider"></div>'


def metric_card(value: str, label: str, sub: str = "", color: str = "") -> str:
    color_cls = f"sp-metric-{color}" if color else ""
    sub_html  = f'<div class="sp-metric-sub">{sub}</div>' if sub else ""
    return (
        f'<div class="sp-metric {color_cls}">'
        f'<div class="sp-metric-value">{value}</div>'
        f'<div class="sp-metric-label">{label}</div>'
        f'{sub_html}'
        f'</div>'
    )


def adjacent_box(text: str) -> str:
    return (
        f'<div class="sp-adjacent-box">'
        f'<div class="sp-adjacent-label">🔗 Adjacent Foundation</div>'
        f'<div class="sp-adjacent-text">{text}</div>'
        f'</div>'
    )


def info_box(text: str) -> str:
    return f'<div class="sp-info-box">{text}</div>'


def section_title(icon: str, title: str) -> str:
    return f'<div class="sp-section-title">{icon} {title}</div>'


def skill_chip(name: str) -> str:
    return f'<span class="sp-skill-chip">⚡ {name}</span>'
