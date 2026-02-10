from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.project import router as project_router

router = APIRouter(prefix="/api/v1")
router.include_router(project_router, tags=["projects"])
router.include_router(auth_router, tags=["auth"])
