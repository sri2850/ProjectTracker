from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config.settings import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: str, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_minutes)
    payload: dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Raises jose.JWTError if invalid/expired.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


# 1. hash the password (cryptocontext)
# 2. verify hash and plan password
# 3. create access token (get subject as user name or email, expiry time)
# (Build the payload dict, and encode with jwt.encode(secret key, algorithm))
# 4. Decode jwt token (using jwt package jwt.decode(payload, secret key, algorithm))
