"""Cohere LLM service — implements ILLMService/ICohereService.

Returns structured JSON via Cohere's chat API with a strict JSON instruction.
On parse failure, retries once with a corrective nudge.
"""
from __future__ import annotations

import json
import logging
from typing import Optional

import cohere

from config.settings import settings
from domain.exceptions import LLMServiceError
from domain.interfaces.services import ICohereService

logger = logging.getLogger(__name__)


class CohereService(ICohereService):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self._api_key = api_key or settings.cohere_api_key
        self._model = model or settings.cohere_model
        if not self._api_key:
            logger.warning("COHERE_API_KEY not set — LLM calls will fail at runtime.")
        self._client = cohere.AsyncClientV2(self._api_key) if self._api_key else None

    async def complete(self, prompt: str, system: Optional[str] = None, **kwargs) -> str:
        if not self._client:
            raise LLMServiceError("Cohere client not initialized (missing API key)")
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        try:
            resp = await self._client.chat(model=self._model, messages=messages, **kwargs)
            return resp.message.content[0].text
        except Exception as exc:  # noqa: BLE001
            logger.exception("Cohere complete failed")
            raise LLMServiceError(str(exc)) from exc

    async def complete_json(self, prompt: str, schema: dict, system: Optional[str] = None) -> dict:
        """Force JSON output. Strips code fences; retries once on parse failure."""
        sys_prompt = (system or "") + "\n\nYou MUST respond with a single valid JSON object matching this schema: " + json.dumps(schema) + ". No markdown, no explanation, only JSON."
        raw = await self.complete(prompt, system=sys_prompt)
        try:
            return self._strip_and_parse(raw)
        except json.JSONDecodeError:
            logger.warning("Cohere returned non-JSON, retrying with correction nudge")
            retry_sys = sys_prompt + "\nYour previous response was not valid JSON. Output ONLY the JSON object now."
            raw2 = await self.complete(prompt, system=retry_sys)
            try:
                return self._strip_and_parse(raw2)
            except json.JSONDecodeError as e:
                raise LLMServiceError(f"Cohere returned unparseable JSON: {e}") from e

    @staticmethod
    def _strip_and_parse(raw: str) -> dict:
        text = raw.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())