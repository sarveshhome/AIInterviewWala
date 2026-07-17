"""Career AI service — resume analysis, learning roadmap, career coach."""
from __future__ import annotations

import json

from domain.interfaces.services import ICareerAI, ILLMService
from domain.value_objects.value_objects import ATSReport, Score
from infrastructure.prompts.prompts import (
    CAREER_COACH_PROMPT,
    LEARNING_ROADMAP_PROMPT,
    RESUME_ANALYSIS_PROMPT,
)


class CohereCareerAI(ICareerAI):
    SYSTEM = "You are AI Interview Coach's career advisor. Be specific, actionable, and concise."

    def __init__(self, llm: ILLMService):
        self._llm = llm

    async def analyze_resume(self, resume_text: str, target_role: str | None = None) -> ATSReport:
        prompt = RESUME_ANALYSIS_PROMPT.format(resume=resume_text[:8000],
                                               target_role=target_role or "Software Engineer")
        schema = {
            "ats_score": "number 0-100",
            "missing_skills": "string[]",
            "strong_areas": "string[]",
            "weak_areas": "string[]",
            "recommended_improvements": "string[]",
        }
        result = await self._llm.complete_json(prompt, schema=schema, system=self.SYSTEM)
        return ATSReport(
            score=Score(value=min(100, max(0, float(result.get("ats_score", 0))))),
            missing_skills=result.get("missing_skills", []),
            strong_areas=result.get("strong_areas", []),
            weak_areas=result.get("weak_areas", []),
            recommended_improvements=result.get("recommended_improvements", []),
        )

    async def build_learning_roadmap(self, profile: dict, gaps: list[str], goal_role: str) -> dict:
        prompt = LEARNING_ROADMAP_PROMPT.format(profile=json.dumps(profile), gaps=", ".join(gaps) or "general gaps", goal_role=goal_role)
        schema = {"title": "string", "est_total_weeks": "number",
                  "milestones": [{"title": "string", "topics": "string[]", "resources": "string[]", "est_weeks": "number"}]}
        return await self._llm.complete_json(prompt, schema=schema, system=self.SYSTEM)

    async def career_coach(self, profile: dict, question: str) -> dict:
        prompt = CAREER_COACH_PROMPT.format(profile=json.dumps(profile), question=question)
        schema = {"answer": "string", "action_items": "string[]", "resources": "string[]"}
        return await self._llm.complete_json(prompt, schema=schema, system=self.SYSTEM)