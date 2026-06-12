from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel
from app.core.enums import ContractStatus, Currency, SignatureStatus


class AmendmentCreate(BaseModel):
    description: str
    effectiveAt: datetime


class AmendmentOut(AmendmentCreate):
    id: str
    contractId: str
    createdAt: datetime

    class Config:
        from_attributes = True


class SignatureOut(BaseModel):
    id: str
    contractId: str
    signerName: str
    signerEmail: str
    status: SignatureStatus
    signedAt: Optional[datetime] = None
    provider: Optional[str] = None
    externalId: Optional[str] = None
    createdAt: datetime

    class Config:
        from_attributes = True


class SignatureRequest(BaseModel):
    signerName: str
    signerEmail: str
    provider: str = "docusign"


class SignatureCallbackPayload(BaseModel):
    externalId: str
    status: str
    signedAt: Optional[datetime] = None


class ContractCreate(BaseModel):
    title: str
    accountId: Optional[str] = None
    opportunityId: Optional[str] = None
    startDate: datetime
    endDate: datetime
    value: Decimal
    currency: Currency = Currency.INR
    terms: Optional[str] = None
    autoRenew: bool = False
    renewalNoticeDays: int = 30


class ContractUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[ContractStatus] = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    value: Optional[Decimal] = None
    currency: Optional[Currency] = None
    terms: Optional[str] = None
    autoRenew: Optional[bool] = None
    renewalNoticeDays: Optional[int] = None


class ContractOut(ContractCreate):
    id: str
    number: str
    status: ContractStatus
    createdAt: datetime
    updatedAt: datetime
    amendments: List[AmendmentOut] = []
    signatures: List[SignatureOut] = []

    class Config:
        from_attributes = True


class ContractListOut(BaseModel):
    id: str
    number: str
    title: str
    status: ContractStatus
    accountId: Optional[str] = None
    value: Decimal
    currency: Currency
    startDate: datetime
    endDate: datetime
    autoRenew: bool
    createdAt: datetime

    class Config:
        from_attributes = True


class RenewalReminder(BaseModel):
    contractId: str
    number: str
    title: str
    endDate: datetime
    daysUntilExpiry: int
    autoRenew: bool
