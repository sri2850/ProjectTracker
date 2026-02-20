from fastapi import APIRouter, Depends

from app.db.models.user import User
from app.dependencies import project_deps
from app.dependencies.auth_deps import get_current_user
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.services.project_service import ProjectService

router = APIRouter()


@router.post("/projects/", response_model=ProjectRead)
async def create_project_endpoint(
    project_in: ProjectCreate,
    svc: ProjectService = Depends(project_deps.get_project_service),
    current_user: User = Depends(get_current_user),
):
    return await svc.create_project_service(project_in, current_user.id)


@router.get(
    "/projects/{project_id}",
    response_model=ProjectRead,
)
async def get_project_endpoint(
    project_id: int,
    svc: ProjectService = Depends(project_deps.get_project_service),
    current_user: User = Depends(get_current_user),
):
    return await svc.fetch_project_by_id(project_id, current_user.id)


@router.get("/projects/")
async def list_projects_endpoint(
    svc: ProjectService = Depends(project_deps.get_project_service),
    current_user: User = Depends(get_current_user),
):
    return await svc.fetch_all_projects(current_user.id)


@router.put("/projects/{project_id}")
async def update_project_endpoint(
    project_id: int,
    project_in: ProjectUpdate,
    svc: ProjectService = Depends(project_deps.get_project_service),
    current_user: User = Depends(get_current_user),
):
    return await svc.update_project_by_id(project_id, current_user.id, project_in.name)
