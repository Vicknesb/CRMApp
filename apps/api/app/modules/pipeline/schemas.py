from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional
from app.core.enums import Currency


class OpportunityCreate(BaseModel):
    title: str
    value: Decimal
    currency: Currency = Currency.INR
    closeDate: datetime
    serviceType: Optional[str] = None
    stageId: str
    accountId: Optional[str] = None
    contactId: Optional[str] = None
    probability: int = 0


class OpportunityUpdate(BaseModel):
    title: Optional[str] = None
    value: Optional[Decimal] = None
    closeDate: Optional[datetime] = None
    serviceType: Optional[str] = None
    stageId: Optional[str] = None
    probability: Optional[int] = None
    lostReason: Optional[str] = None


class StageMove(BaseModel):
    stageId: str


class ForecastResponse(BaseModel):
    totalWeightedValue: float
    currency: str
    byStage: list[dict]
