from fastapi import APIRouter, Depends, Header, Request, status
from prisma import Prisma
from typing import Optional

from app.core.dependencies import get_current_user
from app.core.envelope import ok
from app.db.client import get_db
from app.modules.integration import service
from app.modules.integration.schemas import EmailSend, SlackNotify, TokenStore, WebhookEvent
from app.modules.integration.webhook import (
    verify_slack_signature, verify_github_signature, SUPPORTED_PROVIDERS
)

router = APIRouter(prefix="/integrations", tags=["integrations"])


@router.get("")
async def list_connectors(db: Prisma = Depends(get_db),
                          current_user=Depends(get_current_user)) -> dict:
    conns = await service.list_connectors(db, current_user.id)
    return ok([{"id": c.id, "provider": c.provider, "isActive": c.isActive,
                "connectedAt": str(c.connectedAt)} for c in conns])


@router.post("/connect", status_code=status.HTTP_201_CREATED)
async def connect(body: TokenStore, db: Prisma = Depends(get_db),
                  current_user=Depends(get_current_user)) -> dict:
    conn = await service.store_token(db, body, current_user.id)
    return ok({"id": conn.id, "provider": conn.provider, "isActive": conn.isActive})


@router.delete("/{provider}")
async def disconnect(provider: str, db: Prisma = Depends(get_db),
                     current_user=Depends(get_current_user)) -> dict:
    await service.disconnect(db, provider, current_user.id, current_user.id)
    return ok({"disconnected": True, "provider": provider})


@router.post("/email/send", status_code=status.HTTP_201_CREATED)
async def send_email(body: EmailSend, db: Prisma = Depends(get_db),
                     current_user=Depends(get_current_user)) -> dict:
    return ok(await service.send_email(db, body, current_user.id))


@router.post("/slack/notify", status_code=status.HTTP_201_CREATED)
async def slack_notify(body: SlackNotify, db: Prisma = Depends(get_db),
                       current_user=Depends(get_current_user)) -> dict:
    return ok(await service.send_slack_notification(db, body, current_user.id))


@router.post("/calendar/sync")
async def calendar_sync(db: Prisma = Depends(get_db),
                        current_user=Depends(get_current_user)) -> dict:
    return ok(await service.sync_calendar_events(db, current_user.id))


@router.post("/webhook/{provider}", status_code=status.HTTP_200_OK)
async def receive_webhook(
    provider: str,
    request: Request,
    body: WebhookEvent,
    db: Prisma = Depends(get_db),
    x_slack_signature: Optional[str] = Header(None),
    x_slack_request_timestamp: Optional[str] = Header(None),
    x_hub_signature_256: Optional[str] = Header(None),
) -> dict:
    if provider not in SUPPORTED_PROVIDERS:
        return ok({"processed": False, "reason": "Unknown provider"})
    raw_body = await request.body()
    # Signature verification (secrets loaded from env in production)
    if provider == "slack" and x_slack_signature and x_slack_request_timestamp:
        secret = "SLACK_SIGNING_SECRET"  # from env in production
        if not verify_slack_signature(raw_body, x_slack_request_timestamp,
                                      x_slack_signature, secret):
            from fastapi import HTTPException
            raise HTTPException(status_code=401, detail="Invalid Slack signature")
    elif provider in ("jira", "azuredevops") and x_hub_signature_256:
        secret = "JIRA_WEBHOOK_SECRET"  # from env in production
        if not verify_github_signature(raw_body, x_hub_signature_256, secret):
            from fastapi import HTTPException
            raise HTTPException(status_code=401, detail="Invalid webhook signature")

    result = await service.handle_webhook(db, provider, body.eventType, body.payload)
    return ok(result)
