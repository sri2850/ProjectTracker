from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User


async def get_user_by_email(db: AsyncSession, email):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_login(db: AsyncSession, login: str):
    result = await db.execute(
        select(User).where(or_(User.email == login, User.username == login))
    )
    return result.scalar_one_or_none()
