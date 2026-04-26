"""
Parser Agent — parse JD, resume, and map skills in ONE single LLM call.
Was 3 calls. Now 1 call. Saves 66% of parsing tokens.
"""
from models.llm_client import call_llm_json


def parse_jd(jd_text: str) -> dict:
    """Parse JD only — used when resume not yet available."""
    prompt = f"""Extract skills from this job description. Be concise.

JD:
{jd_text[:3000]}

Return JSON:
{{
    "title": "job title",
    "role_summary": "one sentence",
    "experience_years": number or null,
    "required_skills": [
        {{
            "skill": "name",
            "importance": "critical" or "important" or "nice_to_have",
            "required_proficiency": 0.0-1.0,
            "category": "programming/framework/tool/cloud/concept/devops/data/other"
        }}
    ]
}}
Rules: critical=explicitly required, important=expected, nice_to_have=bonus.
Normalize names: JS->JavaScript, k8s->Kubernetes. Max 12 skills."""
    return call_llm_json(prompt, temperature=0.1)


def parse_resume(resume_text: str) -> dict:
    """Parse resume only."""
    prompt = f"""Extract skills from this resume. Be concise.

RESUME:
{resume_text[:3000]}

Return JSON:
{{
    "name": "candidate name",
    "experience_years": number,
    "education": "degree and field",
    "summary": "one sentence",
    "skills": [
        {{
            "skill": "name",
            "claimed_proficiency": 0.0-1.0,
            "evidence": "brief reason",
            "years_used": number or null
        }}
    ]
}}
Proficiency: listed-only=0.3, used-in-project=0.5, multiple-projects=0.65,
led/architected=0.75, expert-indicators=0.88. Be conservative."""
    return call_llm_json(prompt, temperature=0.1)


def parse_all(jd_text: str, resume_text: str) -> tuple[dict, dict, dict]:
    """
    Parse JD + Resume + Map skills in ONE single LLM call.
    Saves 2 LLM calls vs calling each function separately.
    Returns (jd_parsed, resume_parsed, skill_map)
    """
    prompt = f"""You are a skill extraction and matching engine.
Do THREE things in one response.

JOB DESCRIPTION:
{jd_text[:2500]}

RESUME:
{resume_text[:2500]}

Return ONE JSON object with this exact structure:
{{
    "jd": {{
        "title": "job title",
        "role_summary": "one sentence",
        "experience_years": number or null,
        "required_skills": [
            {{
                "skill": "name",
                "importance": "critical" or "important" or "nice_to_have",
                "required_proficiency": 0.0-1.0,
                "category": "programming/framework/tool/cloud/concept/devops/data/other"
            }}
        ]
    }},
    "resume": {{
        "name": "candidate name",
        "experience_years": number,
        "education": "degree and field",
        "summary": "one sentence",
        "skills": [
            {{
                "skill": "name",
                "claimed_proficiency": 0.0-1.0,
                "evidence": "brief reason",
                "years_used": number or null
            }}
        ]
    }},
    "skill_map": {{
        "matched_skills": [
            {{
                "skill": "JD skill name",
                "importance": "critical/important/nice_to_have",
                "required_proficiency": 0.0-1.0,
                "claimed_proficiency": 0.0-1.0,
                "category": "category",
                "resume_evidence": "brief"
            }}
        ],
        "missing_skills": [
            {{
                "skill": "required but not on resume",
                "importance": "critical/important/nice_to_have",
                "required_proficiency": 0.0-1.0,
                "category": "category"
            }}
        ],
        "extra_skills": ["resume skills not required by JD"]
    }}
}}

Rules:
- JD: max 12 skills, critical=explicitly required, normalize names
- Resume proficiency: listed-only=0.3, project=0.5, multi-project=0.65, led=0.75
- Skill map: handle synonyms (K8s=Kubernetes), partial matches (Flask->FastAPI lower score)
- Be concise and conservative"""

    result = call_llm_json(prompt, temperature=0.1)

    jd_parsed     = result.get("jd", {})
    resume_parsed = result.get("resume", {})
    skill_map     = result.get("skill_map", {})

    # Build assessment queue
    skill_map["assessment_queue"] = _build_queue(skill_map)

    return jd_parsed, resume_parsed, skill_map


def _build_queue(skill_map: dict) -> list:
    from config import MAX_SKILLS
    order   = {"critical": 0, "important": 1, "nice_to_have": 2}
    matched = sorted(
        skill_map.get("matched_skills", []),
        key=lambda s: order.get(s.get("importance", "nice_to_have"), 2)
    )
    missing = [
        s for s in skill_map.get("missing_skills", [])
        if s.get("importance") == "critical"
    ]
    queue = [s["skill"] for s in matched] + [s["skill"] for s in missing]
    return queue[:MAX_SKILLS]
