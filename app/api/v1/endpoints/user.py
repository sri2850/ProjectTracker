from fastapi import APIRouter, Depends, status

from app.dependencies import user_deps
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate, svc: UserService = Depends(user_deps.get_user_service)
):
    return await svc.register_user(user_in)
