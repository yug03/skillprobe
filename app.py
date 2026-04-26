"""
SkillProbe — Main Entry Point
Pure router. No logic here. Everything lives in ui/ modules.
"""
import streamlit as st
import config
from core import state
from ui import styles
from ui import (
    step_input,
    step_parsing,
    step_assessment,
    step_results,
    step_plan,
)

# ── Page config ────────────────────────────────────────────────────
st.set_page_config(
    page_title = config.APP_TITLE,
    page_icon  = config.APP_ICON,
    layout     = "centered",
    initial_sidebar_state = "collapsed",
)

# ── Inject global styles ───────────────────────────────────────────
styles.inject()

# ── Init session state ─────────────────────────────────────────────
state.init()

# ── Sidebar: progress + start over only ───────────────────────────
with st.sidebar:
    st.markdown(
        f'<div style="color:#6366F1;font-size:1.2rem;font-weight:800;'
        f'margin-bottom:1rem">🎯 SkillProbe</div>',
        unsafe_allow_html=True,
    )

    steps = [
        (1, "📄 Input"),
        (2, "🔍 Parsing"),
        (3, "🎯 Assessment"),
        (4, "📊 Results"),
        (5, "📚 Plan"),
    ]
    current = state.get("step")
    for num, label in steps:
        if num < current:
            icon = "✅"
            clr  = "#10B981"
        elif num == current:
            icon = "▶️"
            clr  = "#6366F1"
        else:
            icon = "⬜"
            clr  = "#1E1E35"
        st.markdown(
            f'<div style="color:{clr};padding:0.3rem 0;font-size:0.88rem">'
            f'{icon} {label}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    if st.button("🔄 Start Over", use_container_width=True):
        state.reset()
        st.rerun()

    st.markdown(
        '<div style="color:#1E1E35;font-size:0.72rem;margin-top:2rem">'
        'SkillProbe · Deccan AI Hackathon</div>',
        unsafe_allow_html=True,
    )

# ── Route to correct step ──────────────────────────────────────────
step = state.get("step")

ROUTES = {
    1: step_input.render,
    2: step_parsing.render,
    3: step_assessment.render,
    4: step_results.render,
    5: step_plan.render,
}

renderer = ROUTES.get(step, step_input.render)
renderer()