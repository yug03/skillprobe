"""
Answer Evaluator — scores a candidate answer on 5 dimensions.
Every score comes with explicit reasoning. No black boxes.
"""
from models.llm_client import call_llm_json
import config


def evaluate(skill: str, question: str, answer: str,
             difficulty: int, role_title: str = "") -> dict:
    """
    Evaluate one answer.

    Returns:
        quality:             strong | moderate | weak | no_answer
        score:               0.0 - 1.0
        reasoning:           2-3 sentence explanation
        key_points_covered:  list of strings
        key_points_missed:   list of strings
        demonstrated_depth:  short label
    """
    # Handle skipped answers immediately
    if not answer or answer.strip().lower() in {
        "skip", "s", "pass", "idk", "i don't know",
        "no idea", "not sure", "n/a", ""
    }:
        return {
            "quality": "no_answer",
            "score": 0.0,
            "reasoning": "No answer provided.",
            "key_points_covered": [],
            "key_points_missed": ["No attempt made"],
            "demonstrated_depth": "None",
        }

    diff_label = config.DIFFICULTY_LEVELS.get(difficulty, "Unknown")
    diff_desc  = config.DIFFICULTY_DESCRIPTIONS.get(difficulty, "")

    prompt = f"""You are an expert technical assessor evaluating a candidate for: {role_title or "a technical role"}.

SKILL BEING TESTED: {skill}
DIFFICULTY: Level {difficulty} — {diff_label} ({diff_desc})

QUESTION:
{question}

CANDIDATE ANSWER:
{answer}

Evaluate on these 5 dimensions:
1. Correctness      — Is the information accurate?
2. Depth            — Does it go beyond surface level?
3. Relevance        — Does it actually answer the question?
4. Completeness     — Are key aspects covered?
5. Practical signal — Does it show real hands-on experience?

Level-specific expectations:
- Level 1: Good = clear accurate definition/explanation
- Level 2: Good = mentions specific implementation details, real usage
- Level 3: Good = structured approach, considers edge cases, real scenario thinking
- Level 4: Good = trade-off awareness, system-level thinking, defends choices

Return this exact JSON:
{{
    "quality": "strong" or "moderate" or "weak" or "no_answer",
    "score": 0.0 to 1.0,
    "reasoning": "2-3 sentences explaining the score",
    "key_points_covered": ["point1", "point2"],
    "key_points_missed": ["missed1"],
    "demonstrated_depth": "one short label e.g. Surface-level / Practical / Deep"
}}

Score bands:
- strong:    0.80 - 1.00  (accurate, deep, shows real experience)
- moderate:  0.50 - 0.79  (mostly correct, some gaps)
- weak:      0.10 - 0.49  (partial or surface only)
- no_answer: 0.00
"""
    result = call_llm_json(prompt, temperature=0.2)

    # Clamp score to quality band
    bands = {
        "strong":    (0.80, 1.00),
        "moderate":  (0.50, 0.79),
        "weak":      (0.10, 0.49),
        "no_answer": (0.00, 0.00),
    }
    quality = result.get("quality", "weak")
    lo, hi  = bands.get(quality, (0.0, 1.0))
    result["score"] = max(lo, min(hi, float(result.get("score", lo))))

    return result