from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.project import Project
from app.schemas.project import ProjectCreate
from sqlalchemy import select


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_project(self, data: ProjectCreate):
        project = Project(name=data.name)
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def get_project_by_id(self, project_id: int):
        return await self.db.get(Project, project_id)

    async def fetch_all_projects(self):
        result = await self.db.execute(select(Project))
        return result.scalars().all()
