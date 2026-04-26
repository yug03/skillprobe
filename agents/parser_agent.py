"""
Parser Agent — extract structured skills from JD and resume.
"""
from models.llm_client import call_llm_json


def parse_jd(jd_text: str) -> dict:
    prompt = f"""You are a job description analyst.

Extract structured information from this job description.

JD TEXT:
---
{jd_text}
---

Return this exact JSON:
{{
    "title": "job title",
    "role_summary": "one sentence of what this role does",
    "experience_years": number or null,
    "required_skills": [
        {{
            "skill": "concise skill name (e.g. Python, Docker, FastAPI)",
            "importance": "critical" or "important" or "nice_to_have",
            "required_proficiency": 0.0 to 1.0,
            "category": "programming" or "framework" or "tool" or "cloud" or "concept" or "devops" or "data" or "other"
        }}
    ]
}}

Rules:
- critical = explicitly required, mentioned multiple times, or listed under Requirements
- important = clearly expected but not blocking
- nice_to_have = bonus, preferred, or mentioned once lightly
- required_proficiency: critical senior skill = 0.8+, important = 0.6, nice = 0.4
- Extract ALL skills including implied ones
- Normalize names: JS → JavaScript, k8s → Kubernetes
- Order by importance descending
"""
    return call_llm_json(prompt, temperature=0.1)


def parse_resume(resume_text: str) -> dict:
    prompt = f"""You are a resume analyst.

Extract structured skill information from this resume.

RESUME:
---
{resume_text}
---

Return this exact JSON:
{{
    "name": "candidate full name",
    "experience_years": total professional experience as number,
    "education": "highest degree and field",
    "summary": "one sentence describing this candidate",
    "skills": [
        {{
            "skill": "concise skill name",
            "claimed_proficiency": 0.0 to 1.0,
            "evidence": "brief reason for this rating",
            "years_used": number or null
        }}
    ]
}}

Proficiency rating guide:
- Mentioned only in skills list → 0.3
- Used in 1 project → 0.45
- Used across multiple projects → 0.6
- Led or architected with it → 0.72
- Expert indicators (published, taught, contributed) → 0.85+
- Be conservative. Do not inflate.

Normalize skill names. Extract everything — explicit and implied.
"""
    return call_llm_json(prompt, temperature=0.1)