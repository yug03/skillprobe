"""
SkillProbe — Main Entry Point
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

st.set_page_config(
    page_title            = config.APP_TITLE,
    page_icon             = config.APP_ICON,
    layout                = "wide",
    initial_sidebar_state = "collapsed",
)

styles.inject()
state.init()

current_step = state.get("step")
step_labels  = {1:"Input", 2:"Parsing", 3:"Assessment", 4:"Results", 5:"Plan"}

# ── Build step dots ────────────────────────────────────────────────
def make_step_html(current):
    parts = []
    for num in range(1, 6):
        if num < current:
            bg, clr, lbl, tclr = "#10B981", "#000", "✓", "#10B981"
        elif num == current:
            bg, clr, lbl, tclr = "#6366F1", "#fff", str(num), "#E2E8F0"
        else:
            bg, clr, lbl, tclr = "#1E1E35", "#4B5563", str(num), "#4B5563"

        dot = (
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:3px">'
            f'<div style="width:26px;height:26px;border-radius:50%;background:{bg};'
            f'color:{clr};display:flex;align-items:center;justify-content:center;'
            f'font-size:0.72rem;font-weight:700">{lbl}</div>'
            f'<div style="font-size:0.63rem;color:{tclr};white-space:nowrap">'
            f'{step_labels[num]}</div></div>'
        )
        parts.append(dot)

        if num < 5:
            line_color = "#10B981" if num < current else "#1E1E35"
            parts.append(
                f'<div style="flex:1;height:1px;background:{line_color};'
                f'margin-bottom:12px;min-width:16px"></div>'
            )

    return "".join(parts)


# ── Navbar ─────────────────────────────────────────────────────────
c_logo, c_steps, c_back, c_new, c_num = st.columns([2, 6, 1, 2, 1])

with c_logo:
    st.markdown(
        '<div style="padding:8px 0;display:flex;align-items:center;gap:8px">'
        '<span style="font-size:1.3rem">🎯</span>'
        '<span style="color:#6366F1;font-weight:800;font-size:1.1rem">SkillProbe</span>'
        '</div>',
        unsafe_allow_html=True,
    )

with c_steps:
    step_html = make_step_html(current_step)
    st.markdown(
        f'<div style="display:flex;align-items:center;justify-content:center;'
        f'padding:4px 0;gap:0">{step_html}</div>',
        unsafe_allow_html=True,
    )

with c_back:
    if current_step > 1:
        if st.button("← Back", key=f"back_{current_step}", use_container_width=True):
            prev = current_step - 1
            if current_step in (3, 4):
                state.set("assessment_engine",  None)
                state.set("current_question",   None)
                state.set("conversation_log",   [])
                state.set("parsing_done",       False)
                state.set("assessment_results", None)
                state.set("gap_analysis",       None)
                prev = 2
            elif current_step == 5:
                state.set("learning_plan", None)
                prev = 4
            state.go_to_step(prev)
            st.rerun()

with c_new:
    if current_step > 1:
        if st.button(
            "＋ New Assessment",
            key=f"new_{current_step}",
            use_container_width=True,
            type="primary",
        ):
            state.reset()
            st.rerun()

with c_num:
    st.markdown(
        f'<div style="text-align:right;padding:10px 0">'
        f'<span style="color:#4B5563;font-size:0.75rem">{current_step}/5</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

# ── Divider ────────────────────────────────────────────────────────
st.markdown(
    '<div style="border-bottom:1px solid #1E1E35;margin-bottom:2rem"></div>',
    unsafe_allow_html=True,
)

# ── Content ────────────────────────────────────────────────────────
_, main, _ = st.columns([1, 10, 1])
with main:
    {
        1: step_input.render,
        2: step_parsing.render,
        3: step_assessment.render,
        4: step_results.render,
        5: step_plan.render,
    }.get(current_step, step_input.render)()

# ── Footer ─────────────────────────────────────────────────────────
st.markdown(
    '<div style="border-top:1px solid #1E1E35;margin-top:4rem;padding:1rem 2rem;'
    'display:flex;justify-content:space-between">'
    '<span style="color:#2D2D4E;font-size:0.75rem">🎯 SkillProbe · Deccan AI Hackathon</span>'
    '<span style="color:#2D2D4E;font-size:0.75rem">Gemini 2.0 Flash · Streamlit</span>'
    '</div>',
    unsafe_allow_html=True,
)
