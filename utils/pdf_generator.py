"""
PDF Report Generator — professional downloadable report.
Fixed: safe margins, no set_x conflicts, no Unicode crashes.
"""
from fpdf import FPDF
from datetime import datetime
import config

# ── Page constants ─────────────────────────────────────────────────
PAGE_W      = 210
LEFT_MARGIN = 12
RIGHT_MARGIN= 12
CONTENT_W   = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN   # 186mm usable


def _clean(text: str) -> str:
    """Replace Unicode characters Helvetica cannot render."""
    if not text:
        return ""
    replacements = {
        "\u2014": "-",
        "\u2013": "-",
        "\u2022": "*",
        "\u2019": "'",
        "\u2018": "'",
        "\u201C": '"',
        "\u201D": '"',
        "\u2192": "->",
        "\u2190": "<-",
        "\u2713": "OK",
        "\u2717": "X",
        "\u2610": "[ ]",
        "\u2611": "[x]",
        "\u2026": "...",
        "\u00b7": "-",
        "\u2212": "-",
        "\u00a0": " ",
        "\u25b6": ">",
        "\u2705": "OK",
        "\u274c": "X",
        "\u26a0": "!",
        "\u2b50": "*",
        "\u00e9": "e",
        "\u00e8": "e",
        "\u00e0": "a",
        "\u00fc": "u",
        "\u00f6": "o",
        "\u00e4": "a",
        "\u00df": "ss",
        "\u00f1": "n",
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text.encode("latin-1", errors="ignore").decode("latin-1")


class SkillProbeReport(FPDF):

    def header(self):
        self.set_fill_color(10, 10, 15)
        self.rect(0, 0, PAGE_W, 18, "F")
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(99, 102, 241)
        self.set_xy(0, 4)
        self.cell(PAGE_W, 8, "SKILLPROBE  -  Skill Assessment Report", align="C")

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(100, 116, 139)
        self.cell(
            PAGE_W, 8,
            f"Page {self.page_no()}  |  SkillProbe  |  "
            f"{datetime.today().strftime('%B %d, %Y')}",
            align="C",
        )

    def dark_page(self):
        """Add a new page with dark background."""
        self.add_page()
        self.set_fill_color(10, 10, 15)
        self.rect(0, 0, PAGE_W, 297, "F")
        self.set_left_margin(LEFT_MARGIN)
        self.set_right_margin(RIGHT_MARGIN)
        self.set_x(LEFT_MARGIN)
        self.ln(4)

    def section_title(self, text: str):
        self.set_left_margin(LEFT_MARGIN)
        self.set_x(LEFT_MARGIN)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(99, 102, 241)
        self.set_fill_color(18, 18, 30)
        self.cell(CONTENT_W, 9, _clean(text), ln=True, fill=True)
        self.set_draw_color(99, 102, 241)
        self.line(LEFT_MARGIN, self.get_y(), PAGE_W - RIGHT_MARGIN, self.get_y())
        self.ln(4)

    def write_kv(self, key: str, value: str):
        self.set_left_margin(LEFT_MARGIN)
        self.set_x(LEFT_MARGIN)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(148, 163, 184)
        self.cell(52, 7, _clean(key) + ":")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(226, 232, 240)
        self.multi_cell(CONTENT_W - 52, 7, _clean(str(value)))

    def write_body(self, text: str, indent: int = 0,
                   color=(226, 232, 240), italic: bool = False):
        self.set_left_margin(LEFT_MARGIN + indent)
        self.set_x(LEFT_MARGIN + indent)
        style = "I" if italic else ""
        self.set_font("Helvetica", style, 9)
        self.set_text_color(*color)
        self.multi_cell(CONTENT_W - indent, 6, _clean(text))
        self.set_left_margin(LEFT_MARGIN)

    def safe_check_page(self, needed: int = 30):
        """Add new dark page if not enough space left."""
        if self.get_y() > (297 - 15 - needed):
            self.dark_page()


# ══════════════════════════════════════════════════════════════════
def generate_pdf(
    gap_analysis:        dict,
    learning_plan:       dict,
    assessment_results:  list,
    jd_parsed:           dict,
    resume_parsed:       dict,
) -> bytes:

    pdf = SkillProbeReport()
    pdf.set_auto_page_break(auto=True, margin=15)

    score     = gap_analysis.get("readiness_score", 0)
    pct       = round(score * 100)
    weeks     = gap_analysis.get("hire_ready_weeks", "?")
    candidate = _clean(resume_parsed.get("name", "Candidate"))
    role      = _clean(jd_parsed.get("title", "Target Role"))

    if score >= 0.70:
        score_rgb = (16, 185, 129)
    elif score >= 0.50:
        score_rgb = (245, 158, 11)
    else:
        score_rgb = (239, 68, 68)

    # ══════════════════════════════════════════════════════════════
    # PAGE 1 — Cover
    # ══════════════════════════════════════════════════════════════
    pdf.dark_page()

    pdf.ln(20)
    pdf.set_font("Helvetica", "B", 38)
    pdf.set_text_color(99, 102, 241)
    pdf.cell(CONTENT_W, 18, "SkillProbe", align="C", ln=True)

    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(CONTENT_W, 9, "Skill Assessment Report", align="C", ln=True)

    pdf.ln(14)
    pdf.set_font("Helvetica", "B", 72)
    pdf.set_text_color(*score_rgb)
    pdf.cell(CONTENT_W, 30, f"{pct}%", align="C", ln=True)

    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(CONTENT_W, 8, "Overall Job Readiness", align="C", ln=True)

    pdf.ln(14)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(226, 232, 240)
    for line in [
        f"Candidate :  {candidate}",
        f"Target Role :  {role}",
        f"Hire-Ready Estimate :  {weeks} weeks",
        f"Date :  {datetime.today().strftime('%B %d, %Y')}",
    ]:
        pdf.cell(CONTENT_W, 9, line, align="C", ln=True)

    # ══════════════════════════════════════════════════════════════
    # PAGE 2 — Assessment Summary
    # ══════════════════════════════════════════════════════════════
    pdf.dark_page()
    pdf.section_title("  Assessment Summary")

    obs = gap_analysis.get("overall_observation", "")
    if obs:
        pdf.write_body(obs, color=(148, 163, 184))
        pdf.ln(3)

    pdf.write_kv("Readiness Score",  f"{pct}%")
    pdf.write_kv("Hire-Ready In",    f"{weeks} weeks")
    pdf.write_kv("Claim Accuracy",   gap_analysis.get("claim_accuracy_summary", ""))
    pdf.write_kv("Skills Assessed",  str(len(assessment_results)))
    pdf.ln(5)

    # ── Skill table ────────────────────────────────────────────────
    pdf.section_title("  Skill Breakdown")

    # Column widths — must add up to CONTENT_W (186)
    cw = [46, 24, 24, 24, 20, 48]
    headers = ["Skill", "Required", "Claimed", "Assessed", "Gap", "Accuracy"]

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(148, 163, 184)
    pdf.set_fill_color(18, 18, 30)
    pdf.set_x(LEFT_MARGIN)
    for h, w in zip(headers, cw):
        pdf.cell(w, 8, h, fill=True)
    pdf.ln()

    for s in gap_analysis.get("skill_breakdown", []):
        gap_val = s.get("gap", 0)
        if gap_val <= 0.10:
            rc = (16, 185, 129)
        elif gap_val <= 0.25:
            rc = (245, 158, 11)
        else:
            rc = (239, 68, 68)

        pdf.set_font("Helvetica", "", 8)
        pdf.set_x(LEFT_MARGIN)

        pdf.set_text_color(*rc)
        pdf.cell(cw[0], 7, _clean(str(s.get("skill", "")))[:24])

        pdf.set_text_color(226, 232, 240)
        pdf.cell(cw[1], 7, f"{s.get('required', 0):.0%}")
        pdf.cell(cw[2], 7, f"{s.get('claimed',  0):.0%}")
        pdf.cell(cw[3], 7, f"{s.get('assessed', 0):.0%}")

        pdf.set_text_color(*rc)
        pdf.cell(cw[4], 7, f"{gap_val:.0%}")

        pdf.set_text_color(226, 232, 240)
        pdf.cell(cw[5], 7, _clean(str(s.get("claim_accuracy", "")))[:22])
        pdf.ln()

    pdf.ln(5)

    # ── Strengths / Gaps / Quick Wins ──────────────────────────────
    s_list = gap_analysis.get("strengths",     [])
    g_list = gap_analysis.get("critical_gaps", [])
    q_list = gap_analysis.get("quick_wins",    [])

    col_w = int(CONTENT_W / 3)   # 62mm each

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_x(LEFT_MARGIN)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(col_w, 8, "Strengths")
    pdf.set_text_color(239, 68, 68)
    pdf.cell(col_w, 8, "Critical Gaps")
    pdf.set_text_color(245, 158, 11)
    pdf.cell(col_w, 8, "Quick Wins")
    pdf.ln()

    rows = max(len(s_list), len(g_list), len(q_list), 1)
    pdf.set_font("Helvetica", "", 8)

    for i in range(rows):
        pdf.set_x(LEFT_MARGIN)
        pdf.set_text_color(16, 185, 129)
        pdf.cell(col_w, 7, ("+ " + _clean(s_list[i])[:20]) if i < len(s_list) else "")
        pdf.set_text_color(239, 68, 68)
        pdf.cell(col_w, 7, ("! " + _clean(g_list[i])[:20]) if i < len(g_list) else "")
        pdf.set_text_color(245, 158, 11)
        pdf.cell(col_w, 7, ("-> " + _clean(q_list[i])[:20]) if i < len(q_list) else "")
        pdf.ln()

    # ══════════════════════════════════════════════════════════════
    # PAGE 3+ — Learning Plan
    # ══════════════════════════════════════════════════════════════
    pdf.dark_page()
    pdf.section_title("  Personalised Learning Plan")

    summary = learning_plan.get("summary", "")
    if summary:
        pdf.write_body(summary, color=(148, 163, 184))
        pdf.ln(2)

    pdf.write_kv("Total Weeks",  str(learning_plan.get("total_estimated_weeks", "?")))
    pdf.write_kv("Total Hours",  str(learning_plan.get("total_estimated_hours", "?")))
    pdf.write_kv("Schedule",     learning_plan.get("weekly_schedule", ""))
    pdf.ln(5)

    for phase in learning_plan.get("phases", []):
        pdf.safe_check_page(40)

        phase_title = _clean(phase.get("title", "Phase"))
        phase_weeks = phase.get("duration_weeks", "?")

        pdf.set_x(LEFT_MARGIN)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(99, 102, 241)
        pdf.cell(CONTENT_W, 9, f"{phase_title}  ({phase_weeks} weeks)", ln=True)
        pdf.set_draw_color(30, 30, 53)
        pdf.line(LEFT_MARGIN, pdf.get_y(), PAGE_W - RIGHT_MARGIN, pdf.get_y())
        pdf.ln(4)

        for sk in phase.get("skills", []):
            pdf.safe_check_page(50)

            skill_name = _clean(sk.get("skill", ""))
            curr_lvl   = _clean(sk.get("current_level", ""))
            tgt_lvl    = _clean(sk.get("target_level", ""))
            hours      = sk.get("estimated_hours", "?")

            # Skill heading
            pdf.set_x(LEFT_MARGIN)
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(226, 232, 240)
            header_text = f"{skill_name}  |  {curr_lvl} -> {tgt_lvl}  |  ~{hours} hrs"
            pdf.cell(CONTENT_W, 8, header_text, ln=True)

            # Adjacent foundation
            adjacent = sk.get("adjacent_foundation", "")
            if adjacent:
                pdf.write_body(adjacent, indent=4,
                               color=(148, 163, 184), italic=True)

            # Why now
            why = sk.get("why_now", "")
            if why:
                pdf.write_body(why, indent=4, color=(100, 116, 139))

            # Milestones
            milestones = sk.get("milestones", [])
            if milestones:
                pdf.safe_check_page(20)
                pdf.set_x(LEFT_MARGIN + 4)
                pdf.set_font("Helvetica", "B", 8)
                pdf.set_text_color(99, 102, 241)
                pdf.cell(CONTENT_W - 4, 7, "Milestones:", ln=True)
                pdf.set_font("Helvetica", "", 8)
                pdf.set_text_color(226, 232, 240)
                for m in milestones:
                    pdf.set_left_margin(LEFT_MARGIN + 8)
                    pdf.set_x(LEFT_MARGIN + 8)
                    pdf.multi_cell(CONTENT_W - 8, 6, _clean(f"[ ] {m}"))
                pdf.set_left_margin(LEFT_MARGIN)

            # Project
            project = sk.get("hands_on_project", "")
            if project:
                pdf.safe_check_page(20)
                pdf.set_x(LEFT_MARGIN + 4)
                pdf.set_font("Helvetica", "B", 8)
                pdf.set_text_color(16, 185, 129)
                pdf.cell(CONTENT_W - 4, 7, "Project:", ln=True)
                pdf.write_body(project, indent=8, color=(226, 232, 240))

            # Resources
            resources = sk.get("resources", [])
            if resources:
                pdf.safe_check_page(20)
                pdf.set_x(LEFT_MARGIN + 4)
                pdf.set_font("Helvetica", "B", 8)
                pdf.set_text_color(99, 102, 241)
                pdf.cell(CONTENT_W - 4, 7, "Resources:", ln=True)

                for r in resources[:3]:
                    title = _clean(r.get("title", ""))[:50]
                    url   = _clean(r.get("url",   ""))

                    # Title line
                    pdf.set_left_margin(LEFT_MARGIN + 8)
                    pdf.set_x(LEFT_MARGIN + 8)
                    pdf.set_font("Helvetica", "", 8)
                    pdf.set_text_color(99, 102, 241)
                    pdf.multi_cell(CONTENT_W - 8, 6, f"-> {title}")

                    # URL line — truncate long URLs
                    if url:
                        short_url = url[:80] + "..." if len(url) > 80 else url
                        pdf.set_left_margin(LEFT_MARGIN + 10)
                        pdf.set_x(LEFT_MARGIN + 10)
                        pdf.set_font("Helvetica", "", 7)
                        pdf.set_text_color(100, 116, 139)
                        pdf.multi_cell(CONTENT_W - 10, 5, short_url)

                pdf.set_left_margin(LEFT_MARGIN)

            pdf.ln(3)

    # ── Motivation note ────────────────────────────────────────────
    pdf.safe_check_page(20)
    note = learning_plan.get("motivation_note", "")
    if note:
        pdf.ln(3)
        pdf.set_x(LEFT_MARGIN)
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(16, 185, 129)
        pdf.set_left_margin(LEFT_MARGIN)
        pdf.multi_cell(CONTENT_W, 7, _clean(note))

    return bytes(pdf.output())
