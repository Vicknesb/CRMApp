from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.core.enums import TicketChannel, TicketPriority, TicketStatus


class TicketCreate(BaseModel):
    subject: str
    description: Optional[str] = None
    channel: TicketChannel = TicketChannel.MANUAL
    priority: TicketPriority = TicketPriority.MEDIUM
    categoryId: Optional[str] = None
    accountId: Optional[str] = None
    contactId: Optional[str] = None
    assigneeId: Optional[str] = None


class TicketUpdate(BaseModel):
    subject: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    categoryId: Optional[str] = None
    assigneeId: Optional[str] = None


class TicketNoteCreate(BaseModel):
    body: str
    isInternal: bool = True


class TicketListParams(BaseModel):
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    assigneeId: Optional[str] = None
    accountId: Optional[str] = None
    search: Optional[str] = None
    page: int = 1
    page_size: int = 20
