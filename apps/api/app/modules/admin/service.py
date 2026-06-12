from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional, List, Any, Dict
from prisma import Prisma
from app.modules.admin.schemas import (
    PermissionCreate, CustomFieldCreate, WorkflowCreate, UserAdminUpdate, LayoutCreate,
)
from app.core.audit import record_audit
from fastapi import HTTPException


# ── Users ─────────────────────────────────────────────────────────────────────

async def list_users(db: Prisma, skip: int = 0, limit: int = 50):
    return await db.user.find_many(
        where={"deletedAt": None}, skip=skip, take=limit, order={"createdAt": "desc"}
    )


async def update_user(db: Prisma, user_id: str, data: UserAdminUpdate, actor_id: str):
    user = await db.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    payload = {k: v for k, v in data.model_dump(exclude_none=True).items()}
    if "role" in payload:
        payload["role"] = payload["role"].value
    updated = await db.user.update(where={"id": user_id}, data=payload)
    await record_audit(db, actor_id, "UPDATE", "users", record_id=user_id)
    return updated


async def deactivate_user(db: Prisma, user_id: str, actor_id: str):
    user = await db.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated = await db.user.update(where={"id": user_id}, data={"isActive": False})
    await record_audit(db, actor_id, "DEACTIVATE", "users", record_id=user_id)
    return updated


# ── Permissions ───────────────────────────────────────────────────────────────

async def list_permissions(db: Prisma, role: Optional[str] = None, module: Optional[str] = None):
    where: dict = {}
    if role:
        where["role"] = role
    if module:
        where["module"] = module
    return await db.permission.find_many(where=where, order={"module": "asc"})


async def upsert_permission(db: Prisma, data: PermissionCreate, actor_id: str):
    existing = await db.permission.find_first(
        where={"role": data.role.value, "module": data.module, "action": data.action}
    )
    if existing:
        perm = await db.permission.update(
            where={"id": existing.id},
            data={"fieldRules": data.fieldRules},
        )
    else:
        perm = await db.permission.create(data={
            "role": data.role.value,
            "module": data.module,
            "action": data.action,
            "fieldRules": data.fieldRules,
        })
    await record_audit(db, actor_id, "UPSERT", "permissions", record_id=perm.id)
    return perm


async def delete_permission(db: Prisma, permission_id: str, actor_id: str):
    perm = await db.permission.find_unique(where={"id": permission_id})
    if not perm:
        raise HTTPException(status_code=404, detail="Permission not found")
    await db.permission.delete(where={"id": permission_id})
    await record_audit(db, actor_id, "DELETE", "permissions", record_id=permission_id)


# ── Custom fields ─────────────────────────────────────────────────────────────

async def list_custom_fields(db: Prisma, module: Optional[str] = None):
    where: dict = {"isActive": True}
    if module:
        where["module"] = module
    return await db.customfield.find_many(where=where, order={"order": "asc"})


async def create_custom_field(db: Prisma, data: CustomFieldCreate, actor_id: str):
    existing = await db.customfield.find_first(
        where={"module": data.module, "fieldName": data.fieldName}
    )
    if existing:
        raise HTTPException(status_code=422, detail="Field name already exists in this module")
    field = await db.customfield.create(data={
        "module": data.module,
        "fieldName": data.fieldName,
        "fieldType": data.fieldType,
        "label": data.label,
        "required": data.required,
        "options": data.options,
        "order": data.order,
    })
    await record_audit(db, actor_id, "CREATE", "custom_fields", record_id=field.id)
    return field


async def delete_custom_field(db: Prisma, field_id: str, actor_id: str):
    field = await db.customfield.find_unique(where={"id": field_id})
    if not field:
        raise HTTPException(status_code=404, detail="Custom field not found")
    await db.customfield.update(where={"id": field_id}, data={"isActive": False})
    await record_audit(db, actor_id, "DELETE", "custom_fields", record_id=field_id)


# ── Workflows ─────────────────────────────────────────────────────────────────

async def list_workflows(db: Prisma, module: Optional[str] = None):
    where: dict = {}
    if module:
        where["module"] = module
    return await db.workflow.find_many(where=where, order={"name": "asc"})


async def create_workflow(db: Prisma, data: WorkflowCreate, actor_id: str):
    wf = await db.workflow.create(data={
        "name": data.name,
        "module": data.module,
        "triggerType": data.triggerType,
        "conditions": data.conditions,
        "actions": data.actions,
        "isActive": data.isActive,
    })
    await record_audit(db, actor_id, "CREATE", "workflows", record_id=wf.id)
    return wf


async def update_workflow(db: Prisma, wf_id: str, data: WorkflowCreate, actor_id: str):
    wf = await db.workflow.find_unique(where={"id": wf_id})
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    updated = await db.workflow.update(where={"id": wf_id}, data={
        "name": data.name,
        "conditions": data.conditions,
        "actions": data.actions,
        "isActive": data.isActive,
    })
    await record_audit(db, actor_id, "UPDATE", "workflows", record_id=wf_id)
    return updated


async def evaluate_workflow(db: Prisma, module: str, trigger_type: str,
                             record_data: Dict[str, Any]) -> List[str]:
    """Evaluate active workflows for a trigger. Returns list of fired action descriptions."""
    workflows = await db.workflow.find_many(
        where={"module": module, "triggerType": trigger_type, "isActive": True}
    )
    fired = []
    for wf in workflows:
        conditions = wf.conditions or {}
        # Simple condition evaluation: all conditions must match
        all_match = True
        for field, expected in conditions.items():
            if record_data.get(field) != expected:
                all_match = False
                break
        if all_match:
            fired.extend([a.get("type", "unknown") for a in (wf.actions or [])])
    return fired


# ── Audit logs ────────────────────────────────────────────────────────────────

async def list_audit_logs(db: Prisma, module: Optional[str] = None,
                           action: Optional[str] = None, user_id: Optional[str] = None,
                           skip: int = 0, limit: int = 50):
    where: dict = {}
    if module:
        where["module"] = module
    if action:
        where["action"] = action
    if user_id:
        where["userId"] = user_id
    return await db.auditlog.find_many(
        where=where, skip=skip, take=limit, order={"createdAt": "desc"}
    )


# ── Layouts ───────────────────────────────────────────────────────────────────

async def upsert_layout(db: Prisma, data: LayoutCreate, actor_id: str):
    existing = await db.layout.find_first(
        where={"module": data.module, "role": data.role.value}
    )
    if existing:
        layout = await db.layout.update(
            where={"id": existing.id}, data={"config": data.config}
        )
    else:
        layout = await db.layout.create(data={
            "module": data.module,
            "role": data.role.value,
            "config": data.config,
        })
    await record_audit(db, actor_id, "UPSERT", "layouts", record_id=layout.id)
    return layout
