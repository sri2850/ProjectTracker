from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.dependencies.deps import get_db
from app.services.auth_service import authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
    form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, id=int(form.username), password=form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user id or password",
        )
    token = create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}
