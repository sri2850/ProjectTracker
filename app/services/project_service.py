from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.repositories.project import (
    create_project,
    delete_project_by_id,
    get_all_projects,
    get_project_by_id,
    save,
)
from app.schemas.project import (
    ProjectCreate,
    ProjectListMeta,
    ProjectListResponse,
    ProjectPatch,
)

from .errors import Conflict, NotFound, Unprocessable


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_project_service(self, data: ProjectCreate, user: User):
        name = (data.name or "").strip()
        if not name:
            raise Unprocessable(message="project cannot be empty")
        try:
            project = await create_project(self.db, name, user.id)
            await self.db.commit()
            return project
        except IntegrityError as err:
            await self.db.rollback()
            raise Conflict(
                message="project already exists", details={"name": name}
            ) from err

    async def fetch_project_by_id(self, project_id: int, user: User):
        project = await get_project_by_id(self.db, project_id, user.id)
        if not project:
            raise NotFound(
                message="Project not found", details={"project_id": project_id}
            )
        return project

    async def fetch_all_projects(self, *, limit: int, offset: int, user: User):
        items, total = await get_all_projects(
            self.db,
            limit=limit,
            offset=offset,
            user_id=user.id,
        )
        return ProjectListResponse(
            items=items,
            meta=ProjectListMeta(
                total=total,
                limit=limit,
                offset=offset,
            ),
        )

    async def update_project_by_id(
        self, project_id: int, user: User, updated_project_name: str
    ):
        name = (updated_project_name or "").strip()

        if not name:
            raise Unprocessable(message="project cannot be empty")

        project = await self.fetch_project_by_id(project_id, user)
        try:
            project.name = name
            await save(self.db, project)
            await self.db.commit()
            return project
        except IntegrityError as err:
            await self.db.rollback()
            raise Conflict() from err

    async def del_proj_by_id(self, project_id: int, user: User):
        project = await self.fetch_project_by_id(project_id, user)
        try:
            await delete_project_by_id(self.db, project)
            await self.db.commit()
        except IntegrityError as err:
            await self.db.rollback()
            raise Conflict(message="cannot delete the project") from err

    async def update_project_partial(
        self,
        project_id: int,
        user: User,
        update_data: ProjectPatch,
    ):
        project = await self.fetch_project_by_id(project_id, user)

        if update_data.name is not None:
            name = update_data.name.strip()
            if not name:
                raise Unprocessable(message="project cannot be empty")
            project.name = name

        await save(self.db, project)
        await self.db.commit()
        return project
