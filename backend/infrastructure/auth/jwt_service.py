"""JWT auth service + token issuer — implements IAuthService & ITokenIssuer."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from config.settings import settings
from domain.exceptions import InvalidToken, TokenExpired
from domain.interfaces.services import IAuthService, ITokenIssuer
from domain.value_objects.value_objects import Token


class JWTAuthService(IAuthService):
    def __init__(self):
        self._secret = settings.jwt_secret
        self._algo = settings.jwt_algorithm
        self._pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, plain: str) -> str:
        return self._pwd.hash(plain)

    def verify_password(self, plain: str, hashed: str) -> bool:
        try:
            return self._pwd.verify(plain, hashed)
        except Exception:  # noqa: BLE001
            return False

    def create_access_token(self, subject: str, extra: Optional[dict] = None) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": subject,
            "iat": now,
            "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
            "type": "access",
        }
        if extra:
            payload.update(extra)
        return jwt.encode(payload, self._secret, algorithm=self._algo)

    def create_refresh_token(self, subject: str) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": subject,
            "iat": now,
            "exp": now + timedelta(days=settings.refresh_token_expire_days),
            "type": "refresh",
        }
        return jwt.encode(payload, self._secret, algorithm=self._algo)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self._secret, algorithms=[self._algo])
        except jwt.ExpiredSignatureError as e:
            raise TokenExpired() from e
        except JWTError as e:
            raise InvalidToken(str(e)) from e


class TokenIssuer(ITokenIssuer):
    def __init__(self, auth: IAuthService):
        self._auth = auth

    async def issue(self, user_id: str, email: str) -> Token:
        return Token(
            access_token=self._auth.create_access_token(user_id, extra={"email": email}),
            refresh_token=self._auth.create_refresh_token(user_id),
            expires_in=settings.access_token_expire_minutes * 60,
        )