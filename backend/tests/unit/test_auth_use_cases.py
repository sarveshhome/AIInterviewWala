"""Unit tests for auth use cases (no DB, no LLM)."""
import pytest

from application.commands.auth_commands import LoginUseCase, RegisterUseCase, RefreshTokenUseCase
from application.dtos.dtos import LoginRequest, RegisterRequest, RefreshRequest
from domain.exceptions import DuplicateEntity, InvalidCredentials


@pytest.mark.asyncio
async def test_register_creates_user_and_issues_token(uow, auth, issuer):
    uc = RegisterUseCase(uow, auth, issuer)
    token = await uc.execute(RegisterRequest(email="a@b.com", password="secret123", full_name="A B"))
    assert token.access_token.startswith("access:")
    assert await uow.users.get_by_email("a@b.com")


@pytest.mark.asyncio
async def test_register_duplicate_raises(uow, auth, issuer):
    uc = RegisterUseCase(uow, auth, issuer)
    await uc.execute(RegisterRequest(email="a@b.com", password="secret123", full_name="A B"))
    with pytest.raises(DuplicateEntity):
        await uc.execute(RegisterRequest(email="a@b.com", password="secret123", full_name="A B"))


@pytest.mark.asyncio
async def test_login_success(uow, auth, issuer):
    await RegisterUseCase(uow, auth, issuer).execute(
        RegisterRequest(email="a@b.com", password="secret123", full_name="A B"))
    token = await LoginUseCase(uow, auth, issuer).execute(LoginRequest(email="a@b.com", password="secret123"))
    assert token.access_token.startswith("access:")


@pytest.mark.asyncio
async def test_login_wrong_password_raises(uow, auth, issuer):
    await RegisterUseCase(uow, auth, issuer).execute(
        RegisterRequest(email="a@b.com", password="secret123", full_name="A B"))
    with pytest.raises(InvalidCredentials):
        await LoginUseCase(uow, auth, issuer).execute(LoginRequest(email="a@b.com", password="wrongpass"))


@pytest.mark.asyncio
async def test_refresh_flow(uow, auth, issuer):
    token = await RegisterUseCase(uow, auth, issuer).execute(
        RegisterRequest(email="a@b.com", password="secret123", full_name="A B"))
    new_token = await RefreshTokenUseCase(uow, auth, issuer).execute(token.refresh_token)
    assert new_token.access_token.startswith("access:")