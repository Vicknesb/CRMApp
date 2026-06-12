from __future__ import annotations
import re
from datetime import datetime, timezone
from typing import Optional, List
from prisma import Prisma
from app.modules.comms.schemas import (
    CommentCreate, EmailTemplateCreate, MentionCreate, TemplatePreview,
)
from app.core.audit import record_audit
from fastapi import HTTPException


# ── Notifications ─────────────────────────────────────────────────────────────

async def list_notifications(db: Prisma, user_id: str, unread_only: bool = False):
    where: dict = {"userId": user_id}
    if unread_only:
        where["readAt"] = None
    return await db.notification.find_many(where=where, order={"createdAt": "desc"}, take=50)


async def mark_read(db: Prisma, notification_id: str, user_id: str):
    notif = await db.notification.find_unique(where={"id": notification_id})
    if not notif or notif.userId != user_id:
        raise HTTPException(status_code=404, detail="Notification not found")
    return await db.notification.update(
        where={"id": notification_id},
        data={"readAt": datetime.now(timezone.utc)},
    )


async def mark_all_read(db: Prisma, user_id: str):
    now = datetime.now(timezone.utc)
    await db.notification.update_many(
        where={"userId": user_id, "readAt": None},
        data={"readAt": now},
    )


async def create_notification(db: Prisma, user_id: str, type_: str, title: str,
                               body: Optional[str] = None, related_type: Optional[str] = None,
                               related_id: Optional[str] = None):
    return await db.notification.create(data={
        "userId": user_id,
        "type": type_,
        "title": title,
        "body": body,
        "relatedType": related_type,
        "relatedId": related_id,
    })


# ── Comments ──────────────────────────────────────────────────────────────────

async def add_comment(db: Prisma, data: CommentCreate, author_id: str):
    comment = await db.comment.create(data={
        "authorId": author_id,
        "content": data.content,
        "relatedType": data.relatedType,
        "relatedId": data.relatedId,
        "parentId": data.parentId,
    })
    # Parse @mentions and notify
    mentions = re.findall(r"@(\w+)", data.content)
    if mentions:
        users = await db.user.find_many(
            where={"OR": [{"firstName": m} for m in mentions]}
        )
        for u in users:
            await create_notification(
                db, u.id, "MENTION",
                f"You were mentioned in a comment",
                related_type=data.relatedType,
                related_id=data.relatedId,
            )
    await record_audit(db, author_id, "CREATE", "comments", record_id=comment.id)
    return comment


async def list_comments(db: Prisma, related_type: str, related_id: str):
    return await db.comment.find_many(
        where={"relatedType": related_type, "relatedId": related_id,
               "parentId": None, "deletedAt": None},
        include={"replies": True},
        order={"createdAt": "asc"},
    )


async def delete_comment(db: Prisma, comment_id: str, actor_id: str):
    comment = await db.comment.find_unique(where={"id": comment_id})
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    await db.comment.update(where={"id": comment_id},
                             data={"deletedAt": datetime.now(timezone.utc)})
    await record_audit(db, actor_id, "DELETE", "comments", record_id=comment_id)


# ── Unified comm log ──────────────────────────────────────────────────────────

async def comm_log(db: Prisma, contact_id: Optional[str] = None,
                   account_id: Optional[str] = None, limit: int = 50):
    where: dict = {}
    if contact_id:
        where["OR"] = [{"relatedType": "contact", "relatedId": contact_id},
                       {"contactId": contact_id}]
    elif account_id:
        where["relatedType"] = "account"
        where["relatedId"] = account_id
    activities = await db.activity.find_many(where=where, order={"happenedAt": "desc"}, take=limit)
    return activities


# ── Email templates ───────────────────────────────────────────────────────────

async def create_template(db: Prisma, data: EmailTemplateCreate, actor_id: str):
    tmpl = await db.emailtemplate.create(data={
        "name": data.name,
        "subject": data.subject,
        "body": data.body,
        "variables": data.variables,
    })
    await record_audit(db, actor_id, "CREATE", "email_templates", record_id=tmpl.id)
    return tmpl


async def list_templates(db: Prisma):
    return await db.emailtemplate.find_many(where={"isActive": True}, order={"name": "asc"})


async def preview_template(db: Prisma, template_id: str, variables: dict) -> TemplatePreview:
    tmpl = await db.emailtemplate.find_unique(where={"id": template_id})
    if not tmpl:
        raise HTTPException(status_code=404, detail="Template not found")
    subject = tmpl.subject
    body = tmpl.body
    for k, v in variables.items():
        subject = subject.replace(f"{{{{{k}}}}}", str(v))
        body = body.replace(f"{{{{{k}}}}}", str(v))
    return TemplatePreview(subject=subject, body=body)
