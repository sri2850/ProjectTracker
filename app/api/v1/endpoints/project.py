from fastapi import APIRouter, Depends, HTTPException
from app.schemas.project import ProjectRead, ProjectCreate
from app.services.project_service import ProjectService
from app.dependencies import project_deps
from app.dependencies.auth_deps import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/projects/", response_model=ProjectRead)
async def create_project_endpoint(
    project_in: ProjectCreate,
    svc: ProjectService = Depends(project_deps.get_project_service),
):
    return await svc.create_project(project_in)


@router.get(
    "/projects/{project_id}",
    response_model=ProjectRead,
    responses={404: {"description": "project not found"}},
)
async def get_project_endpoint(
    project_id: int, svc: ProjectService = Depends(project_deps.get_project_service)
):
    project = await svc.get_project_by_id(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")
    return project


@router.get("/projects/")
async def list_projects_endpoint(
    svc: ProjectService = Depends(project_deps.get_project_service),
):
    return await svc.fetch_all_projects()
