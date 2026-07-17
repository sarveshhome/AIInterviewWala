"""OAuth providers — Google & LinkedIn token verification."""
from __future__ import annotations

import logging

import httpx

from config.settings import settings
from domain.exceptions import InvalidCredentials
from domain.interfaces.services import IOAuthProvider
from domain.value_objects.value_objects import Provider

logger = logging.getLogger(__name__)


class GoogleOAuthProvider(IOAuthProvider):
    GOOGLE_CERTS_URL = "https://www.googleapis.com/oauth2/v3/certs"

    async def verify(self, token: str) -> dict:
        # Validate id_token via Google tokeninfo endpoint (production-grade uses JWKS + signature).
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get("https://oauth2.googleapis.com/tokeninfo", params={"id_token": token})
        if resp.status_code != 200:
            raise InvalidCredentials()
        data = resp.json()
        if settings.google_client_id and data.get("aud") != settings.google_client_id:
            raise InvalidCredentials()
        return {"sub": data["sub"], "email": data.get("email", ""), "name": data.get("name", "")}


class LinkedInOAuthProvider(IOAuthProvider):
    PROFILE_URL = "https://api.linkedin.com/v2/userinfo"

    async def verify(self, token: str) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(self.PROFILE_URL, headers={"Authorization": f"Bearer {token}"})
        if resp.status_code != 200:
            raise InvalidCredentials()
        data = resp.json()
        return {"sub": data.get("sub", data.get("id", "")),
                "email": data.get("email", ""), "name": data.get("name", "")}


def build_oauth_providers() -> dict[Provider, IOAuthProvider]:
    return {Provider.GOOGLE: GoogleOAuthProvider(), Provider.LINKEDIN: LinkedInOAuthProvider()}