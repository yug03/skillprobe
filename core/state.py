"""
Session State Manager
Single source of truth for all Streamlit session state.
Every key is defined here. No scattered st.session_state['x'] = y elsewhere.
"""
import streamlit as st


# ── All state keys and their defaults ─────────────────────────────
DEFAULTS = {
    # Navigation
    "step": 1,

    # Raw inputs
    "jd_text": "",
    "resume_text": "",
    "jd_input_buffer": "",
    "resume_input_buffer": "",

    # Parsed data
    "jd_parsed": None,
    "resume_parsed": None,
    "skill_map": None,

    # Assessment
    "assessment_engine": None,
    "current_question": None,
    "conversation_log": [],

    # Results
    "assessment_results": None,
    "gap_analysis": None,

    # Learning plan
    "learning_plan": None,

    # UI state
    "parsing_done": False,
    "assessment_complete": False,
}


def init():
    """Initialize all session state keys with defaults if not set."""
    for key, default in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default


def get(key: str):
    """Get a session state value."""
    return st.session_state.get(key, DEFAULTS.get(key))


def set(key: str, value):
    """Set a session state value."""
    st.session_state[key] = value


def reset():
    """Reset all state to defaults (Start Over)."""
    for key, default in DEFAULTS.items():
        st.session_state[key] = default


def go_to_step(step: int):
    """Navigate to a step."""
    st.session_state["step"] = step