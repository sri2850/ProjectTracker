import logging

import redis.asyncio as redis
from fastapi import FastAPI

from app.api.v1.router import router as api_router
from app.core.exception_handlers import register_exception_handlers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
)


async def lifespan(app: FastAPI):
    app.state.redis = redis.from_url(
        "redis://localhost:6379/0",
        decode_responses=True,
    )
    yield
    await app.state.redis.close()
    await app.state.redis.connection_pool.disconnect()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    register_exception_handlers(app)
    app.include_router(api_router)
    return app


app = create_app()
