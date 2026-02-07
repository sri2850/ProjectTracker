# app/api/exception_handlers.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.services.errors import (
    DomainError,
    NotFound,
    Conflict,
    Forbidden,
    Unauthorized,
    Unprocessable,
)


def _error_payload(code: str, message: str, details: dict | None = None) -> dict:
    return {"error": {"code": code, "message": message, "details": details or {}}}


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFound)
    async def _(request: Request, exc: NotFound):
        return JSONResponse(_error_payload(exc.code, exc.message, exc.details), 404)

    @app.exception_handler(Conflict)
    async def _(request: Request, exc: Conflict):
        return JSONResponse(_error_payload(exc.code, exc.message, exc.details), 409)

    @app.exception_handler(Forbidden)
    async def _(request: Request, exc: Forbidden):
        return JSONResponse(_error_payload(exc.code, exc.message, exc.details), 403)

    @app.exception_handler(Unauthorized)
    async def _(request: Request, exc: Unauthorized):
        return JSONResponse(_error_payload(exc.code, exc.message, exc.details), 401)

    @app.exception_handler(Unprocessable)
    async def _(request: Request, exc: Unprocessable):
        return JSONResponse(_error_payload(exc.code, exc.message, exc.details), 422)

    # Normalize framework-origin errors to your format (keeps “consistent error response” true)
    @app.exception_handler(RequestValidationError)
    async def _(request: Request, exc: RequestValidationError):
        return JSONResponse(
            _error_payload(
                "validation_error",
                "Request validation failed",
                {"errors": exc.errors()},
            ),
            422,
        )

    @app.exception_handler(HTTPException)
    async def _(request: Request, exc: HTTPException):
        return JSONResponse(
            _error_payload("http_error", str(exc.detail), {}),
            exc.status_code,
        )

    # Safety net
    @app.exception_handler(DomainError)
    async def _(request: Request, exc: DomainError):
        return JSONResponse(_error_payload(exc.code, exc.message, exc.details), 422)
