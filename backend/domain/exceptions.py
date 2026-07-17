"""Domain-level exceptions — business-rule violations independent of HTTP."""
from __future__ import annotations


class DomainException(Exception):
    """Base for all domain-level errors."""
    def __init__(self, message: str = "Domain error", code: str = "domain_error"):
        self.message = message
        self.code = code
        super().__init__(message)


class EntityNotFound(DomainException):
    def __init__(self, entity: str, id: object):
        super().__init__(f"{entity} '{id}' not found", code="entity_not_found")


class DuplicateEntity(DomainException):
    def __init__(self, entity: str, key: str):
        super().__init__(f"{entity} already exists for {key}", code="duplicate_entity")


class InvalidCredentials(DomainException):
    def __init__(self):
        super().__init__("Invalid email or password", code="invalid_credentials")


class TokenExpired(DomainException):
    def __init__(self):
        super().__init__("Token has expired", code="token_expired")


class InvalidToken(DomainException):
    def __init__(self, reason: str = "invalid"):
        super().__init__(f"Invalid token: {reason}", code="invalid_token")


class Unauthorized(DomainException):
    def __init__(self, reason: str = "unauthorized"):
        super().__init__(reason, code="unauthorized")


class Forbidden(DomainException):
    def __init__(self, reason: str = "forbidden"):
        super().__init__(reason, code="forbidden")


class BusinessRuleViolation(DomainException):
    def __init__(self, rule: str):
        super().__init__(f"Business rule violated: {rule}", code="business_rule")


class LLMServiceError(DomainException):
    def __init__(self, reason: str = "LLM call failed"):
        super().__init__(reason, code="llm_error")


class RateLimited(DomainException):
    def __init__(self, detail: str = "Too many requests"):
        super().__init__(detail, code="rate_limited")