from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.deps import get_db
from app.services.project_service import ProjectService


def get_project_service(db: AsyncSession = Depends(get_db)):
    return ProjectService(db)
