from fastapi import FastAPI
from app.core.exception_handlers import register_exception_handlers
from app.api.v1.router import router as api_router
from app.db.session import engine
from app.db.base import Base


async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: (add cleanup if needed)


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    register_exception_handlers(app)
    app.include_router(api_router)
    return app


app = create_app()
