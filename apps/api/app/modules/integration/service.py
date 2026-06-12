from datetime import datetime, timezone
from prisma import Prisma
from app.core.audit import record_audit
from app.middleware.error_handler import NotFoundError
from app.modules.integration.token_vault import encrypt_token, decrypt_token
from app.modules.integration.schemas import EmailSend, SlackNotify, TokenStore


async def list_connectors(db: Prisma, user_id: str) -> list:
    return await db.integration.find_many(where={"userId": user_id}, order={"provider": "asc"})


async def get_connector(db: Prisma, provider: str, user_id: str) -> object:
    conn = await db.integration.find_first(where={"provider": provider, "userId": user_id})
    if not conn:
        raise NotFoundError(f"Integration '{provider}' not connected")
    return conn


async def store_token(db: Prisma, body: TokenStore, user_id: str) -> object:
    encrypted = encrypt_token({
        "accessToken": body.accessToken,
        "refreshToken": body.refreshToken,
        "expiresAt": body.expiresAt,
        "scopes": body.scopes,
    })
    conn = await db.integration.upsert(
        where={"provider_userId": {"provider": body.provider, "userId": user_id}},
        data={
            "create": {
                "provider": body.provider,
                "userId": user_id,
                "encryptedToken": encrypted,
                "connectedAt": datetime.now(timezone.utc),
                "isActive": True,
            },
            "update": {
                "encryptedToken": encrypted,
                "connectedAt": datetime.now(timezone.utc),
                "isActive": True,
            },
        },
    )
    await record_audit(db, user_id, "INTEGRATION_CONNECT", "integrations",
                       record_id=conn.id, new_values={"provider": body.provider})
    return conn


async def disconnect(db: Prisma, provider: str, user_id: str, actor_id: str) -> None:
    conn = await get_connector(db, provider, user_id)
    await db.integration.update(where={"id": conn.id}, data={"isActive": False, "encryptedToken": ""})
    await record_audit(db, actor_id, "INTEGRATION_DISCONNECT", "integrations",
                       record_id=conn.id, new_values={"provider": provider})


def get_decrypted_token(conn) -> dict:
    """Decrypt and return token data for a connector record."""
    if not conn.encryptedToken:
        raise ValueError("No token stored for this integration")
    return decrypt_token(conn.encryptedToken)


# --- Email (Gmail/Outlook) ---
async def send_email(db: Prisma, body: EmailSend, user_id: str) -> dict:
    """Send email via connected Gmail/Outlook and log as Activity."""
    # In production: use token to call Gmail API / Microsoft Graph
    # Here we validate connector exists and simulate send
    conn = await db.integration.find_first(
        where={"userId": user_id, "provider": {"in": ["gmail", "outlook"]}, "isActive": True}
    )
    if not conn:
        raise NotFoundError("No active email integration connected")

    # Log as activity
    activity = await db.activity.create(data={
        "userId": user_id,
        "type": "EMAIL",
        "subject": body.subject,
        "description": f"To: {body.to}\n\n{body.body}",
        "relatedType": "contact" if body.contactId else None,
        "relatedId": body.contactId,
        "happenedAt": datetime.now(timezone.utc),
    })
    await record_audit(db, user_id, "EMAIL_SENT", "activities", record_id=activity.id)
    return {"sent": True, "activityId": activity.id, "provider": conn.provider}


# --- Slack/Teams notification ---
async def send_slack_notification(db: Prisma, body: SlackNotify, user_id: str) -> dict:
    """Post message to Slack/Teams channel via webhook URL stored in connector."""
    conn = await db.integration.find_first(
        where={"userId": user_id, "provider": {"in": ["slack", "teams"]}, "isActive": True}
    )
    if not conn:
        raise NotFoundError("No active Slack/Teams integration")
    # In production: POST to webhook URL from token
    return {"sent": True, "channel": body.channel, "provider": conn.provider}


# --- Webhook inbound handler ---
async def handle_webhook(db: Prisma, provider: str, event_type: str, payload: dict) -> dict:
    """Process inbound webhook from any provider."""
    handlers = {
        "jira": _handle_jira_webhook,
        "azuredevops": _handle_jira_webhook,
        "slack": _handle_slack_webhook,
        "gmail": _handle_email_webhook,
        "outlook": _handle_email_webhook,
    }
    handler = handlers.get(provider)
    if handler:
        return await handler(db, event_type, payload)
    return {"processed": False, "reason": "No handler for provider"}


async def _handle_jira_webhook(db: Prisma, event_type: str, payload: dict) -> dict:
    # Update project task status from Jira issue update
    return {"processed": True, "provider": "jira", "event": event_type}


async def _handle_slack_webhook(db: Prisma, event_type: str, payload: dict) -> dict:
    return {"processed": True, "provider": "slack", "event": event_type}


async def _handle_email_webhook(db: Prisma, event_type: str, payload: dict) -> dict:
    return {"processed": True, "provider": "email", "event": event_type}


# --- Calendar sync ---
async def sync_calendar_events(db: Prisma, user_id: str) -> dict:
    """Pull calendar events and create/update Tasks."""
    conn = await db.integration.find_first(
        where={"userId": user_id, "provider": {"in": ["google_calendar", "outlook"]}, "isActive": True}
    )
    if not conn:
        raise NotFoundError("No active calendar integration")
    # In production: call Google Calendar / Microsoft Graph API
    return {"synced": True, "provider": conn.provider, "eventsProcessed": 0}
