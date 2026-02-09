# tests/test_projects.py
import pytest

from app.db.models.user import User
from app.core.security import hash_password


async def _login_get_token(client, db_session):
    user = User(
        username="alice",
        email="a@b.com",
        id="1",
        hashed_password=await hash_password("pass123"),
    )
    db_session.add(user)
    await db_session.commit()

    login = await client.post(
        "/api/v1/auth/login",
        data={"username": str(user.id), "password": "pass123"},
    )
    return login.json()["access_token"]


@pytest.mark.asyncio
async def test_projects__create_then_list__shows_created_project(client, db_session):
    token = await _login_get_token(client, db_session)

    # Create
    create = await client.post(
        "/api/v1/projects/",
        json={"name": "proj-1"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create.status_code in (200, 201)

    # List
    lst = await client.get(
        "/api/v1/projects/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert lst.status_code == 200
    data = lst.json()
    assert any(p["name"] == "proj-1" for p in data)
