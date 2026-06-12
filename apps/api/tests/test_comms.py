import pytest
import re
from httpx import AsyncClient
from app.modules.comms.service import preview_template
from unittest.mock import AsyncMock, MagicMock


# ── Unit: template variable substitution ─────────────────────────────────────

@pytest.mark.asyncio
async def test_template_var_substitution():
    db = AsyncMock()
    tmpl = MagicMock()
    tmpl.subject = "Hello {{name}}"
    tmpl.body = "Dear {{name}}, your ticket {{ticketId}} is resolved."
    db.emailtemplate.find_unique = AsyncMock(return_value=tmpl)
    preview = await preview_template(db, "tmpl-1", {"name": "Ravi", "ticketId": "TKT-001"})
    assert preview.subject == "Hello Ravi"
    assert "Ravi" in preview.body
    assert "TKT-001" in preview.body


@pytest.mark.asyncio
async def test_template_not_found():
    from fastapi import HTTPException
    db = AsyncMock()
    db.emailtemplate.find_unique = AsyncMock(return_value=None)
    with pytest.raises(HTTPException) as exc:
        await preview_template(db, "not-found", {})
    assert exc.value.status_code == 404


# ── Unit: @mention regex ──────────────────────────────────────────────────────

def test_mention_parse():
    content = "Hey @john and @jane, please review this."
    mentions = re.findall(r"@(\w+)", content)
    assert "john" in mentions
    assert "jane" in mentions
    assert len(mentions) == 2


# ── Integration: API endpoints ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_notifications(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/notifications")
    assert resp.status_code == 200
    assert "data" in resp.json()


@pytest.mark.asyncio
async def test_unread_notifications_filter(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/notifications?unread=true")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_add_comment(auth_client: AsyncClient):
    resp = await auth_client.post("/api/v1/comments", json={
        "content": "This is a comment on the lead.",
        "relatedType": "lead",
        "relatedId": "00000000-0000-0000-0000-000000000001",
    })
    assert resp.status_code in (201, 404)


@pytest.mark.asyncio
async def test_list_comments(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/comments?relatedType=lead&relatedId=00000000-0000-0000-0000-000000000001")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_list_email_templates(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/email-templates")
    assert resp.status_code == 200
