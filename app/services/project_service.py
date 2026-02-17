from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.project import Project
from app.schemas.project import ProjectCreate

from .errors import Conflict, Forbidden, NotFound, Unprocessable


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_project(self, data: ProjectCreate, user_id):
        name = data.name.strip() if data.name else ""
        if not name:
            raise Unprocessable(message="project name cannot be empty")
        existing = await self.db.execute(select(Project).where(Project.name == name))
        if existing.scalars().first() is not None:
            raise Conflict(message="Project already exists", details={"name": name})
        project = Project(name=name, created_by=user_id)
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def get_project_by_id(self, project_id: int, user_id: int):
        project = await self.db.get(Project, project_id)
        if not project:
            raise NotFound(
                message="Project not found", details={"project_id": project_id}
            )
        if project.created_by != user_id:
            raise Forbidden(
                message="You're not authorized", details={"project_id": project_id}
            )
        return project

    async def fetch_all_projects(self, user_id: int):
        result = await self.db.execute(
            select(Project).where(Project.created_by == user_id)
        )
        return result.scalars().all()
