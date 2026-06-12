from fastapi import APIRouter, Depends, Query
from typing import Optional
from prisma import Prisma
from app.db.client import get_db
from app.core.security import get_current_user, require_role
from app.modules.comms import schemas, service

router = APIRouter(tags=["comms"])


# ── Notifications ─────────────────────────────────────────────────────────────

@router.get("/notifications")
async def list_notifications(unread: bool = Query(False),
                              db: Prisma = Depends(get_db),
                              current_user=Depends(get_current_user)):
    notifs = await service.list_notifications(db, current_user.id, unread)
    return {"data": notifs, "error": None, "meta": {"total": len(notifs)}}


@router.patch("/notifications/{notification_id}/read")
async def mark_read(notification_id: str, db: Prisma = Depends(get_db),
                    current_user=Depends(get_current_user)):
    notif = await service.mark_read(db, notification_id, current_user.id)
    return {"data": notif, "error": None, "meta": {}}


@router.post("/notifications/read-all", status_code=204)
async def mark_all_read(db: Prisma = Depends(get_db), current_user=Depends(get_current_user)):
    await service.mark_all_read(db, current_user.id)


# ── Comments ──────────────────────────────────────────────────────────────────

@router.post("/comments", status_code=201)
async def add_comment(body: schemas.CommentCreate, db: Prisma = Depends(get_db),
                       current_user=Depends(get_current_user)):
    comment = await service.add_comment(db, body, current_user.id)
    return {"data": comment, "error": None, "meta": {}}


@router.get("/comments")
async def list_comments(relatedType: str = Query(...), relatedId: str = Query(...),
                         db: Prisma = Depends(get_db), _=Depends(get_current_user)):
    comments = await service.list_comments(db, relatedType, relatedId)
    return {"data": comments, "error": None, "meta": {}}


@router.delete("/comments/{comment_id}", status_code=204)
async def delete_comment(comment_id: str, db: Prisma = Depends(get_db),
                          current_user=Depends(get_current_user)):
    await service.delete_comment(db, comment_id, current_user.id)


# ── Comm log ──────────────────────────────────────────────────────────────────

@router.get("/comm-log")
async def comm_log(contactId: Optional[str] = Query(None),
                   accountId: Optional[str] = Query(None),
                   db: Prisma = Depends(get_db), _=Depends(get_current_user)):
    activities = await service.comm_log(db, contactId, accountId)
    return {"data": activities, "error": None, "meta": {}}


# ── Email templates ───────────────────────────────────────────────────────────

@router.get("/email-templates")
async def list_templates(db: Prisma = Depends(get_db), _=Depends(get_current_user)):
    templates = await service.list_templates(db)
    return {"data": templates, "error": None, "meta": {}}


@router.post("/email-templates", status_code=201)
async def create_template(body: schemas.EmailTemplateCreate,
                           db: Prisma = Depends(get_db),
                           current_user=Depends(require_role(["ADMIN", "MARKETING"]))):
    tmpl = await service.create_template(db, body, current_user.id)
    return {"data": tmpl, "error": None, "meta": {}}


@router.post("/email-templates/{template_id}/preview")
async def preview_template(template_id: str, variables: dict,
                            db: Prisma = Depends(get_db), _=Depends(get_current_user)):
    preview = await service.preview_template(db, template_id, variables)
    return {"data": preview, "error": None, "meta": {}}
