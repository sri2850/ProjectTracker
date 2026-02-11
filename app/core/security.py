from datetime import UTC, datetime, timedelta

import anyio
import anyio.to_thread
from jose import jwt
from passlib.context import CryptContext

from app.core.config.settings import settings

secret_key = settings.SECRET_KEY
algorithm = "HS256"
access_token_expire_mintes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password_sync(password):
    return pwd_context.hash(password)


async def hash_password(password):
    return await anyio.to_thread.run_sync(hash_password_sync, password)


def verify_password_sync(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def verify_password(plain_password, hashed_password):
    return await anyio.to_thread.run_sync(
        verify_password_sync, plain_password, hashed_password
    )


def create_access_token(subject, expires_minutes=access_token_expire_mintes):
    now = datetime.now(UTC)
    expire = now + timedelta(minutes=expires_minutes)
    payload = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    return jwt.encode(payload, secret_key, algorithm)


def decode_access_token(token):
    return jwt.decode(token, secret_key, algorithms=[algorithm])
