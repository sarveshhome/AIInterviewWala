"""Auth router — login, register, oauth, refresh."""
from __future__ import annotations

from fastapi import APIRouter, Depends, status

from application.dtos.dtos import (
    LoginRequest, OAuthLoginRequest, RefreshRequest, RegisterRequest, TokenResponse,
)
from infrastructure.di.container import get_container

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(req: RegisterRequest):
    return await get_container().register_use_case().execute(req)


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    return await get_container().login_use_case().execute(req)


@router.post("/oauth", response_model=TokenResponse)
async def oauth_login(req: OAuthLoginRequest):
    return await get_container().oauth_login_use_case().execute(req)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(req: RefreshRequest):
    return await get_container().refresh_use_case().execute(req.refresh_token)