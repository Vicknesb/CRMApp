from __future__ import annotations
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from app.core.enums import UserRole


class PermissionCreate(BaseModel):
    role: UserRole
    module: str
    action: str
    fieldRules: Dict[str, Any] = {}


class PermissionOut(PermissionCreate):
    id: str
    createdAt: str
    updatedAt: str

    class Config:
        from_attributes = True


class CustomFieldCreate(BaseModel):
    module: str
    fieldName: str
    fieldType: str  # text, number, date, select, boolean
    label: str
    required: bool = False
    options: Optional[List[str]] = None
    order: int = 0


class CustomFieldOut(CustomFieldCreate):
    id: str
    isActive: bool
    createdAt: str

    class Config:
        from_attributes = True


class WorkflowCreate(BaseModel):
    name: str
    module: str
    triggerType: str  # on_create, on_update, on_status_change, scheduled
    conditions: Dict[str, Any] = {}
    actions: List[Dict[str, Any]] = []
    isActive: bool = True


class WorkflowOut(WorkflowCreate):
    id: str
    createdAt: str
    updatedAt: str

    class Config:
        from_attributes = True


class UserAdminUpdate(BaseModel):
    role: Optional[UserRole] = None
    isActive: Optional[bool] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None


class LayoutCreate(BaseModel):
    module: str
    role: UserRole
    config: Dict[str, Any]


class LayoutOut(LayoutCreate):
    id: str
    createdAt: str
    updatedAt: str

    class Config:
        from_attributes = True


class AuditLogFilter(BaseModel):
    module: Optional[str] = None
    action: Optional[str] = None
    userId: Optional[str] = None
    skip: int = 0
    limit: int = 50
