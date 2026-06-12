from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from app.core.enums import ActivityType, Priority, TaskStatus


class ActivityCreate(BaseModel):
    type: ActivityType
    subject: str
    description: Optional[str] = None
    relatedType: Optional[str] = None
    relatedId: Optional[str] = None
    happenedAt: datetime = None

    def model_post_init(self, __context):
        if self.happenedAt is None:
            self.happenedAt = datetime.utcnow()


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    dueAt: Optional[datetime] = None
    assigneeId: Optional[str] = None
    relatedType: Optional[str] = None
    relatedId: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[Priority] = None
    dueAt: Optional[datetime] = None
    assigneeId: Optional[str] = None


class ReminderCreate(BaseModel):
    taskId: str
    remindAt: datetime
