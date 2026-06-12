from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class ImportFieldMapping(BaseModel):
    sourceColumn: str
    targetField: str


class ImportRequest(BaseModel):
    module: str  # leads, contacts, accounts
    mappings: List[ImportFieldMapping]


class ImportResult(BaseModel):
    total: int
    imported: int
    errors: int
    errorRows: List[Dict[str, Any]] = []


class RecycleBinEntry(BaseModel):
    id: str
    module: str
    recordId: str
    deletedAt: datetime
    purgeAt: datetime


class DataExportRequest(BaseModel):
    subjectEmail: str


class ErasureRequest(BaseModel):
    subjectEmail: str
    reason: str


class ConsentRecord(BaseModel):
    email: str
    consentType: str
    granted: bool
    ipAddress: Optional[str] = None
