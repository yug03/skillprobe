"""
SkillProbe — Central Configuration
Loads from .env file or Streamlit secrets.
API keys are NEVER shown in the UI.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── Streamlit secrets fallback (for cloud deploy) ──────────────────
try:
    import streamlit as st
    _s = dict(st.secrets) if hasattr(st, "secrets") else {}
except Exception:
    _s = {}

# ── LLM ────────────────────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "") or _s.get("GEMINI_API_KEY", "")
GROQ_API_KEY   = os.getenv("GROQ_API_KEY",   "") or _s.get("GROQ_API_KEY",   "")
GEMINI_MODEL   = "gemini-2.0-flash"
GROQ_MODEL     = "llama-3.3-70b-versatile"
LLM_PROVIDER   = os.getenv("LLM_PROVIDER", "gemini")
MAX_TOKENS     = 4096
TEMPERATURE    = 0.3

# ── Assessment (CAT) ───────────────────────────────────────────────
DIFFICULTY_LEVELS = {
    1: "Conceptual",
    2: "Practical",
    3: "Scenario",
    4: "Architecture",
}

DIFFICULTY_DESCRIPTIONS = {
    1: "Definition & core concepts",
    2: "Implementation & usage",
    3: "Problem solving & scenarios",
    4: "Trade-offs, design & edge cases",
}

MIN_QUESTIONS        = 2
MAX_QUESTIONS        = 5
CONFIDENCE_THRESHOLD = 0.80
MAX_SKILLS           = 8

# ── Proficiency ────────────────────────────────────────────────────
PROFICIENCY_BANDS = [
    (0.0,  0.20, "Novice"),
    (0.20, 0.40, "Beginner"),
    (0.40, 0.60, "Intermediate"),
    (0.60, 0.80, "Advanced"),
    (0.80, 1.01, "Expert"),
]

def get_proficiency_label(score: float) -> str:
    for lo, hi, label in PROFICIENCY_BANDS:
        if lo <= score < hi:
            return label
    return "Unknown"

def get_proficiency_color(score: float) -> str:
    if score >= 0.75:
        return "#10B981"   # green
    elif score >= 0.50:
        return "#F59E0B"   # amber
    else:
        return "#EF4444"   # red

# ── App ────────────────────────────────────────────────────────────
APP_TITLE   = "SkillProbe"
APP_TAGLINE = "Know where you stand. Know how to get there."
APP_ICON    = "🎯"

# ── Chart colors ───────────────────────────────────────────────────
COLOR_REQUIRED = "#6366F1"
COLOR_CLAIMED  = "#10B981"
COLOR_ASSESSED = "#F59E0B"
COLOR_GAP      = "#EF4444"