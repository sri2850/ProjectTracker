from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1.router import router as api_router
from app.db.session import engine
from app.db.base import Base

from app.services.errors import (
    DomainError,
    NotFound,
    Conflict,
    Forbidden,
    Unauthorized,
    Unprocessable,
)


def _error_payload(exc: DomainError) -> dict:
    return {
        "error": {
            "code": exc.code,
            "message": exc.message,
            "details": exc.details or {},
        }
    }


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFound)
    async def not_found_handler(request: Request, exc: NotFound):
        return JSONResponse(status_code=404, content=_error_payload(exc))

    @app.exception_handler(Conflict)
    async def conflict_handler(request: Request, exc: Conflict):
        return JSONResponse(status_code=409, content=_error_payload(exc))

    @app.exception_handler(Forbidden)
    async def forbidden_handler(request: Request, exc: Forbidden):
        return JSONResponse(status_code=403, content=_error_payload(exc))

    @app.exception_handler(Unauthorized)
    async def unauthorized_handler(request: Request, exc: Unauthorized):
        return JSONResponse(status_code=401, content=_error_payload(exc))

    @app.exception_handler(Unprocessable)
    async def unprocessable_handler(request: Request, exc: Unprocessable):
        return JSONResponse(status_code=422, content=_error_payload(exc))

    # Optional safety net: if you want ALL DomainError mapped to 422 by default
    @app.exception_handler(DomainError)
    async def domain_error_fallback(request: Request, exc: DomainError):
        return JSONResponse(status_code=422, content=_error_payload(exc))


async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: (add cleanup if needed)


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    add_exception_handlers(app)
    app.include_router(api_router)
    return app


app = create_app()
