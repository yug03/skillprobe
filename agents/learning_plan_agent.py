"""
Learning Plan Agent — generates a personalised, phased learning plan.
Adjacent skill reasoning is the core feature here.
Every skill in the plan explains WHY it's achievable from where the candidate is now.
"""
from models.llm_client import call_llm_json
from agents.resource_finder import find_resources, find_project_ideas
import config


def generate(gap_analysis: dict, skill_map: dict,
             resume_parsed: dict, jd_parsed: dict) -> dict:

    targets = _get_targets(gap_analysis)
    if not targets:
        return _empty_plan()

    plan = _build_plan(targets, resume_parsed, jd_parsed)
    plan = _enrich_with_resources(plan)
    return plan


def _get_targets(gap_analysis: dict) -> list[dict]:
    """Get skills that need learning, sorted by priority."""
    order  = {"critical": 0, "important": 1, "nice_to_have": 2}
    return sorted(
        [
            {
                "skill":       s["skill"],
                "current":     s["assessed"],
                "target":      s["required"],
                "gap":         s["gap"],
                "importance":  s["importance"],
                "current_lbl": config.get_proficiency_label(s["assessed"]),
                "target_lbl":  config.get_proficiency_label(s["required"]),
            }
            for s in gap_analysis.get("skill_breakdown", [])
            if s["gap"] > 0.05
        ],
        key=lambda t: (order.get(t["importance"], 2), -t["gap"])
    )


def _build_plan(targets: list, resume_parsed: dict, jd_parsed: dict) -> dict:
    existing = [s["skill"] for s in resume_parsed.get("skills", [])]
    exp_yrs  = resume_parsed.get("experience_years", "unknown")
    role     = jd_parsed.get("title", "Technical Role")

    targets_text = "\n".join(
        f"- {t['skill']}: currently {t['current_lbl']} ({t['current']:.0%}), "
        f"need {t['target_lbl']} ({t['target']:.0%}), gap {t['gap']:.0%}, {t['importance']}"
        for t in targets
    )

    prompt = f"""You are a personalised learning coach.

Create a phased learning plan for this candidate.

TARGET ROLE: {role}
CANDIDATE EXPERIENCE: {exp_yrs} years
EXISTING SKILLS: {', '.join(existing[:25])}

SKILLS TO DEVELOP:
{targets_text}

Build a 3-phase plan:
- Phase 1 "Quick Wins" (1-2 weeks): smallest gaps + adjacent skills candidate can learn fast
- Phase 2 "Core Gaps" (2-4 weeks): critical and important gaps
- Phase 3 "Advanced" (2-4 weeks): nice-to-have + depth building

For EVERY skill the adjacent_foundation MUST explain:
- What existing skill(s) make this learnable
- Why those existing skills help
- Any learning acceleration this gives the candidate
Example: "Since you already know Flask and REST API design, FastAPI is a natural next step.
Your existing routing and middleware knowledge transfers directly — estimated 40% faster to learn."

Return this exact JSON:
{{
    "summary": "2-3 sentence plan overview",
    "total_estimated_hours": number,
    "total_estimated_weeks": number,
    "weekly_schedule": "e.g. 10 hrs/week: 2h weekdays",
    "phases": [
        {{
            "phase_number": 1,
            "title": "Phase 1: Quick Wins",
            "duration_weeks": number,
            "skills": [
                {{
                    "skill": "skill name",
                    "current_level": "label",
                    "target_level": "label",
                    "estimated_hours": number,
                    "why_now": "why this skill in this phase",
                    "adjacent_foundation": "Since you already know X and Y, learning Z is realistic because... Estimated learning time: N weeks (vs M weeks without prior knowledge).",
                    "learning_approach": "specific step-by-step approach",
                    "milestones": [
                        "milestone 1 (end of week 1)",
                        "milestone 2 (end of week 2)",
                        "milestone 3 (project complete)"
                    ],
                    "hands_on_project": "specific, concrete, portfolio-worthy project description"
                }}
            ]
        }}
    ],
    "motivation_note": "genuine, encouraging closing note referencing specific strengths"
}}

RULES:
- adjacent_foundation is MANDATORY for every skill. Never leave it generic.
- milestones must be specific and measurable
- hands_on_project must be specific (not just "build a project")
- hours must be realistic (Docker basics = 15h, not 2h)
- phases must only contain skills from the skills-to-develop list
"""
    return call_llm_json(prompt, temperature=0.3)


def _enrich_with_resources(plan: dict) -> dict:
    """Add real DuckDuckGo-searched resources to every skill."""
    for phase in plan.get("phases", []):
        for sk in phase.get("skills", []):
            skill = sk.get("skill", "")
            level = sk.get("current_level", "beginner").lower()

            if "expert" in level or "advanced" in level:
                search_level = "advanced"
            elif "intermediate" in level:
                search_level = "intermediate"
            else:
                search_level = "beginner"

            try:
                sk["resources"] = find_resources(skill, level=search_level, n=2)
            except Exception:
                sk["resources"] = []

            sk["project_links"] = []

    return plan


def _empty_plan() -> dict:
    return {
        "summary": "No significant skill gaps identified. You are well-prepared for this role.",
        "total_estimated_hours": 0,
        "total_estimated_weeks": 0,
        "weekly_schedule": "N/A",
        "phases": [],
        "motivation_note": "Your skills align strongly with this role. Go apply!",
    }
