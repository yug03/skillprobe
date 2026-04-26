"""
Gap Analyzer — computes required vs claimed vs assessed for every skill.
Produces the full results object used by the results UI and PDF.
"""
from models.llm_client import call_llm
import config


def analyze(skill_map: dict, results: list[dict],
            jd_parsed: dict, resume_parsed: dict) -> dict:

    assessed_map = {r["skill"]: r for r in results}
    matched      = {s["skill"]: s for s in skill_map.get("matched_skills", [])}
    missing      = {s["skill"]: s for s in skill_map.get("missing_skills", [])}

    importance_w = {"critical": 3.0, "important": 2.0, "nice_to_have": 1.0}
    breakdown    = []
    total_gap_w  = 0.0
    total_w      = 0.0

    # ── Assessed skills ────────────────────────────────────────────
    for r in results:
        skill      = r["skill"]
        required   = r.get("required_proficiency", 0.5)
        claimed    = r.get("claimed_proficiency",  0.0)
        assessed   = r.get("assessed_proficiency", 0.0)
        importance = r.get("importance", "important")
        gap        = max(0.0, required - assessed)
        diff       = claimed - assessed

        if   abs(diff) <= 0.10: accuracy = "Accurate"
        elif diff >   0.20:     accuracy = "Overstated"
        elif diff >   0.10:     accuracy = "Slightly overstated"
        elif diff <  -0.20:     accuracy = "Stronger than claimed"
        else:                   accuracy = "Slightly understated"

        breakdown.append({
            "skill":            skill,
            "required":         required,
            "claimed":          claimed,
            "assessed":         assessed,
            "gap":              round(gap, 3),
            "claim_accuracy":   accuracy,
            "importance":       importance,
            "observation":      r.get("observation", ""),
            "confidence":       r.get("confidence", 0.0),
            "questions_asked":  r.get("questions_asked", 0),
            "max_difficulty":   r.get("max_difficulty", 0),
        })

        w           = importance_w.get(importance, 1.0)
        total_gap_w += gap * w
        total_w     += w

    # ── Unassessed missing skills ──────────────────────────────────
    for skill, s in missing.items():
        if skill not in assessed_map:
            req        = s.get("required_proficiency", 0.5)
            importance = s.get("importance", "important")
            breakdown.append({
                "skill":           skill,
                "required":        req,
                "claimed":         0.0,
                "assessed":        0.0,
                "gap":             req,
                "claim_accuracy":  "Not on resume",
                "importance":      importance,
                "observation":     "Not assessed — skill absent from resume.",
                "confidence":      0.0,
                "questions_asked": 0,
                "max_difficulty":  0,
            })
            w           = importance_w.get(importance, 1.0)
            total_gap_w += req * w
            total_w     += w

    # ── Readiness ──────────────────────────────────────────────────
    avg_gap        = (total_gap_w / total_w) if total_w else 0.0
    readiness      = round(max(0.0, 1.0 - avg_gap), 3)

    if   readiness >= 0.85: weeks = 1
    elif readiness >= 0.70: weeks = 3
    elif readiness >= 0.50: weeks = 6
    elif readiness >= 0.30: weeks = 10
    else:                   weeks = 16

    # ── Categories ────────────────────────────────────────────────
    strengths = [
        s["skill"] for s in breakdown
        if s["gap"] <= 0.10 and s["assessed"] >= 0.55
    ]
    critical_gaps = [
        s["skill"] for s in breakdown
        if s["gap"] > 0.20 and s["importance"] == "critical"
    ]
    quick_wins = [
        s["skill"] for s in breakdown
        if 0.05 < s["gap"] <= 0.25 and s["assessed"] >= 0.25
    ]

    # ── Claim accuracy summary ─────────────────────────────────────
    accurate    = sum(1 for s in breakdown if s["claim_accuracy"] == "Accurate")
    overstated  = sum(1 for s in breakdown if "overstated" in s["claim_accuracy"].lower())
    understated = sum(1 for s in breakdown if "stronger" in s["claim_accuracy"].lower() or
                                               "understated" in s["claim_accuracy"].lower())
    total       = len(breakdown)
    acc_parts   = []
    if accurate:    acc_parts.append(f"{accurate}/{total} skills accurately represented")
    if overstated:  acc_parts.append(f"{overstated}/{total} overstated")
    if understated: acc_parts.append(f"{understated}/{total} stronger than claimed")
    claim_summary = ". ".join(acc_parts) + "." if acc_parts else "Insufficient data."

    # ── Overall observation (LLM) ──────────────────────────────────
    detail = "\n".join(
        f"- {s['skill']}: required {s['required']:.0%}, "
        f"assessed {s['assessed']:.0%}, gap {s['gap']:.0%}, {s['claim_accuracy']}"
        for s in breakdown[:10]
    )
    obs_prompt = (
        f"Write 2 sentences summarizing this candidate for {jd_parsed.get('title','the role')}. "
        f"Readiness: {readiness:.0%}. "
        f"Strengths: {', '.join(strengths[:3]) or 'None'}. "
        f"Gaps: {', '.join(critical_gaps[:3]) or 'None'}. "
        f"Be specific and constructive. Return only the summary."
    )
    overall_obs = call_llm(obs_prompt, temperature=0.3)

    return {
        "readiness_score":      readiness,
        "hire_ready_weeks":     weeks,
        "skill_breakdown":      breakdown,
        "strengths":            strengths,
        "critical_gaps":        critical_gaps,
        "quick_wins":           quick_wins,
        "claim_accuracy_summary": claim_summary,
        "overall_observation":  overall_obs,
    }
