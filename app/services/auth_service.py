from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_password
from app.db.models.user import User
from app.repositories.user import get_user_by_id


async def authenticate_user(db: AsyncSession, id: int, password):
    user = await get_user_by_id(db, id)
    return (
        user
        if user and verify_password(password, user.hashed_password) and user.is_active
        else None
    )
