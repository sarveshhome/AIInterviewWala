"""Interview AI service — orchestrates Cohere prompts for interview flows."""
from __future__ import annotations

import json
import logging
from typing import Optional

from domain.interfaces.services import IInterviewAI, ILLMService
from domain.value_objects.value_objects import Feedback, InterviewType, Score
from infrastructure.prompts.prompts import (
    BEHAVIORAL_EVALUATE_PROMPT,
    BEHAVIORAL_FIRST_PROMPT,
    BEHAVIORAL_NEXT_PROMPT,
    CODING_EVALUATE_PROMPT,
    CODING_FIRST_PROMPT,
    CODING_NEXT_PROMPT,
    SYSTEM_DESIGN_EVALUATE_PROMPT,
    SYSTEM_DESIGN_FIRST_PROMPT,
    SYSTEM_DESIGN_NEXT_PROMPT,
    SUMMARY_PROMPT,
    TECHNICAL_EVALUATE_PROMPT,
    TECHNICAL_FIRST_PROMPT,
    TECHNICAL_NEXT_PROMPT,
    VOICE_EVALUATE_PROMPT,
    VOICE_FIRST_PROMPT,
    VOICE_NEXT_PROMPT,
)

logger = logging.getLogger(__name__)

_FIRST = {
    InterviewType.TECHNICAL: TECHNICAL_FIRST_PROMPT,
    InterviewType.CODING: CODING_FIRST_PROMPT,
    InterviewType.BEHAVIORAL: BEHAVIORAL_FIRST_PROMPT,
    InterviewType.SYSTEM_DESIGN: SYSTEM_DESIGN_FIRST_PROMPT,
    InterviewType.VOICE: VOICE_FIRST_PROMPT,
}
_NEXT = {
    InterviewType.TECHNICAL: TECHNICAL_NEXT_PROMPT,
    InterviewType.CODING: CODING_NEXT_PROMPT,
    InterviewType.BEHAVIORAL: BEHAVIORAL_NEXT_PROMPT,
    InterviewType.SYSTEM_DESIGN: SYSTEM_DESIGN_NEXT_PROMPT,
    InterviewType.VOICE: VOICE_NEXT_PROMPT,
}
_EVAL = {
    InterviewType.TECHNICAL: TECHNICAL_EVALUATE_PROMPT,
    InterviewType.CODING: CODING_EVALUATE_PROMPT,
    InterviewType.BEHAVIORAL: BEHAVIORAL_EVALUATE_PROMPT,
    InterviewType.SYSTEM_DESIGN: SYSTEM_DESIGN_EVALUATE_PROMPT,
    InterviewType.VOICE: VOICE_EVALUATE_PROMPT,
}


class CohereInterviewAI(IInterviewAI):
    SYSTEM = "You are AI Interview Coach, a senior FAANG interviewer conducting realistic interviews."

    def __init__(self, llm: ILLMService):
        self._llm = llm

    async def generate_first_question(self, interview_type: InterviewType, technology: Optional[str],
                                      resume_text: Optional[str] = None) -> str:
        prompt = _FIRST[interview_type].format(technology=technology or "general",
                                              resume=resume_text or "Not provided")
        result = await self._llm.complete_json(prompt, schema={"question": "string"}, system=self.SYSTEM)
        return result.get("question", "Tell me about your most challenging project.")

    async def evaluate_answer(self, interview_type: InterviewType, question: str, answer: str,
                               technology: Optional[str] = None, code: Optional[str] = None) -> Feedback:
        prompt = _EVAL[interview_type].format(technology=technology or "general", question=question,
                                               answer=answer or "(no text answer)", code=code or "(no code)")
        schema = {
            "score": "number 0-100",
            "mistakes": "string[]",
            "ideal_answer": "string",
            "suggested_improvements": "string[]",
            "follow_up_question": "string",
        }
        result = await self._llm.complete_json(prompt, schema=schema, system=self.SYSTEM)
        return Feedback(
            score=Score(value=min(100, max(0, float(result.get("score", 50))))),
            mistakes=result.get("mistakes", []),
            ideal_answer=result.get("ideal_answer"),
            suggested_improvements=result.get("suggested_improvements", []),
            follow_up_question=result.get("follow_up_question"),
        )

    async def generate_next_question(self, interview_type: InterviewType, technology: Optional[str],
                                      history: list[dict]) -> str:
        prompt = _NEXT[interview_type].format(technology=technology or "general",
                                              history=json.dumps(history[-8:]))
        result = await self._llm.complete_json(prompt, schema={"question": "string"}, system=self.SYSTEM)
        return result.get("question", "What would you do differently next time?")

    async def summarize_interview(self, interview_type: InterviewType, qa_pairs: list[dict]) -> dict:
        prompt = SUMMARY_PROMPT.format(interview_type=interview_type.value,
                                       qa=json.dumps(qa_pairs))
        schema = {"overall_score": "number 0-100", "summary": "string",
                  "strong_areas": "string[]", "weak_areas": "string[]"}
        return await self._llm.complete_json(prompt, schema=schema, system=self.SYSTEM)