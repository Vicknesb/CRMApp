from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Any
from pydantic import BaseModel
from app.core.enums import CampaignStatus, CampaignType, Currency


class SegmentCreate(BaseModel):
    name: str
    filters: dict = {}


class SegmentOut(SegmentCreate):
    id: str
    campaignId: str
    createdAt: datetime

    class Config:
        from_attributes = True


class MetricIngest(BaseModel):
    metricKey: str
    value: Decimal


class MetricOut(BaseModel):
    id: str
    campaignId: str
    metricKey: str
    value: Decimal
    recordedAt: datetime

    class Config:
        from_attributes = True


class CampaignMetricsSummary(BaseModel):
    sent: int = 0
    opens: int = 0
    clicks: int = 0
    conversions: int = 0
    openRate: float = 0.0
    clickRate: float = 0.0
    conversionRate: float = 0.0


class EventCreate(BaseModel):
    name: str
    description: Optional[str] = None
    location: Optional[str] = None
    startsAt: datetime
    endsAt: Optional[datetime] = None


class EventOut(EventCreate):
    id: str
    campaignId: Optional[str] = None
    createdAt: datetime

    class Config:
        from_attributes = True


class CampaignCreate(BaseModel):
    name: str
    type: CampaignType
    status: CampaignStatus = CampaignStatus.DRAFT
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    budget: Optional[Decimal] = None
    currency: Currency = Currency.INR
    ownerId: Optional[str] = None


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[CampaignStatus] = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    budget: Optional[Decimal] = None


class CampaignOut(CampaignCreate):
    id: str
    createdAt: datetime
    updatedAt: datetime
    segments: List[SegmentOut] = []
    metrics: List[MetricOut] = []

    class Config:
        from_attributes = True


class CampaignListOut(BaseModel):
    id: str
    name: str
    type: CampaignType
    status: CampaignStatus
    budget: Optional[Decimal] = None
    currency: Currency
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    createdAt: datetime

    class Config:
        from_attributes = True


class ROIReport(BaseModel):
    campaignId: str
    campaignName: str
    budget: Decimal
    attributedRevenue: Decimal
    roi: float
    leadsGenerated: int
    dealsWon: int
