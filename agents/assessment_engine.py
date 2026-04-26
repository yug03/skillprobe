"""
Assessment Engine — the core CAT state machine.
This is what makes SkillProbe an agent, not a chatbot.

For each skill it:
  - Tracks state (difficulty, confidence, history)
  - Generates adaptive questions
  - Decides when to stop
  - Moves to next skill autonomously
"""
from models.llm_client import call_llm_json, call_llm
from agents.answer_evaluator import evaluate
import config


class SkillState:
    """Tracks assessment state for one skill."""

    def __init__(self, skill: str, claimed: float,
                 required: float, importance: str):
        self.skill      = skill
        self.claimed    = claimed
        self.required   = required
        self.importance = importance

        # Starting difficulty based on claimed proficiency
        if claimed >= 0.70:
            self.difficulty = 3
        elif claimed >= 0.40:
            self.difficulty = 2
        else:
            self.difficulty = 1

        self.history:    list[dict] = []   # {question, answer, difficulty, score, quality, reasoning}
        self.confidence: float      = 0.0
        self.is_done:    bool       = False
        self.proficiency:float      = 0.0
        self.observation:str        = ""
        self.max_diff:   int        = 1

    # ── After each answer ──────────────────────────────────────────
    def record(self, question: str, answer: str,
               difficulty: int, evaluation: dict):
        score   = evaluation.get("score", 0.0)
        quality = evaluation.get("quality", "weak")

        self.history.append({
            "question":   question,
            "answer":     answer,
            "difficulty": difficulty,
            "score":      score,
            "quality":    quality,
            "reasoning":  evaluation.get("reasoning", ""),
            "covered":    evaluation.get("key_points_covered", []),
            "missed":     evaluation.get("key_points_missed", []),
        })
        self.max_diff = max(self.max_diff, difficulty)

        # Adapt difficulty
        if quality == "strong":
            self.difficulty = min(4, difficulty + 1)
        elif quality == "moderate":
            self.difficulty = difficulty
        else:
            self.difficulty = max(1, difficulty - 1)

        self._update_confidence()
        self._check_stop()

    def _update_confidence(self):
        n = len(self.history)
        if n == 0:
            self.confidence = 0.0
            return
        base = min(n / config.MAX_QUESTIONS, 0.70)
        scores = [h["score"] for h in self.history]
        mean   = sum(scores) / len(scores)
        var    = sum((s - mean) ** 2 for s in scores) / len(scores)
        consistency = max(0.0, 1.0 - var * 4)
        self.confidence = round(min(base + consistency * 0.30, 1.0), 3)

    def _check_stop(self):
        n = len(self.history)
        if n >= config.MAX_QUESTIONS:
            self.is_done = True
        elif n >= config.MIN_QUESTIONS and self.confidence >= config.CONFIDENCE_THRESHOLD:
            self.is_done = True
        if self.is_done:
            self._finalise()

    def _finalise(self):
        """Compute final proficiency using weighted score + difficulty ceiling."""
        if not self.history:
            self.proficiency = 0.0
            return
        w_sum  = sum(h["score"] * h["difficulty"] for h in self.history)
        w_tot  = sum(h["difficulty"]               for h in self.history)
        raw    = w_sum / w_tot if w_tot else 0.0
        ceil   = self.max_diff / 4.0
        self.proficiency = round(min(raw * ceil * 1.3, 1.0), 3)

    def to_dict(self) -> dict:
        return {
            "skill":                self.skill,
            "claimed_proficiency":  self.claimed,
            "required_proficiency": self.required,
            "assessed_proficiency": self.proficiency,
            "importance":           self.importance,
            "confidence":           self.confidence,
            "questions_asked":      len(self.history),
            "max_difficulty":       self.max_diff,
            "max_difficulty_label": config.DIFFICULTY_LEVELS.get(self.max_diff, ""),
            "observation":          self.observation,
            "history":              self.history,
            "is_done":              self.is_done,
        }


