from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose.exceptions import ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.dependencies.deps import get_db
from app.repositories.user import get_user_by_id
from app.services.errors import (
    InactiveUser,
    InvalidToken,
    MissingToken,
    TokenExpired,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    if not token:
        raise MissingToken(message="Token is missing")
    try:
        payload = decode_access_token(token)
    except ExpiredSignatureError as e:
        raise TokenExpired(message="Expired token") from e
    except JWTError as e:
        raise InvalidToken(message="Invalid token") from e
    subject = payload.get("sub")
    try:
        user_id = int(subject)
    except (TypeError, ValueError) as e:
        raise InvalidToken() from e
    user = await get_user_by_id(db, user_id)
    if not user:
        raise InvalidToken()
    if not user.is_active:
        raise InactiveUser(message="user is inactive")
    return user
