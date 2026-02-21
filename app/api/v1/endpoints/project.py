from fastapi import APIRouter, Depends, status

from app.db.models.user import User
from app.dependencies import project_deps
from app.dependencies.auth_deps import get_current_user
from app.schemas.project import ProjectCreate, ProjectPatch, ProjectRead, ProjectUpdate
from app.services.project_service import ProjectService

router = APIRouter()


@router.post(
    "/projects/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED
)
async def create_project_endpoint(
    project_in: ProjectCreate,
    svc: ProjectService = Depends(project_deps.get_project_service),
    current_user: User = Depends(get_current_user),
):
    return await svc.create_project_service(project_in, current_user)


@router.get(
    "/projects/{project_id}", response_model=ProjectRead, status_code=status.HTTP_200_OK
)
async def get_project_endpoint(
    project_id: int,
    svc: ProjectService = Depends(project_deps.get_project_service),
    current_user: User = Depends(get_current_user),
):
    return await svc.fetch_project_by_id(project_id, current_user)


@router.get("/projects/", status_code=status.HTTP_200_OK)
async def list_projects_endpoint(
    svc: ProjectService = Depends(project_deps.get_project_service),
    current_user: User = Depends(get_current_user),
):
    return await svc.fetch_all_projects(current_user)


@router.put("/projects/{project_id}", status_code=status.HTTP_200_OK)
async def update_project_endpoint(
    project_id: int,
    project_in: ProjectUpdate,
    svc: ProjectService = Depends(project_deps.get_project_service),
    current_user: User = Depends(get_current_user),
):
    return await svc.update_project_by_id(project_id, current_user, project_in.name)


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_endpoint(
    project_id: int,
    svc: ProjectService = Depends(project_deps.get_project_service),
    current_user: User = Depends(get_current_user),
):
    return await svc.del_proj_by_id(project_id, current_user)


@router.patch("/projects/{project_id}", response_model=ProjectRead)
async def patch_project_endpoint(
    project_id: int,
    project_in: ProjectPatch,
    svc: ProjectService = Depends(project_deps.get_project_service),
    current_user: User = Depends(get_current_user),
):
    return await svc.update_project_partial(
        project_id,
        current_user,
        project_in,
    )
