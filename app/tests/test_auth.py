# tests/test_auth.py
import pytest

from app.core.security import (
    create_access_token,
    hash_password,
)  # whatever you named it
from app.db.models.project import Project
from app.db.models.user import User
from app.tests.conftest import login_and_get_token


@pytest.mark.asyncio
async def test_login__valid_credentials__returns_token(client, db_session):
    # Arrange: create a user
    user = User(
        username="alice",
        email="a@b.com",
        hashed_password=await hash_password("pass123"),
    )
    db_session.add(user)
    await db_session.commit()

    # Act
    await db_session.refresh(user)
    resp = await client.post(
        "/api/v1/auth/login",
        data={"username": str(user.id), "password": "pass123"},
    )

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data.get("token_type") == "bearer"


@pytest.mark.asyncio
async def test_protected__missing_token__returns_401(client):
    resp = await client.get("/api/v1/projects/")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_protected__valid_token__returns_200(client, db_session):
    # Arrange user
    user = User(
        username="alice",
        email="a@b.com",
        hashed_password=await hash_password("pass123"),
    )
    db_session.add(user)
    await db_session.commit()

    # Login to get token
    login = await client.post(
        "/api/v1/auth/login",
        data={"username": str(user.id), "password": "pass123"},
    )
    token = login.json()["access_token"]

    # Act
    resp = await client.get(
        "/api/v1/projects/", headers={"Authorization": f"Bearer {token}"}
    )

    # Assert
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_expired_token_returns_401(client, db_session):
    user = User(
        username="sri",
        email="a@b.com",
        hashed_password=await hash_password("pass123"),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # Make an already-expired token (exp in the past)
    token = create_access_token(subject=str(user.id), expires_minutes=-1)

    # Act
    resp = await client.get(
        "/api/v1/projects/", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 401
    body = resp.json()
    assert body["error"]["code"] == "token_expired"


@pytest.mark.asyncio
async def test_user_cannot_read_other_users_project(client, db_session):
    # Arrange: create 2 users and a project for user1
    user1 = User(
        username="user1",
        email="user1@example.com",
        hashed_password=await hash_password("pass123"),
    )
    db_session.add(user1)
    await db_session.commit()

    user2 = User(
        username="user2",
        email="user2@example.com",
        hashed_password=await hash_password("pass123"),
    )
    db_session.add(user2)
    await db_session.commit()

    project = Project(name="Project 1", created_by=user1.id)
    db_session.add(project)
    await db_session.commit()

    # Act: user2 tries to access user1's project
    await db_session.refresh(user2)
    # token = create_access_token(subject=str(user2.id), expires_minutes=10)
    token = await login_and_get_token(client, user2.id, "pass123")
    print(token)
    resp = await client.get(
        f"/api/v1/projects/{project.id}", headers={"Authorization": f"Bearer {token}"}
    )
    print(resp.json())

    # Assert
    assert resp.status_code == 403
    body = resp.json()
    assert body["error"]["code"] == "forbidden"


@pytest.mark.asyncio
async def test_unauthenticated_access_returns_401(client, db_session):
    user1 = User(
        username="user1",
        email="user1@example.com",
        hashed_password=await hash_password("pass123"),
    )
    db_session.add(user1)
    await db_session.commit()
    project = Project(name="project1", created_by=user1.id)
    db_session.add(project)
    await db_session.commit()

    resp = await client.get(f"/api/v1/projects/{project.id}")
    assert resp.status_code == 401
