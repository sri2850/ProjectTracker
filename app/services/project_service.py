import hashlib
import json
import logging

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

logger = logging.getLogger(__name__)
CACHE_TTL_SECONDS = 60
CACHE_VER = "v1"


def _projects_list_key(
    *,
    user_id: int,
    limit: int,
    offset: int,
    sort_by: str,
    order: str,
    name: str | None,
):
    payload = {
        "limit": limit,
        "offset": offset,
        "sort_by": sort_by,
        "order": order,
        "name": name,
    }
    fingerprint = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest()[:16]
    return f"projects:list:{CACHE_VER}:{user_id}:{fingerprint}"


class ProjectService:
    def __init__(self, db: AsyncSession, redis):
        self.db = db
        self.redis = redis

    async def _invalidate_projects_list_cache(self, user_id: int):
        keys_set = f"projects:list:keys:{CACHE_VER}:{user_id}"

        keys = await self.redis.smembers(keys_set)
        if keys:
            await self.redis.delete(*list(keys))
        await self.redis.delete(keys_set)
        logger.info("CACHE INVALIDATE user=%s keys=%s", user_id, len(keys))

    async def create_project_service(self, data: ProjectCreate, user: User):
        name = (data.name or "").strip()
        if not name:
            raise Unprocessable(message="project cannot be empty")
        try:
            project = await create_project(self.db, name, user.id)
            await self.db.commit()
            await self._invalidate_projects_list_cache(user.id)
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
        await self._invalidate_projects_list_cache(user.id)
        return project

    async def fetch_all_projects(
        self,
        *,
        limit: int,
        offset: int,
        sort_by: str,
        order: str,
        name: str,
        user: User,
    ):
        cache_key = _projects_list_key(
            user_id=user.id,
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            order=order,
            name=name,
        )

        cached = await self.redis.get(cache_key)
        if cached:
            logger.info("CACHE HIT %s", cache_key)
            return ProjectListResponse.model_validate_json(cached)
        logger.info("CACHE MISS %s", cache_key)

        items, total = await get_all_projects(
            self.db,
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            order=order,
            name=name,
            user_id=user.id,
        )
        resp = ProjectListResponse(
            items=items,
            meta=ProjectListMeta(total=total, limit=limit, offset=offset),
        )
        await self.redis.set(cache_key, resp.model_dump_json(), ex=CACHE_TTL_SECONDS)
        return resp

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
            await self._invalidate_projects_list_cache(user.id)
            return project
        except IntegrityError as err:
            await self.db.rollback()
            raise Conflict() from err

    async def del_proj_by_id(self, project_id: int, user: User):
        project = await self.fetch_project_by_id(project_id, user)
        try:
            await delete_project_by_id(self.db, project)
            await self._invalidate_projects_list_cache(user.id)
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
        await self._invalidate_projects_list_cache(user.id)
        return project
