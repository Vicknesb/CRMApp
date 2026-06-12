from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional
from app.core.enums import AccountTier, Currency


class AccountCreate(BaseModel):
    name: str
    industry: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[dict] = None
    tier: AccountTier = AccountTier.SMB
    annualRevenue: Optional[Decimal] = None
    currency: Currency = Currency.INR
    parentId: Optional[str] = None


class AccountUpdate(BaseModel):
    name: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[dict] = None
    tier: Optional[AccountTier] = None
    annualRevenue: Optional[Decimal] = None
    parentId: Optional[str] = None


class AccountResponse(BaseModel):
    id: str
    name: str
    industry: Optional[str]
    website: Optional[str]
    tier: AccountTier
    healthScore: int
    annualRevenue: Optional[Decimal]
    currency: Currency
    parentId: Optional[str]
    ownerId: Optional[str]
    createdAt: datetime

    class Config:
        from_attributes = True
