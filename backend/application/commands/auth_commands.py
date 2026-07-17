"""Use cases — Commands (writes). One use case per business operation.

Each use case depends only on abstractions (UoW + service interfaces),
keeping the application layer framework-agnostic and testable in isolation.
"""
from __future__ import annotations

from typing import Optional
from uuid import UUID

from application.dtos.dtos import (
    LoginRequest,
    OAuthLoginRequest,
    RegisterRequest,
    TokenResponse,
)
from application.unit_of_work import IUnitOfWork
from domain.entities.entities import User
from domain.exceptions import DuplicateEntity, InvalidCredentials
from domain.interfaces.services import IAuthService, IOAuthProvider, ITokenIssuer
from domain.value_objects.value_objects import Provider


class RegisterUseCase:
    def __init__(self, uow: IUnitOfWork, auth: IAuthService, issuer: ITokenIssuer):
        self._uow = uow
        self._auth = auth
        self._issuer = issuer

    async def execute(self, req: RegisterRequest) -> TokenResponse:
        async with self._uow as uow:
            existing = await uow.users.get_by_email(req.email)
            if existing:
                raise DuplicateEntity("User", req.email)
            user = User(
                email=req.email,
                full_name=req.full_name,
                hashed_password=self._auth.hash_password(req.password),
                provider=Provider.EMAIL,
                target_role=req.target_role,
                experience_years=req.experience_years,
            )
            await uow.users.add(user)
        return await self._issuer.issue(str(user.id), user.email)


class LoginUseCase:
    def __init__(self, uow: IUnitOfWork, auth: IAuthService, issuer: ITokenIssuer):
        self._uow = uow
        self._auth = auth
        self._issuer = issuer

    async def execute(self, req: LoginRequest) -> TokenResponse:
        async with self._uow as uow:
            user = await uow.users.get_by_email(req.email)
            if not user or not user.hashed_password:
                raise InvalidCredentials()
            if not self._auth.verify_password(req.password, user.hashed_password):
                raise InvalidCredentials()
            if not user.is_active:
                raise InvalidCredentials()
        return await self._issuer.issue(str(user.id), user.email)


class OAuthLoginUseCase:
    """Login/register via Google or LinkedIn OAuth."""
    def __init__(self, uow: IUnitOfWork, providers: dict[Provider, IOAuthProvider], issuer: ITokenIssuer):
        self._uow = uow
        self._providers = providers
        self._issuer = issuer

    async def execute(self, req: OAuthLoginRequest) -> TokenResponse:
        provider = self._providers.get(req.provider)
        if not provider:
            raise InvalidCredentials()
        profile = await provider.verify(req.token)
        sub = profile["sub"]
        async with self._uow as uow:
            user = await uow.users.get_by_provider_subject(req.provider.value, sub)
            if not user:
                user = User(
                    email=profile["email"],
                    full_name=profile.get("name", profile["email"]),
                    provider=req.provider,
                    provider_subject=sub,
                    is_verified=True,
                )
                await uow.users.add(user)
        return await self._issuer.issue(str(user.id), user.email)


class RefreshTokenUseCase:
    def __init__(self, uow: IUnitOfWork, auth: IAuthService, issuer: ITokenIssuer):
        self._uow = uow
        self._auth = auth
        self._issuer = issuer

    async def execute(self, refresh_token: str) -> TokenResponse:
        payload = self._auth.decode_token(refresh_token)
        if payload.get("type") != "refresh":
            from domain.exceptions import InvalidToken
            raise InvalidToken("not a refresh token")
        user_id = payload.get("sub")
        async with self._uow as uow:
            user = await uow.users.get_by_id(UUID(user_id))
            if not user or not user.is_active:
                raise InvalidCredentials()
        return await self._issuer.issue(str(user.id), user.email)