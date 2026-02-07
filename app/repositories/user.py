from db.models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_by_id(db: AsyncSession, id: int):
    return await db.execute(User, id)
