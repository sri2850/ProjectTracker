from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_password
from app.db.models.user import User
from app.repositories.user import get_user_by_email


async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not user.is_active:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

    # return user if user and verify_password(password, user.hashed_password) else None
