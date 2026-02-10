import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.base import Base
from app.dependencies.deps import get_db
from app.main import app

TEST_DB_URL = "sqlite+aiosqlite:///./test_db.sqlite3"


@pytest.fixture(scope="session")
def engine():
    return create_async_engine(TEST_DB_URL, echo=True)


@pytest.fixture(scope="session")
def SessionLocal(engine):
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture(scope="function")
async def db_session(engine, SessionLocal):
    # Hard isolation approach for SQLite: recreate schema per test.
    # (Later we can optimize with transactions/savepoints, but not today.)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession):
    # Override get_db so the app uses our per-test session.
    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
