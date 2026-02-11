# errors.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(eq=False)
class DomainError(Exception):
    """
    Base domain exception.
    - code: stable machine-readable string
    - message: human-readable safe message
    - details: extra structured info (optional)
    """

    code: str
    message: str
    details: dict[str, Any] | None = None

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


# 404
class NotFound(DomainError):
    def __init__(
        self,
        *,
        message: str = "Resource not found",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(code="not_found", message=message, details=details)


# 409
class Conflict(DomainError):
    def __init__(
        self, *, message: str = "Conflict", details: dict[str, Any] | None = None
    ):
        super().__init__(code="conflict", message=message, details=details)


# 403
class Forbidden(DomainError):
    def __init__(
        self, *, message: str = "Forbidden", details: dict[str, Any] | None = None
    ):
        super().__init__(code="forbidden", message=message, details=details)


# 401 (usually boundary/auth dependency, but available if service must signal it)
class Unauthorized(DomainError):
    def __init__(
        self, *, message: str = "Unauthorized", details: dict[str, Any] | None = None
    ):
        super().__init__(code="unauthorized", message=message, details=details)


# 422 (domain/business rule violation, not Pydantic validation)
class Unprocessable(DomainError):
    def __init__(
        self,
        *,
        message: str = "Unprocessable entity",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(code="unprocessable_entity", message=message, details=details)


# 401 (missing token)
class MissingToken(DomainError):
    def __init__(
        self, *, message="Missing Token", details: dict[str, Any] | None = None
    ):
        super().__init__(code="missing_token", message=message, details=details)


# 401 (token_expired)
class TokenExpired(DomainError):
    def __init__(
        self, *, message="Token Expired", details: dict[str, Any] | None = None
    ):
        super().__init__(code="token_expired", message=message, details=details)


# 401 (invalid_token)
class InvalidToken(DomainError):
    def __init__(
        self, *, message="Invalid Token", details: dict[str, Any] | None = None
    ):
        super().__init__(code="invalid_token", message=message, details=details)


# 401 (invalid_credentials)
class InvalidCredentials(DomainError):
    def __init__(
        self, *, message="Invalid Credentials", details: dict[str, Any] | None = None
    ):
        super().__init__(code="invalid_credentials", message=message, details=details)


# 401 (inactive_user)
class InactiveUser(DomainError):
    def __init__(
        self, *, message="Inactive User", details: dict[str, Any] | None = None
    ):
        super().__init__(code="inactive_user", message=message, details=details)
