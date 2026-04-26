"""
Skill Mapper — match JD requirements against resume claims.
Builds the prioritised assessment queue.
"""
from models.llm_client import call_llm_json
import config


def map_skills(jd_parsed: dict, resume_parsed: dict) -> dict:
    jd_skills     = jd_parsed.get("required_skills", [])
    resume_skills = resume_parsed.get("skills", [])

    jd_list = "\n".join(
        f"- {s['skill']} | {s['importance']} | required_proficiency {s['required_proficiency']}"
        for s in jd_skills
    )
    resume_list = "\n".join(
        f"- {s['skill']} | claimed {s['claimed_proficiency']} | {s.get('evidence', '')}"
        for s in resume_skills
    )

    prompt = f"""You are a skill matching engine.

Match job requirements against resume skills.

JOB REQUIRES:
{jd_list}

RESUME CLAIMS:
{resume_list}

Rules:
- Handle synonyms: K8s=Kubernetes, JS=JavaScript, Postgres=PostgreSQL
- Handle partial matches: Flask partially covers FastAPI (set lower claimed_proficiency)
- If resume shows adjacent skill, note it but keep claimed_proficiency lower

Return this exact JSON:
{{
    "matched_skills": [
        {{
            "skill": "JD skill name",
            "importance": "critical/important/nice_to_have",
            "required_proficiency": 0.0-1.0,
            "claimed_proficiency": 0.0-1.0,
            "category": "category from JD",
            "resume_evidence": "what on resume supports this"
        }}
    ],
    "missing_skills": [
        {{
            "skill": "skill required by JD with no resume match",
            "importance": "critical/important/nice_to_have",
            "required_proficiency": 0.0-1.0,
            "category": "category"
        }}
    ],
    "extra_skills": ["skills on resume not required by JD"]
}}
"""
    result = call_llm_json(prompt, temperature=0.1)
    result["assessment_queue"] = _build_queue(result)
    return result


def _build_queue(skill_map: dict) -> list:
    """
    Build ordered assessment queue.
    Priority: critical matched → important matched → critical missing
    Cap at MAX_SKILLS.
    """
    order  = {"critical": 0, "important": 1, "nice_to_have": 2}
    matched = sorted(
        skill_map.get("matched_skills", []),
        key=lambda s: order.get(s.get("importance", "nice_to_have"), 2)
    )
    missing = [
        s for s in skill_map.get("missing_skills", [])
        if s.get("importance") == "critical"
    ]

    queue = [s["skill"] for s in matched] + [s["skill"] for s in missing]
    return queue[:config.MAX_SKILLS]