from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class NotificationOut(BaseModel):
    id: str
    userId: str
    type: str
    title: str
    body: Optional[str] = None
    readAt: Optional[datetime] = None
    relatedType: Optional[str] = None
    relatedId: Optional[str] = None
    createdAt: datetime

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    content: str
    relatedType: str
    relatedId: str
    parentId: Optional[str] = None


class CommentOut(BaseModel):
    id: str
    authorId: Optional[str] = None
    content: str
    relatedType: str
    relatedId: str
    parentId: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime
    replies: List["CommentOut"] = []

    class Config:
        from_attributes = True


CommentOut.model_rebuild()


class MentionCreate(BaseModel):
    mentionedUserId: str
    relatedType: str
    relatedId: str


class EmailTemplateCreate(BaseModel):
    name: str
    subject: str
    body: str
    variables: List[str] = []


class EmailTemplateOut(EmailTemplateCreate):
    id: str
    isActive: bool
    createdAt: datetime

    class Config:
        from_attributes = True


class TemplatePreview(BaseModel):
    subject: str
    body: str


class SlackNotifyPayload(BaseModel):
    channel: str
    message: str
    eventType: Optional[str] = None
