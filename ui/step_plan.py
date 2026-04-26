"""
Step 5 — Personalised Learning Plan.
Phased, adjacent-skill-first, real resources, downloadable PDF.
"""
import streamlit as st
from agents.learning_plan_agent import generate
from utils.pdf_generator import generate_pdf
from core import state


def render():
    st.markdown(
        '<div class="sp-section-title">📚 Your Personalised Learning Plan</div>',
        unsafe_allow_html=True,
    )

    gap_analysis  = state.get("gap_analysis")
    skill_map     = state.get("skill_map")
    resume_parsed = state.get("resume_parsed")
    jd_parsed     = state.get("jd_parsed")
    results       = state.get("assessment_results")

    # ── Generate plan once ─────────────────────────────────────────
    if state.get("learning_plan") is None:
        with st.status(
            "Building your personalised plan...", expanded=True
        ) as status:
            try:
                st.write("🧠 Analysing your skill gaps...")
                st.write("🔗 Identifying adjacent skill paths...")
                plan = generate(gap_analysis, skill_map, resume_parsed, jd_parsed)
                st.write("🌐 Finding real learning resources...")
                state.set("learning_plan", plan)
                status.update(label="✅ Plan ready!", state="complete")
            except Exception as e:
                status.update(label="❌ Failed", state="error")
                st.error(f"Could not generate plan: {e}")
                return

    plan = state.get("learning_plan")

    # ── Summary header ─────────────────────────────────────────────
    st.markdown(
        f'<div class="sp-card-highlight">'
        f'<div style="color:#94A3B8;font-size:0.88rem;line-height:1.7">'
        f'{plan.get("summary","")}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Key numbers ────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f'<div class="sp-metric">'
            f'<div class="sp-metric-value">{plan.get("total_estimated_weeks","?")}</div>'
            f'<div class="sp-metric-label">Total Weeks</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="sp-metric">'
            f'<div class="sp-metric-value">{plan.get("total_estimated_hours","?")}</div>'
            f'<div class="sp-metric-label">Total Hours</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div class="sp-metric">'
            f'<div class="sp-metric-value" style="font-size:1.1rem;padding-top:0.3rem">'
            f'{plan.get("weekly_schedule","?")}</div>'
            f'<div class="sp-metric-label">Weekly Schedule</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="sp-divider"></div>', unsafe_allow_html=True)

    # ── Phases ─────────────────────────────────────────────────────
    phase_colors = ["#6366F1", "#10B981", "#F59E0B"]

    for phase in plan.get("phases", []):
        pnum  = phase.get("phase_number", 1)
        ptitle= phase.get("title", f"Phase {pnum}")
        pweeks= phase.get("duration_weeks", "?")
        pclr  = phase_colors[min(pnum - 1, len(phase_colors) - 1)]

        st.markdown(
            f'<div class="sp-phase-header" style="border-left-color:{pclr}">'
            f'<div style="color:{pclr};font-size:0.72rem;font-weight:700;'
            f'text-transform:uppercase;letter-spacing:1.5px">'
            f'PHASE {pnum}</div>'
            f'<div style="color:#E2E8F0;font-size:1.15rem;font-weight:700">'
            f'{ptitle}</div>'
            f'<div style="color:#64748B;font-size:0.82rem">'
            f'{pweeks} week{"s" if pweeks != 1 else ""}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        for sk in phase.get("skills", []):
            skill_name = sk.get("skill", "")
            curr_lvl   = sk.get("current_level", "")
            tgt_lvl    = sk.get("target_level", "")
            hours      = sk.get("estimated_hours", "?")

            with st.expander(
                f"  {skill_name}   {curr_lvl} → {tgt_lvl}   ~{hours} hours"
            ):
                # Adjacent foundation — the key differentiator
                adj = sk.get("adjacent_foundation", "")
                if adj:
                    st.markdown(
                        f'<div class="sp-card" style="border-color:#6366F1">'
                        f'<div style="color:#6366F1;font-size:0.72rem;font-weight:700;'
                        f'text-transform:uppercase;letter-spacing:1px;margin-bottom:0.4rem">'
                        f'🔗 Why This Is Achievable For You</div>'
                        f'<div style="color:#E2E8F0;font-size:0.9rem;line-height:1.7">'
                        f'{adj}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                # Why now
                why = sk.get("why_now", "")
                if why:
                    st.markdown(
                        f'<div style="color:#94A3B8;font-size:0.85rem;'
                        f'margin:0.5rem 0;font-style:italic">{why}</div>',
                        unsafe_allow_html=True,
                    )

                # Learning approach
                approach = sk.get("learning_approach", "")
                if approach:
                    st.markdown(
                        f'<div style="color:#6366F1;font-size:0.75rem;font-weight:700;'
                        f'text-transform:uppercase;letter-spacing:1px;margin:0.8rem 0 0.3rem">'
                        f'📖 Learning Approach</div>'
                        f'<div style="color:#E2E8F0;font-size:0.88rem;line-height:1.6">'
                        f'{approach}</div>',
                        unsafe_allow_html=True,
                    )

                # Milestones
                milestones = sk.get("milestones", [])
                if milestones:
                    st.markdown(
                        '<div style="color:#6366F1;font-size:0.75rem;font-weight:700;'
                        'text-transform:uppercase;letter-spacing:1px;margin:0.8rem 0 0.3rem">'
                        '🏁 Milestones</div>',
                        unsafe_allow_html=True,
                    )
                    for i, m in enumerate(milestones, 1):
                        st.markdown(
                            f'<div style="color:#E2E8F0;font-size:0.87rem;'
                            f'padding:0.3rem 0;display:flex;gap:0.6rem">'
                            f'<span style="color:#6366F1;font-weight:700">{i}.</span>'
                            f'{m}</div>',
                            unsafe_allow_html=True,
                        )

                # Hands-on project
                project = sk.get("hands_on_project", "")
                if project:
                    st.markdown(
                        f'<div class="sp-card" style="margin-top:0.8rem;'
                        f'border-color:#10B981">'
                        f'<div style="color:#10B981;font-size:0.72rem;font-weight:700;'
                        f'text-transform:uppercase;letter-spacing:1px;margin-bottom:0.4rem">'
                        f'🛠️ Hands-On Project</div>'
                        f'<div style="color:#E2E8F0;font-size:0.88rem;line-height:1.6">'
                        f'{project}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                # Real resources
                resources = sk.get("resources", [])
                if resources:
                    st.markdown(
                        '<div style="color:#6366F1;font-size:0.75rem;font-weight:700;'
                        'text-transform:uppercase;letter-spacing:1px;margin:0.8rem 0 0.4rem">'
                        '📚 Learning Resources</div>',
                        unsafe_allow_html=True,
                    )
                    for r in resources:
                        title = r.get("title", "Resource")
                        url   = r.get("url", "#")
                        desc  = r.get("description", "")
                        st.markdown(
                            f'<div class="sp-resource">'
                            f'<a href="{url}" target="_blank">{title}</a>'
                            f'{"<div class=sp-resource-desc>" + desc + "</div>" if desc else ""}'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

                # Project reference links
                proj_links = sk.get("project_links", [])
                if proj_links:
                    st.markdown(
                        '<div style="color:#F59E0B;font-size:0.75rem;font-weight:700;'
                        'text-transform:uppercase;letter-spacing:1px;margin:0.8rem 0 0.3rem">'
                        '💡 Project Ideas</div>',
                        unsafe_allow_html=True,
                    )
                    for r in proj_links:
                        st.markdown(
                            f'<div class="sp-resource">'
                            f'<a href="{r.get("url","#")}" target="_blank">'
                            f'{r.get("title","Link")}</a>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

        st.markdown('<div class="sp-divider"></div>', unsafe_allow_html=True)

    # ── Motivation note ────────────────────────────────────────────
    note = plan.get("motivation_note", "")
    if note:
        st.markdown(
            f'<div class="sp-card-highlight" style="text-align:center;padding:1.5rem">'
            f'<div style="font-size:1.5rem;margin-bottom:0.5rem">💪</div>'
            f'<div style="color:#E2E8F0;font-size:0.95rem;line-height:1.7;'
            f'font-style:italic">{note}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="sp-divider"></div>', unsafe_allow_html=True)

    # ── Download PDF ───────────────────────────────────────────────
    st.markdown(
        '<div class="sp-section-title">📥 Download Your Report</div>',
        unsafe_allow_html=True,
    )

    col_pdf, col_json = st.columns(2)

    with col_pdf:
        try:
            pdf_bytes = generate_pdf(
                gap_analysis      = gap_analysis,
                learning_plan     = plan,
                assessment_results= results,
                jd_parsed         = jd_parsed,
                resume_parsed     = resume_parsed,
            )
            candidate = resume_parsed.get("name", "candidate").replace(" ", "_")
            role      = jd_parsed.get("title", "role").replace(" ", "_")
            st.download_button(
                label        = "⬇️ Download PDF Report",
                data         = pdf_bytes,
                file_name    = f"SkillProbe_{candidate}_{role}.pdf",
                mime         = "application/pdf",
                use_container_width = True,
                type         = "primary",
            )
        except Exception as e:
            st.error(f"PDF generation failed: {e}")

    with col_json:
        import json
        export = {
            "assessment_results": results,
            "gap_analysis":       gap_analysis,
            "learning_plan":      plan,
        }
        st.download_button(
            label        = "⬇️ Download JSON Data",
            data         = json.dumps(export, indent=2, default=str),
            file_name    = "skillprobe_report.json",
            mime         = "application/json",
            use_container_width = True,
        )