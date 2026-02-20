from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.project import (
    create_project,
    get_all_projects,
    get_project_by_id,
    save,
)
from app.schemas.project import ProjectCreate

from .errors import Conflict, Forbidden, NotFound, Unprocessable


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_project_service(self, data: ProjectCreate, user_id):
        name = (data.name or "").strip()
        if not name:
            raise Unprocessable(message="project cannot be empty")
        try:
            project = await create_project(self.db, name, user_id)
            await self.db.commit()
            return project
        except IntegrityError as err:
            await self.db.rollback()
            raise Conflict(
                message="project already exists", details={"name": name}
            ) from err

    async def fetch_project_by_id(self, project_id: int, user_id: int):
        project = await get_project_by_id(self.db, project_id, user_id)
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
        result = await get_all_projects(self.db, user_id)
        return result

    async def update_project_by_id(
        self, project_id: int, user_id: int, updated_project_name: str
    ):
        project = await self.fetch_project_by_id(project_id, user_id)

        if not project:
            raise NotFound()

        project.name = updated_project_name
        return await save(self.db, project)
