from fastapi import APIRouter, Depends, Query
from typing import Optional
from prisma import Prisma
from app.db.client import get_db
from app.core.security import get_current_user, require_role
from app.modules.admin import schemas, service

router = APIRouter(prefix="/admin", tags=["admin"])
ADMIN_ONLY = ["ADMIN"]


# ── Users ─────────────────────────────────────────────────────────────────────

@router.get("/users")
async def list_users(skip: int = 0, limit: int = 50, db: Prisma = Depends(get_db),
                     _=Depends(require_role(ADMIN_ONLY))):
    users = await service.list_users(db, skip, limit)
    return {"data": users, "error": None, "meta": {"total": len(users)}}


@router.patch("/users/{user_id}")
async def update_user(user_id: str, body: schemas.UserAdminUpdate, db: Prisma = Depends(get_db),
                      current_user=Depends(require_role(ADMIN_ONLY))):
    user = await service.update_user(db, user_id, body, current_user.id)
    return {"data": user, "error": None, "meta": {}}


@router.post("/users/{user_id}/deactivate", status_code=204)
async def deactivate_user(user_id: str, db: Prisma = Depends(get_db),
                           current_user=Depends(require_role(ADMIN_ONLY))):
    await service.deactivate_user(db, user_id, current_user.id)


# ── Permissions ───────────────────────────────────────────────────────────────

@router.get("/permissions")
async def list_permissions(role: Optional[str] = Query(None), module: Optional[str] = Query(None),
                            db: Prisma = Depends(get_db), _=Depends(require_role(ADMIN_ONLY))):
    perms = await service.list_permissions(db, role, module)
    return {"data": perms, "error": None, "meta": {}}


@router.post("/permissions", status_code=201)
async def upsert_permission(body: schemas.PermissionCreate, db: Prisma = Depends(get_db),
                             current_user=Depends(require_role(ADMIN_ONLY))):
    perm = await service.upsert_permission(db, body, current_user.id)
    return {"data": perm, "error": None, "meta": {}}


@router.delete("/permissions/{permission_id}", status_code=204)
async def delete_permission(permission_id: str, db: Prisma = Depends(get_db),
                             current_user=Depends(require_role(ADMIN_ONLY))):
    await service.delete_permission(db, permission_id, current_user.id)


# ── Custom fields ─────────────────────────────────────────────────────────────

@router.get("/custom-fields")
async def list_custom_fields(module: Optional[str] = Query(None), db: Prisma = Depends(get_db),
                              _=Depends(get_current_user)):
    fields = await service.list_custom_fields(db, module)
    return {"data": fields, "error": None, "meta": {}}


@router.post("/custom-fields", status_code=201)
async def create_custom_field(body: schemas.CustomFieldCreate, db: Prisma = Depends(get_db),
                               current_user=Depends(require_role(ADMIN_ONLY))):
    field = await service.create_custom_field(db, body, current_user.id)
    return {"data": field, "error": None, "meta": {}}


@router.delete("/custom-fields/{field_id}", status_code=204)
async def delete_custom_field(field_id: str, db: Prisma = Depends(get_db),
                               current_user=Depends(require_role(ADMIN_ONLY))):
    await service.delete_custom_field(db, field_id, current_user.id)


# ── Workflows ─────────────────────────────────────────────────────────────────

@router.get("/workflows")
async def list_workflows(module: Optional[str] = Query(None), db: Prisma = Depends(get_db),
                          _=Depends(require_role(ADMIN_ONLY))):
    workflows = await service.list_workflows(db, module)
    return {"data": workflows, "error": None, "meta": {}}


@router.post("/workflows", status_code=201)
async def create_workflow(body: schemas.WorkflowCreate, db: Prisma = Depends(get_db),
                           current_user=Depends(require_role(ADMIN_ONLY))):
    wf = await service.create_workflow(db, body, current_user.id)
    return {"data": wf, "error": None, "meta": {}}


@router.patch("/workflows/{wf_id}")
async def update_workflow(wf_id: str, body: schemas.WorkflowCreate, db: Prisma = Depends(get_db),
                           current_user=Depends(require_role(ADMIN_ONLY))):
    wf = await service.update_workflow(db, wf_id, body, current_user.id)
    return {"data": wf, "error": None, "meta": {}}


# ── Audit logs ────────────────────────────────────────────────────────────────

@router.get("/audit-logs")
async def list_audit_logs(module: Optional[str] = Query(None), action: Optional[str] = Query(None),
                           userId: Optional[str] = Query(None), skip: int = 0, limit: int = 50,
                           db: Prisma = Depends(get_db), _=Depends(require_role(ADMIN_ONLY))):
    logs = await service.list_audit_logs(db, module, action, userId, skip, limit)
    return {"data": logs, "error": None, "meta": {"total": len(logs)}}


# ── Layouts ───────────────────────────────────────────────────────────────────

@router.post("/layouts", status_code=201)
async def upsert_layout(body: schemas.LayoutCreate, db: Prisma = Depends(get_db),
                         current_user=Depends(require_role(ADMIN_ONLY))):
    layout = await service.upsert_layout(db, body, current_user.id)
    return {"data": layout, "error": None, "meta": {}}
