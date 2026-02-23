from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.project import Project


async def get_project_by_id(db: AsyncSession, project_id: int, user_id: int):
    stmt = select(Project).where(
        Project.id == project_id, Project.created_by == user_id
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_all_projects(
    db: AsyncSession, *, limit: int = 100, offset: int = 0, user_id: int
):
    base_query = select(Project).where(Project.created_by == user_id)
    count_query = select(func.count()).select_from(base_query.subquery())

    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    query = base_query.limit(limit).offset(offset)
    result = await db.execute(query)
    items = result.scalars().all()
    return items, total


async def create_project(db: AsyncSession, name, user_id):
    project = Project(name=name, created_by=user_id)
    db.add(project)
    await db.flush()
    await db.refresh(project)
    return project


async def save(db: AsyncSession, project: Project) -> Project:
    await db.flush()
    await db.refresh(project)
    return project


async def delete_project_by_id(db: AsyncSession, project: Project):
    return await db.delete(project)
