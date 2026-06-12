from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field
from app.core.enums import ProjectStatus, TaskStatus, Priority, Currency


class PhaseCreate(BaseModel):
    name: str
    order: int
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None


class PhaseOut(PhaseCreate):
    id: str
    projectId: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class MilestoneCreate(BaseModel):
    name: str
    phaseId: Optional[str] = None
    dueDate: Optional[datetime] = None
    order: int = 0


class MilestoneUpdate(BaseModel):
    name: Optional[str] = None
    dueDate: Optional[datetime] = None
    completedAt: Optional[datetime] = None
    order: Optional[int] = None


class MilestoneOut(MilestoneCreate):
    id: str
    projectId: str
    completedAt: Optional[datetime] = None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class ProjectTaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: Priority = Priority.MEDIUM
    assigneeId: Optional[str] = None
    effortHours: Optional[Decimal] = None
    dueAt: Optional[datetime] = None


class ProjectTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[Priority] = None
    assigneeId: Optional[str] = None
    effortHours: Optional[Decimal] = None
    dueAt: Optional[datetime] = None
    completedAt: Optional[datetime] = None


class ProjectTaskOut(ProjectTaskCreate):
    id: str
    projectId: str
    completedAt: Optional[datetime] = None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class DocumentCreate(BaseModel):
    name: str
    url: str
    mimeType: Optional[str] = None
    sizeBytes: Optional[int] = None


class DocumentOut(DocumentCreate):
    id: str
    projectId: str
    uploadedById: Optional[str] = None
    createdAt: datetime

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.PLANNING
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    budget: Optional[Decimal] = None
    currency: Currency = Currency.INR
    accountId: Optional[str] = None
    opportunityId: Optional[str] = None
    managerId: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    budget: Optional[Decimal] = None
    currency: Optional[Currency] = None
    accountId: Optional[str] = None
    managerId: Optional[str] = None


class ProjectOut(ProjectCreate):
    id: str
    createdAt: datetime
    updatedAt: datetime
    phases: List[PhaseOut] = []
    milestones: List[MilestoneOut] = []
    tasks: List[ProjectTaskOut] = []
    documents: List[DocumentOut] = []

    class Config:
        from_attributes = True


class ProjectListOut(BaseModel):
    id: str
    name: str
    status: ProjectStatus
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    budget: Optional[Decimal] = None
    currency: Currency
    accountId: Optional[str] = None
    createdAt: datetime

    class Config:
        from_attributes = True


class JiraSyncRequest(BaseModel):
    projectTaskId: str
    jiraIssueKey: str


class JiraSyncOut(BaseModel):
    projectTaskId: str
    jiraIssueKey: str
    synced: bool
    message: str
