from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional, List
from prisma import Prisma
from app.modules.project.schemas import (
    ProjectCreate, ProjectUpdate, PhaseCreate, MilestoneCreate, MilestoneUpdate,
    ProjectTaskCreate, ProjectTaskUpdate, DocumentCreate, JiraSyncOut,
)
from app.core.audit import record_audit
from fastapi import HTTPException


async def create_project(db: Prisma, data: ProjectCreate, actor_id: str):
    project = await db.project.create(data={
        "name": data.name,
        "description": data.description,
        "status": data.status.value,
        "startDate": data.startDate,
        "endDate": data.endDate,
        "budget": data.budget,
        "currency": data.currency.value,
        "accountId": data.accountId,
        "opportunityId": data.opportunityId,
        "managerId": data.managerId or actor_id,
    })
    await record_audit(db, actor_id, "CREATE", "projects", record_id=project.id)
    return project


async def get_project(db: Prisma, project_id: str):
    project = await db.project.find_first(
        where={"id": project_id, "deletedAt": None},
        include={"phases": True, "milestones": True, "tasks": True, "documents": True},
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


async def list_projects(db: Prisma, status: Optional[str] = None, account_id: Optional[str] = None,
                        skip: int = 0, limit: int = 50) -> List:
    where: dict = {"deletedAt": None}
    if status:
        where["status"] = status
    if account_id:
        where["accountId"] = account_id
    return await db.project.find_many(where=where, skip=skip, take=limit,
                                       order={"createdAt": "desc"})


async def update_project(db: Prisma, project_id: str, data: ProjectUpdate, actor_id: str):
    await get_project(db, project_id)
    payload = {k: v for k, v in data.model_dump(exclude_none=True).items()}
    if "status" in payload:
        payload["status"] = payload["status"].value
    if "currency" in payload:
        payload["currency"] = payload["currency"].value
    project = await db.project.update(where={"id": project_id}, data=payload)
    await record_audit(db, actor_id, "UPDATE", "projects", record_id=project_id)
    return project


async def delete_project(db: Prisma, project_id: str, actor_id: str):
    await get_project(db, project_id)
    await db.project.update(where={"id": project_id},
                             data={"deletedAt": datetime.now(timezone.utc)})
    await record_audit(db, actor_id, "DELETE", "projects", record_id=project_id)


# Phases
async def create_phase(db: Prisma, project_id: str, data: PhaseCreate, actor_id: str):
    await get_project(db, project_id)
    phase = await db.phase.create(data={
        "projectId": project_id,
        "name": data.name,
        "order": data.order,
        "startDate": data.startDate,
        "endDate": data.endDate,
    })
    await record_audit(db, actor_id, "CREATE", "phases", record_id=phase.id)
    return phase


async def list_phases(db: Prisma, project_id: str):
    return await db.phase.find_many(where={"projectId": project_id}, order={"order": "asc"})


# Milestones
async def create_milestone(db: Prisma, project_id: str, data: MilestoneCreate, actor_id: str):
    await get_project(db, project_id)
    milestone = await db.milestone.create(data={
        "projectId": project_id,
        "phaseId": data.phaseId,
        "name": data.name,
        "dueDate": data.dueDate,
        "order": data.order,
    })
    await record_audit(db, actor_id, "CREATE", "milestones", record_id=milestone.id)
    return milestone


async def update_milestone(db: Prisma, milestone_id: str, data: MilestoneUpdate, actor_id: str):
    payload = {k: v for k, v in data.model_dump(exclude_none=True).items()}
    milestone = await db.milestone.update(where={"id": milestone_id}, data=payload)
    await record_audit(db, actor_id, "UPDATE", "milestones", record_id=milestone_id)
    return milestone


async def list_milestones(db: Prisma, project_id: str):
    return await db.milestone.find_many(where={"projectId": project_id}, order={"order": "asc"})


# Project Tasks
async def create_project_task(db: Prisma, project_id: str, data: ProjectTaskCreate, actor_id: str):
    await get_project(db, project_id)
    task = await db.projecttask.create(data={
        "projectId": project_id,
        "title": data.title,
        "description": data.description,
        "status": data.status.value,
        "priority": data.priority.value,
        "assigneeId": data.assigneeId,
        "effortHours": data.effortHours,
        "dueAt": data.dueAt,
    })
    await record_audit(db, actor_id, "CREATE", "project_tasks", record_id=task.id)
    await _rollup_project_status(db, project_id, actor_id)
    return task


async def update_project_task(db: Prisma, task_id: str, data: ProjectTaskUpdate, actor_id: str):
    task = await db.projecttask.find_unique(where={"id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    payload = {k: v for k, v in data.model_dump(exclude_none=True).items()}
    if "status" in payload:
        payload["status"] = payload["status"].value
    if "priority" in payload:
        payload["priority"] = payload["priority"].value
    updated = await db.projecttask.update(where={"id": task_id}, data=payload)
    await record_audit(db, actor_id, "UPDATE", "project_tasks", record_id=task_id)
    await _rollup_project_status(db, task.projectId, actor_id)
    return updated


async def list_project_tasks(db: Prisma, project_id: str):
    return await db.projecttask.find_many(where={"projectId": project_id},
                                           order={"createdAt": "desc"})


async def _rollup_project_status(db: Prisma, project_id: str, actor_id: str):
    """Update project status based on task completion."""
    tasks = await db.projecttask.find_many(where={"projectId": project_id})
    if not tasks:
        return
    statuses = {t.status for t in tasks}
    if all(t.status == "COMPLETED" for t in tasks):
        new_status = "COMPLETED"
    elif any(t.status == "IN_PROGRESS" for t in tasks):
        new_status = "ACTIVE"
    else:
        new_status = None
    if new_status:
        await db.project.update(where={"id": project_id}, data={"status": new_status})


# Documents
async def add_document(db: Prisma, project_id: str, data: DocumentCreate, actor_id: str):
    await get_project(db, project_id)
    doc = await db.document.create(data={
        "projectId": project_id,
        "name": data.name,
        "url": data.url,
        "mimeType": data.mimeType,
        "sizeBytes": data.sizeBytes,
        "uploadedById": actor_id,
    })
    await record_audit(db, actor_id, "CREATE", "documents", record_id=doc.id)
    return doc


async def list_documents(db: Prisma, project_id: str):
    return await db.document.find_many(where={"projectId": project_id},
                                        order={"createdAt": "desc"})


# Jira sync stub
async def sync_to_jira(db: Prisma, data: JiraSyncOut, actor_id: str) -> JiraSyncOut:
    task = await db.projecttask.find_unique(where={"id": data.projectTaskId})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await record_audit(db, actor_id, "JIRA_SYNC", "project_tasks", record_id=data.projectTaskId)
    return JiraSyncOut(
        projectTaskId=data.projectTaskId,
        jiraIssueKey=data.jiraIssueKey,
        synced=True,
        message=f"Task synced to Jira issue {data.jiraIssueKey}",
    )
