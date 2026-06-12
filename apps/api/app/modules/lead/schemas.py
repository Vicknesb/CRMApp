from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.core.enums import Currency, LeadSource, LeadStatus, Priority, QualificationStage


class LeadCreate(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    jobTitle: Optional[str] = None
    source: LeadSource = LeadSource.OTHER
    utmSource: Optional[str] = None
    utmMedium: Optional[str] = None
    utmCampaign: Optional[str] = None
    budget: Optional[Decimal] = None
    currency: Currency = Currency.INR
    notes: Optional[str] = None
    assigneeId: Optional[str] = None


class LeadUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    jobTitle: Optional[str] = None
    status: Optional[LeadStatus] = None
    source: Optional[LeadSource] = None
    qualStage: Optional[QualificationStage] = None
    budget: Optional[Decimal] = None
    notes: Optional[str] = None
    assigneeId: Optional[str] = None


class LeadResponse(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    phone: Optional[str]
    company: Optional[str]
    jobTitle: Optional[str]
    status: LeadStatus
    source: LeadSource
    score: int
    qualStage: Optional[QualificationStage]
    budget: Optional[Decimal]
    currency: Currency
    notes: Optional[str]
    ownerId: Optional[str]
    assigneeId: Optional[str]
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class LeadListParams(BaseModel):
    page: int = 1
    page_size: int = 20
    status: Optional[LeadStatus] = None
    source: Optional[LeadSource] = None
    assignee_id: Optional[str] = None
    search: Optional[str] = None


class ConvertLeadRequest(BaseModel):
    createAccount: bool = True
    accountName: Optional[str] = None
    createContact: bool = True
    createOpportunity: bool = True
    opportunityTitle: Optional[str] = None


class ScoreLeadResponse(BaseModel):
    leadId: str
    score: int
    delta: int
