"""
Unified LLM Client
Uses the new google-genai SDK (google.generativeai is deprecated).
Gemini primary → Groq backup → clear error if both fail.
"""
import json
import time
from google import genai
from google.genai import types
from groq import Groq
import config

# ── Lazy clients ───────────────────────────────────────────────────
_gemini_client = None
_groq_client   = None


def _get_gemini():
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = genai.Client(api_key=config.GEMINI_API_KEY)
    return _gemini_client


def _get_groq():
    global _groq_client
    if _groq_client is None:
        _groq_client = Groq(api_key=config.GROQ_API_KEY)
    return _groq_client


# ── Core call ──────────────────────────────────────────────────────
def call_llm(prompt: str,
             temperature: float = config.TEMPERATURE,
             expect_json: bool = False,
             retries: int = 2) -> str:
    """
    Send a prompt to the configured LLM. Returns raw text.
    Retries on transient errors. Falls back to backup provider.
    """
    if expect_json:
        prompt += (
            "\n\nCRITICAL: Return ONLY valid JSON. "
            "No markdown. No code fences. No explanation. Pure JSON only."
        )

    last_err = None

    for attempt in range(retries + 1):
        try:
            if config.LLM_PROVIDER == "gemini":
                client   = _get_gemini()
                response = client.models.generate_content(
                    model    = config.GEMINI_MODEL,
                    contents = prompt,
                    config   = types.GenerateContentConfig(
                        temperature       = temperature,
                        max_output_tokens = config.MAX_TOKENS,
                    ),
                )
                return response.text.strip()

            elif config.LLM_PROVIDER == "groq":
                client   = _get_groq()
                response = client.chat.completions.create(
                    model       = config.GROQ_MODEL,
                    messages    = [{"role": "user", "content": prompt}],
                    temperature = temperature,
                    max_tokens  = config.MAX_TOKENS,
                )
                return response.choices[0].message.content.strip()

            else:
                raise ValueError(f"Unknown provider: {config.LLM_PROVIDER}")

        except Exception as e:
            last_err = e
            if attempt < retries:
                time.sleep(attempt + 1)
                continue

    # ── Fallback to other provider ─────────────────────────────────
    try:
        if config.LLM_PROVIDER == "gemini" and config.GROQ_API_KEY:
            client   = _get_groq()
            response = client.chat.completions.create(
                model       = config.GROQ_MODEL,
                messages    = [{"role": "user", "content": prompt}],
                temperature = temperature,
                max_tokens  = config.MAX_TOKENS,
            )
            return response.choices[0].message.content.strip()

        elif config.LLM_PROVIDER == "groq" and config.GEMINI_API_KEY:
            client   = _get_gemini()
            response = client.models.generate_content(
                model    = config.GEMINI_MODEL,
                contents = prompt,
                config   = types.GenerateContentConfig(
                    temperature       = temperature,
                    max_output_tokens = config.MAX_TOKENS,
                ),
            )
            return response.text.strip()

    except Exception as e2:
        raise RuntimeError(
            f"Both providers failed.\nPrimary: {last_err}\nFallback: {e2}"
        )

    raise RuntimeError(f"LLM call failed: {last_err}")


# ── JSON helpers ───────────────────────────────────────────────────
def parse_json(text: str) -> dict:
    """Robustly parse JSON from LLM response."""
    cleaned = text.strip()

    # Strip code fences
    if "```" in cleaned:
        lines  = cleaned.split("\n")
        inner  = []
        inside = False
        for line in lines:
            if line.strip().startswith("```"):
                inside = not inside
                continue
            if inside:
                inner.append(line)
        if inner:
            cleaned = "\n".join(inner).strip()

    # Direct parse
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Find JSON object
    s = cleaned.find("{")
    e = cleaned.rfind("}") + 1
    if s != -1 and e > s:
        try:
            return json.loads(cleaned[s:e])
        except json.JSONDecodeError:
            pass

    # Find JSON array
    s = cleaned.find("[")
    e = cleaned.rfind("]") + 1
    if s != -1 and e > s:
        try:
            return json.loads(cleaned[s:e])
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Cannot parse JSON from: {text[:300]}")


def call_llm_json(prompt: str,
                  temperature: float = config.TEMPERATURE) -> dict:
    """Call LLM and return parsed JSON dict directly."""
    raw = call_llm(prompt, temperature=temperature, expect_json=True)
    return parse_json(raw)