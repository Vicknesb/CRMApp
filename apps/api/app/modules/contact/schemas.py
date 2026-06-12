from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.core.enums import ActivityType


class ContactCreate(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    phone: Optional[str] = None
    jobTitle: Optional[str] = None
    department: Optional[str] = None
    linkedinUrl: Optional[str] = None


class ContactUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    jobTitle: Optional[str] = None
    department: Optional[str] = None
    linkedinUrl: Optional[str] = None


class InteractionCreate(BaseModel):
    type: ActivityType
    summary: str
    happenedAt: datetime


class ContactResponse(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    phone: Optional[str]
    jobTitle: Optional[str]
    department: Optional[str]
    linkedinUrl: Optional[str]
    ownerId: Optional[str]
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
