from fastapi import FastAPI, Depends
from app.api.v1.router import router as api_router
from app.db.session import engine
from app.db.base import Base
from typing import Annotated


async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: (add cleanup if needed)


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(api_router)
    return app


app = create_app()
