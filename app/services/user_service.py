from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.repositories.user import add_user, get_user_by_email, get_user_by_name
from app.schemas.user import UserCreate

from .errors import Conflict, Unprocessable


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, data: UserCreate):
        username = data.username.strip()
        email = data.email.strip().lower()
        if not username or not data.password:
            raise Unprocessable(message="Invalid registration")
        existing_user = await get_user_by_name(self.db, username)
        existing_email = await get_user_by_email(self.db, email)

        if existing_user:
            raise Conflict(message="user already exists")
        if existing_email:
            raise Conflict(message="Email already exists")
        hashed = await hash_password(data.password)
        try:
            user = await add_user(self.db, username, email, hashed)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except IntegrityError as e:
            await self.db.rollback()
            raise e from Conflict(message="username already exists")
