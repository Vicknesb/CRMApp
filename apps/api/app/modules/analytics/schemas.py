from __future__ import annotations
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class DashboardWidget(BaseModel):
    key: str
    title: str
    value: Any
    unit: Optional[str] = None
    trend: Optional[float] = None


class DashboardResponse(BaseModel):
    role: str
    widgets: List[DashboardWidget]


class ReportFilter(BaseModel):
    field: str
    operator: str  # eq, gt, lt, gte, lte, in
    value: Any


class ReportGroupBy(BaseModel):
    field: str


class CustomReportDefinition(BaseModel):
    module: str
    fields: List[str]
    filters: List[ReportFilter] = []
    groupBy: Optional[str] = None
    aggregate: Optional[str] = None  # count, sum, avg, min, max
    aggregateField: Optional[str] = None


class ReportRow(BaseModel):
    data: Dict[str, Any]


class ReportResult(BaseModel):
    columns: List[str]
    rows: List[Dict[str, Any]]
    total: int


class ScheduledReportCreate(BaseModel):
    reportKey: str
    frequency: str  # daily, weekly, monthly
    recipientEmails: List[str]
    format: str = "csv"  # csv, pdf, excel


class ScheduledReportOut(ScheduledReportCreate):
    id: str
    createdAt: str
