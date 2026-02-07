# errors.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


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
    details: Optional[Dict[str, Any]] = None

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


# 404
class NotFound(DomainError):
    def __init__(
        self,
        *,
        message: str = "Resource not found",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(code="not_found", message=message, details=details)


# 409
class Conflict(DomainError):
    def __init__(
        self, *, message: str = "Conflict", details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(code="conflict", message=message, details=details)


# 403
class Forbidden(DomainError):
    def __init__(
        self, *, message: str = "Forbidden", details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(code="forbidden", message=message, details=details)


# 401 (usually boundary/auth dependency, but available if service must signal it)
class Unauthorized(DomainError):
    def __init__(
        self, *, message: str = "Unauthorized", details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(code="unauthorized", message=message, details=details)


# 422 (domain/business rule violation, not Pydantic validation)
class Unprocessable(DomainError):
    def __init__(
        self,
        *,
        message: str = "Unprocessable entity",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(code="unprocessable_entity", message=message, details=details)