class AssessmentEngine:
    """
    Orchestrates the full adaptive assessment across all skills.
    This is the agent brain.
    """

    def __init__(self, skill_map: dict, jd_parsed: dict, resume_parsed: dict):
        self.skill_map     = skill_map
        self.jd_parsed     = jd_parsed
        self.resume_parsed = resume_parsed
        self.queue         = skill_map.get("assessment_queue", [])
        self.index         = 0
        self.states:  dict[str, SkillState] = {}
        self.done:    bool = False
        self._init_states()

    def _init_states(self):
        matched = {s["skill"]: s for s in self.skill_map.get("matched_skills", [])}
        missing = {s["skill"]: s for s in self.skill_map.get("missing_skills", [])}

        for skill in self.queue:
            if skill in matched:
                s = matched[skill]
                self.states[skill] = SkillState(
                    skill      = skill,
                    claimed    = s.get("claimed_proficiency", 0.0),
                    required   = s.get("required_proficiency", 0.5),
                    importance = s.get("importance", "important"),
                )
            elif skill in missing:
                s = missing[skill]
                self.states[skill] = SkillState(
                    skill      = skill,
                    claimed    = 0.0,
                    required   = s.get("required_proficiency", 0.5),
                    importance = s.get("importance", "important"),
                )

    # ── Navigation ─────────────────────────────────────────────────
    def current_skill(self) -> str | None:
        while self.index < len(self.queue):
            skill = self.queue[self.index]
            state = self.states.get(skill)
            if state and state.is_done:
                self.index += 1
                continue
            return skill
        self.done = True
        return None

    def current_state(self) -> SkillState | None:
        skill = self.current_skill()
        return self.states.get(skill) if skill else None

    def advance(self):
        self.index += 1
        if self.index >= len(self.queue):
            self.done = True

    # ── Question Generation ────────────────────────────────────────
    def generate_question(self) -> dict | None:
        state = self.current_state()
        if state is None:
            return None

        difficulty = state.difficulty
        skill      = state.skill
        prev_qs    = [h["question"] for h in state.history]
        prev_block = ""
        if prev_qs:
            prev_block = "\n\nDo NOT repeat or rephrase these already-asked questions:\n" + \
                         "\n".join(f"- {q}" for q in prev_qs)

        prompt = f"""You are a technical assessor running a skill interview.

Role being hired for: {self.jd_parsed.get('title', 'Technical Role')}
Skill being assessed: {skill}
Difficulty: Level {difficulty} — {config.DIFFICULTY_LEVELS[difficulty]}
({config.DIFFICULTY_DESCRIPTIONS[difficulty]})
Candidate claimed proficiency: {state.claimed:.0%}
{prev_block}

Generate exactly ONE question at this difficulty level.

Level guide:
- Level 1: Ask for definition, explanation, or core concept
- Level 2: Ask how they would implement or use it in practice
- Level 3: Give a realistic scenario or problem, ask them to solve it
- Level 4: Ask about design decisions, trade-offs, or failure modes

Rules:
- ONE question only
- Answerable in 3-6 sentences
- No multiple choice
- Natural, professional tone — not robotic
- Must genuinely probe depth at Level {difficulty}

Return this exact JSON:
{{
    "question": "the question text",
    "expected_key_points": ["point a good answer would cover"]
}}
"""
        result = call_llm_json(prompt, temperature=0.45)
        return {
            "skill":           skill,
            "question":        result["question"],
            "difficulty":      difficulty,
            "difficulty_label":config.DIFFICULTY_LEVELS[difficulty],
            "question_number": len(state.history) + 1,
            "skill_number":    self.index + 1,
            "total_skills":    len(self.queue),
            "expected_depth":  result.get("expected_key_points", []),
        }

    # ── Answer Submission ──────────────────────────────────────────
    def submit_answer(self, question: str, answer: str,
                      difficulty: int) -> dict:
        """
        Evaluate answer, record it, return result dict.
        Caller checks result['skill_done'] and result['assessment_done'].
        """
        state = self.current_state()
        if state is None:
            return {"assessment_done": True}

        evaluation = evaluate(
            skill      = state.skill,
            question   = question,
            answer     = answer,
            difficulty = difficulty,
            role_title = self.jd_parsed.get("title", ""),
        )

        state.record(question, answer, difficulty, evaluation)

        skill_done = state.is_done
        if skill_done:
            # Generate observation
            state.observation = self._observe(state)
            self.advance()

        return {
            "evaluation":      evaluation,
            "skill_done":      skill_done,
            "assessment_done": self.done,
            "skill_summary":   state.to_dict() if skill_done else None,
            "next_skill":      self.current_skill(),
        }

    def _observe(self, state: SkillState) -> str:
      """Generate observation — skipped during assessment to save tokens.
      Observations are generated in bulk by gap_analyzer instead."""
      scores = [h["score"] for h in state.history]
      avg    = sum(scores) / len(scores) if scores else 0
      max_d  = state.max_diff
  
      if avg >= 0.8 and max_d >= 3:
          return "Strong demonstrated proficiency across difficulty levels."
      elif avg >= 0.6:
          return "Solid foundational knowledge with some gaps at advanced levels."
      elif avg >= 0.4:
          return "Partial understanding demonstrated. Core concepts present but depth is limited."
      else:
          return "Limited demonstrated proficiency. Foundational study recommended."

Skill: {state.skill}
Claimed: {state.claimed:.0%} | Assessed: {state.proficiency:.0%}
Max difficulty reached: Level {state.max_diff}

Answer quality history:
{history_lines}

Examples of good observations:
- "Solid conceptual understanding but practical implementation knowledge was surface-level."
- "Stronger than the resume suggests — handled architecture-level questions with clarity."
- "Foundational knowledge is present; deeper scenario-based experience appears limited."

Return ONLY the observation sentence(s). No JSON. No labels.
"""
        return call_llm(prompt, temperature=0.3)

    # ── Final Results ──────────────────────────────────────────────
    def get_results(self) -> list[dict]:
        results = []
        for skill in self.queue:
            state = self.states.get(skill)
            if state:
                if not state.is_done:
                    state._finalise()
                results.append(state.to_dict())
        return results
