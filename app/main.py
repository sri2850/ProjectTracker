from fastapi import FastAPI

from app.api.v1.router import router as api_router
from app.core.exception_handlers import register_exception_handlers


async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    register_exception_handlers(app)
    app.include_router(api_router)
    return app


app = create_app()
