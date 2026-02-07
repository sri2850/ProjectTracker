from app.db.models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_by_id(db: AsyncSession, id: int):
    result = await db.execute(select(User).where(User.id == id))
    return result.scalar_one_or_none()
