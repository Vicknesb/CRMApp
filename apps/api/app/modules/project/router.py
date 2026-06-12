from fastapi import APIRouter, Depends, Query
from typing import Optional
from prisma import Prisma
from app.db.client import get_db
from app.core.security import get_current_user, require_role
from app.modules.project import schemas, service

router = APIRouter(prefix="/projects", tags=["projects"])

MANAGER_ROLES = ["PROJECT_MANAGER", "ADMIN"]


@router.post("", status_code=201)
async def create_project(
    body: schemas.ProjectCreate,
    db: Prisma = Depends(get_db),
    current_user=Depends(require_role(MANAGER_ROLES)),
):
    project = await service.create_project(db, body, current_user.id)
    return {"data": project, "error": None, "meta": {}}


@router.get("")
async def list_projects(
    status: Optional[str] = Query(None),
    accountId: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: Prisma = Depends(get_db),
    _=Depends(get_current_user),
):
    projects = await service.list_projects(db, status, accountId, skip, limit)
    return {"data": projects, "error": None, "meta": {"total": len(projects)}}


@router.get("/{project_id}")
async def get_project(
    project_id: str,
    db: Prisma = Depends(get_db),
    _=Depends(get_current_user),
):
    project = await service.get_project(db, project_id)
    return {"data": project, "error": None, "meta": {}}


@router.patch("/{project_id}")
async def update_project(
    project_id: str,
    body: schemas.ProjectUpdate,
    db: Prisma = Depends(get_db),
    current_user=Depends(require_role(MANAGER_ROLES)),
):
    project = await service.update_project(db, project_id, body, current_user.id)
    return {"data": project, "error": None, "meta": {}}


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: str,
    db: Prisma = Depends(get_db),
    current_user=Depends(require_role(["ADMIN"])),
):
    await service.delete_project(db, project_id, current_user.id)


# Phases
@router.post("/{project_id}/phases", status_code=201)
async def create_phase(
    project_id: str,
    body: schemas.PhaseCreate,
    db: Prisma = Depends(get_db),
    current_user=Depends(require_role(MANAGER_ROLES)),
):
    phase = await service.create_phase(db, project_id, body, current_user.id)
    return {"data": phase, "error": None, "meta": {}}


@router.get("/{project_id}/phases")
async def list_phases(
    project_id: str,
    db: Prisma = Depends(get_db),
    _=Depends(get_current_user),
):
    phases = await service.list_phases(db, project_id)
    return {"data": phases, "error": None, "meta": {}}


# Milestones
@router.post("/{project_id}/milestones", status_code=201)
async def create_milestone(
    project_id: str,
    body: schemas.MilestoneCreate,
    db: Prisma = Depends(get_db),
    current_user=Depends(require_role(MANAGER_ROLES)),
):
    milestone = await service.create_milestone(db, project_id, body, current_user.id)
    return {"data": milestone, "error": None, "meta": {}}


@router.patch("/{project_id}/milestones/{milestone_id}")
async def update_milestone(
    project_id: str,
    milestone_id: str,
    body: schemas.MilestoneUpdate,
    db: Prisma = Depends(get_db),
    current_user=Depends(require_role(MANAGER_ROLES)),
):
    milestone = await service.update_milestone(db, milestone_id, body, current_user.id)
    return {"data": milestone, "error": None, "meta": {}}


@router.get("/{project_id}/milestones")
async def list_milestones(
    project_id: str,
    db: Prisma = Depends(get_db),
    _=Depends(get_current_user),
):
    milestones = await service.list_milestones(db, project_id)
    return {"data": milestones, "error": None, "meta": {}}


# Tasks
@router.post("/{project_id}/tasks", status_code=201)
async def create_task(
    project_id: str,
    body: schemas.ProjectTaskCreate,
    db: Prisma = Depends(get_db),
    current_user=Depends(require_role(MANAGER_ROLES)),
):
    task = await service.create_project_task(db, project_id, body, current_user.id)
    return {"data": task, "error": None, "meta": {}}


@router.patch("/{project_id}/tasks/{task_id}")
async def update_task(
    project_id: str,
    task_id: str,
    body: schemas.ProjectTaskUpdate,
    db: Prisma = Depends(get_db),
    current_user=Depends(require_role(MANAGER_ROLES)),
):
    task = await service.update_project_task(db, task_id, body, current_user.id)
    return {"data": task, "error": None, "meta": {}}


@router.get("/{project_id}/tasks")
async def list_tasks(
    project_id: str,
    db: Prisma = Depends(get_db),
    _=Depends(get_current_user),
):
    tasks = await service.list_project_tasks(db, project_id)
    return {"data": tasks, "error": None, "meta": {}}


# Documents
@router.post("/{project_id}/documents", status_code=201)
async def add_document(
    project_id: str,
    body: schemas.DocumentCreate,
    db: Prisma = Depends(get_db),
    current_user=Depends(require_role(MANAGER_ROLES)),
):
    doc = await service.add_document(db, project_id, body, current_user.id)
    return {"data": doc, "error": None, "meta": {}}


@router.get("/{project_id}/documents")
async def list_documents(
    project_id: str,
    db: Prisma = Depends(get_db),
    _=Depends(get_current_user),
):
    docs = await service.list_documents(db, project_id)
    return {"data": docs, "error": None, "meta": {}}


# Jira sync
@router.post("/jira/sync")
async def jira_sync(
    body: schemas.JiraSyncRequest,
    db: Prisma = Depends(get_db),
    current_user=Depends(require_role(MANAGER_ROLES)),
):
    from app.modules.project.schemas import JiraSyncOut
    result = await service.sync_to_jira(db, JiraSyncOut(**body.model_dump(), synced=False, message=""), current_user.id)
    return {"data": result, "error": None, "meta": {}}
