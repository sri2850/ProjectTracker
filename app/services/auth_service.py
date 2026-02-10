from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password
from app.repositories.user import get_user_by_id


async def authenticate_user(db: AsyncSession, id: int, password: str):
    user = await get_user_by_id(db, id)
    if not user:
        return None
    if not user.is_active:
        return None
    if not await verify_password(password, user.hashed_password):
        return None
    return user
