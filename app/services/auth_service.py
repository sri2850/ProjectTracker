from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password
from app.repositories.user import get_user_by_name


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_name(db, username)
    print(user)
    if not user:
        return None
    if not user.is_active:
        return None
    if not await verify_password(password, user.hashed_password):
        return None
    return user
