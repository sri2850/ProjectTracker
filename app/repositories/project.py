from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.project import Project


async def get_project_by_id(db: AsyncSession, project_id: int, user_id: int):
    stmt = select(Project).where(
        Project.id == project_id, Project.created_by == user_id
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_all_projects(db: AsyncSession, user_id: int):
    result = await db.execute(select(Project).where(Project.created_by == user_id))
    return result.scalars().all()


async def create_project(db: AsyncSession, name, user_id):
    project = Project(name=name, created_by=user_id)
    db.add(project)
    await db.flush()
    await db.refresh(project)
    return project


async def save(db: AsyncSession, project: Project) -> Project:
    await db.commit()
    await db.refresh(project)
    return project
