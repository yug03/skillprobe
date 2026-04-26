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
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

styles.inject()
state.init()

current_step = state.get("step") or 1
step_labels = {1: "Input", 2: "Parsing", 3: "Assessment", 4: "Results", 5: "Plan"}


def make_step_html(current):
    parts = []
    for num in range(1, 6):
        if num < current:
            dot_bg = "#10B981"
            dot_clr = "#000000"
            dot_lbl = "✓"
            lbl_clr = "#10B981"
            ring = "none"
            line_fill = "#10B981"
            done_pct = "100%"
        elif num == current:
            dot_bg = "#6366F1"
            dot_clr = "#FFFFFF"
            dot_lbl = str(num)
            lbl_clr = "#E2E8F0"
            ring = "0 0 0 3px rgba(99,102,241,0.28)"
            line_fill = "#6366F1"
            done_pct = "0%"
        else:
            dot_bg = "#1A1A2E"
            dot_clr = "#4B5563"
            dot_lbl = str(num)
            lbl_clr = "#4B5563"
            ring = "none"
            line_fill = "#1A1A2E"
            done_pct = "0%"

        parts.append(
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:4px;position:relative">'
            f'<div style="width:28px;height:28px;border-radius:50%;background:{dot_bg};color:{dot_clr};display:flex;align-items:center;justify-content:center;font-size:0.72rem;font-weight:800;box-shadow:{ring}">{dot_lbl}</div>'
            f'<div style="font-size:0.62rem;color:{lbl_clr};font-weight:700;letter-spacing:0.03em;white-space:nowrap">{step_labels[num]}</div>'
            f'</div>'
        )

        if num < 5:
            parts.append(
                f'<div style="flex:1;height:2px;background:#1A1A2E;margin-bottom:14px;min-width:20px;position:relative;border-radius:999px;overflow:hidden">'
                f'<div style="position:absolute;left:0;top:0;height:100%;width:{done_pct};background:{line_fill};border-radius:999px"></div>'
                f'</div>'
            )

    return "".join(parts)


# ── Top navbar ────────────────────────────────────────────────────────────────
c_logo, c_steps, c_actions = st.columns([2, 7, 3])

with c_logo:
    st.markdown(
        '<div style="display:flex;align-items:center;gap:10px;padding:4px 0">'
        '<div style="background:linear-gradient(135deg,#6366F1,#8B5CF6);border-radius:10px;width:36px;height:36px;display:flex;align-items:center;justify-content:center;font-size:1.05rem;box-shadow:0 0 16px rgba(99,102,241,0.35)">🎯</div>'
        '<div>'
        '<div style="color:#E2E8F0;font-weight:800;font-size:1.05rem;line-height:1.05;letter-spacing:-0.02em">SkillProbe</div>'
        '<div style="color:#64748B;font-size:0.62rem;letter-spacing:0.1em;font-weight:700">AI SKILL ASSESSMENT</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

with c_steps:
    st.markdown(
        f'<div style="display:flex;align-items:center;justify-content:center;gap:0;padding:4px 8px">{make_step_html(current_step)}</div>',
        unsafe_allow_html=True,
    )

with c_actions:
    a1, a2 = st.columns(2)

    with a1:
        if current_step > 1:
            if st.button("← Back", key=f"back_{current_step}", use_container_width=True):
                prev = current_step - 1
                if current_step in (3, 4):
                    state.set("assessment_engine", None)
                    state.set("current_question", None)
                    state.set("conversation_log", [])
                    state.set("parsing_done", False)
                    state.set("assessment_results", None)
                    state.set("gap_analysis", None)
                    prev = 2
                elif current_step == 5:
                    state.set("learning_plan", None)
                    prev = 4
                state.go_to_step(prev)
                st.rerun()
        else:
            st.empty()

    with a2:
        if current_step > 1:
            if st.button("＋ New", key=f"new_{current_step}", use_container_width=True, type="primary"):
                state.reset()
                st.rerun()
        else:
            st.empty()

st.markdown(
    '<div style="border-bottom:1px solid #1A1A2E;margin:0.15rem 0 1.2rem 0"></div>',
    unsafe_allow_html=True,
)

# ── Main content ──────────────────────────────────────────────────────────────
pad_l, main_col, pad_r = st.columns([0.4, 24, 0.4])
with main_col:
    {
        1: step_input.render,
        2: step_parsing.render,
        3: step_assessment.render,
        4: step_results.render,
        5: step_plan.render,
    }.get(current_step, step_input.render)()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div style="border-top:1px solid #1A1A2E;margin-top:4rem;padding:1rem 0.2rem;display:flex;align-items:center;justify-content:space-between">'
    '<div style="display:flex;align-items:center;gap:8px">'
    '<span style="font-size:0.85rem">🎯</span>'
    '<span style="color:#334155;font-size:0.72rem;font-weight:700;letter-spacing:0.04em">SkillProbe</span>'
    '<span style="color:#1E1E35;font-size:0.72rem">·</span>'
    '<span style="color:#334155;font-size:0.72rem">Deccan AI Hackathon</span>'
    '</div>'
    '<div style="display:flex;align-items:center;gap:16px">'
    '<span style="color:#334155;font-size:0.65rem">Gemini 2.0 Flash</span>'
    '<span style="color:#1E1E35">·</span>'
    '<span style="color:#334155;font-size:0.65rem">Adaptive CAT Engine</span>'
    '<span style="color:#1E1E35">·</span>'
    '<span style="color:#334155;font-size:0.65rem">Streamlit</span>'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)
