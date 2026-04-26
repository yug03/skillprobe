"""
SkillProbe — Main Entry Point
Wide layout, no sidebar, full navbar with all controls.
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
    page_title            = config.APP_TITLE,
    page_icon             = config.APP_ICON,
    layout                = "wide",
    initial_sidebar_state = "collapsed",
)

# ── Inject global styles ───────────────────────────────────────────
styles.inject()

# ── Init session state ─────────────────────────────────────────────
state.init()

current_step = state.get("step")

step_labels = {
    1: "Input",
    2: "Parsing",
    3: "Assessment",
    4: "Results",
    5: "Plan",
}

# ── Build step indicators HTML ─────────────────────────────────────
step_html = ""
for num in range(1, 6):
    label = step_labels[num]
    if num < current_step:
        dot_bg  = "#10B981"
        dot_clr = "#000"
        dot_lbl = "&#10003;"
        txt_clr = "#10B981"
        fw      = "600"
    elif num == current_step:
        dot_bg  = "#6366F1"
        dot_clr = "#fff"
        dot_lbl = str(num)
        txt_clr = "#E2E8F0"
        fw      = "700"
    else:
        dot_bg  = "#1E1E35"
        dot_clr = "#4B5563"
        dot_lbl = str(num)
        txt_clr = "#4B5563"
        fw      = "400"

    step_html += f"""
      <div style="display:flex;flex-direction:column;
      align-items:center;gap:3px;min-width:52px">
        <div style="width:26px;height:26px;border-radius:50%;
        background:{dot_bg};color:{dot_clr};
        display:flex;align-items:center;justify-content:center;
        font-size:0.72rem;font-weight:700">{dot_lbl}</div>
        <div style="font-size:0.63rem;color:{txt_clr};
        font-weight:{fw};white-space:nowrap">{label}</div>
      </div>
    """
    if num < 5:
        conn = "#10B981" if num < current_step else "#1E1E35"
        step_html += f"""
          <div style="flex:1;height:1px;background:{conn};
          margin-bottom:13px;min-width:20px"></div>
        """

# ── Top navbar ─────────────────────────────────────────────────────
back_key    = f"back_btn_{current_step}"
restart_key = f"restart_btn_{current_step}"

nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(
    [2, 5, 2, 2, 1]
)

with nav_col1:
    st.markdown(
        '<div style="display:flex;align-items:center;gap:8px;padding:6px 0">'
        '<span style="font-size:1.25rem">🎯</span>'
        '<span style="color:#6366F1;font-weight:800;font-size:1.1rem;'
        'letter-spacing:-0.5px">SkillProbe</span>'
        '</div>',
        unsafe_allow_html=True,
    )

with nav_col2:
    st.markdown(
        f'<div style="display:flex;align-items:center;'
        f'justify-content:center;padding:4px 0;gap:0">'
        f'{step_html}'
        f'</div>',
        unsafe_allow_html=True,
    )

with nav_col3:
    if current_step > 1:
        if st.button("← Back", key=back_key, use_container_width=True):
            prev = current_step - 1
            if current_step == 3:
                state.set("assessment_engine", None)
                state.set("current_question",  None)
                state.set("conversation_log",  [])
                state.set("parsing_done",      False)
                prev = 2
            elif current_step == 4:
                state.set("assessment_results", None)
                state.set("gap_analysis",       None)
                state.set("current_question",   None)
                state.set("conversation_log",   [])
                state.set("assessment_engine",  None)
                state.set("parsing_done",       False)
                prev = 2
            elif current_step == 5:
                state.set("learning_plan", None)
                prev = 4
            state.go_to_step(prev)
            st.rerun()

with nav_col4:
    if current_step > 1:
        if st.button(
            "New Assessment",
            key=restart_key,
            use_container_width=True,
            type="primary",
        ):
            state.reset()
            st.rerun()

with nav_col5:
    st.markdown(
        f'<div style="text-align:right;padding:8px 0">'
        f'<span style="color:#4B5563;font-size:0.72rem">'
        f'{current_step}/5</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

# ── Divider under navbar ───────────────────────────────────────────
st.markdown(
    '<div style="border-bottom:1px solid #1E1E35;'
    'margin-bottom:1.8rem"></div>',
    unsafe_allow_html=True,
)

# ── Main content with controlled padding ───────────────────────────
_, content_col, _ = st.columns([1, 10, 1])

with content_col:
    ROUTES = {
        1: step_input.render,
        2: step_parsing.render,
        3: step_assessment.render,
        4: step_results.render,
        5: step_plan.render,
    }
    ROUTES.get(current_step, step_input.render)()

# ── Footer ─────────────────────────────────────────────────────────
st.markdown(
    '<div style="border-top:1px solid #1E1E35;margin-top:4rem;'
    'padding:1.2rem 2rem;display:flex;justify-content:space-between">'
    '<span style="color:#2D2D4E;font-size:0.75rem">'
    '🎯 SkillProbe &nbsp;·&nbsp; Deccan AI Hackathon</span>'
    '<span style="color:#2D2D4E;font-size:0.75rem">'
    'Gemini 2.0 Flash &nbsp;·&nbsp; Streamlit</span>'
    '</div>',
    unsafe_allow_html=True,
)
