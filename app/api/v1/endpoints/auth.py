from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.dependencies.deps import get_db
from app.services.auth_service import authenticate_user
from app.services.errors import InvalidCredentials

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
    form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, id=int(form.username), password=form.password)
    if not user:
        raise InvalidCredentials
    token = create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}
