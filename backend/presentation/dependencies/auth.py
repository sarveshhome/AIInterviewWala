"""FastAPI dependencies — request-scoped resolution of current user & use cases."""
from __future__ import annotations

from uuid import UUID

from fastapi import Depends, Header, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from domain.entities.entities import User
from domain.exceptions import InvalidToken, Unauthorized
from domain.value_objects.value_objects import Provider
from infrastructure.di.container import get_container

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
) -> User:
    """Resolve the current user from a Bearer JWT."""
    container = get_container()
    auth = container.auth()
    token = creds.credentials if creds else None
    if not token:
        raise Unauthorized("missing bearer token")
    try:
        payload = auth.decode_token(token)
        if payload.get("type") != "access":
            raise Unauthorized("not an access token")
        user_id = UUID(payload["sub"])
    except InvalidToken as e:
        raise Unauthorized(str(e)) from e
    async with container.uow() as uow:
        user = await uow.users.get_by_id(user_id)
    if not user or not user.is_active:
        raise Unauthorized("user not found or inactive")
    return user


async def get_current_user_id(user: User = Depends(get_current_user)) -> UUID:
    return user.id