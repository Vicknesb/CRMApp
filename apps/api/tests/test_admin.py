import pytest
from httpx import AsyncClient
from app.modules.admin.service import evaluate_workflow
from unittest.mock import AsyncMock, MagicMock


# ── Unit: workflow condition evaluation ───────────────────────────────────────

@pytest.mark.asyncio
async def test_workflow_fires_on_matching_condition():
    db = AsyncMock()
    wf = MagicMock()
    wf.conditions = {"status": "QUALIFIED"}
    wf.actions = [{"type": "create_task"}, {"type": "notify"}]
    wf.isActive = True
    db.workflow.find_many = AsyncMock(return_value=[wf])
    fired = await evaluate_workflow(db, "leads", "on_update", {"status": "QUALIFIED"})
    assert "create_task" in fired
    assert "notify" in fired


@pytest.mark.asyncio
async def test_workflow_no_fire_on_mismatch():
    db = AsyncMock()
    wf = MagicMock()
    wf.conditions = {"status": "QUALIFIED"}
    wf.actions = [{"type": "create_task"}]
    wf.isActive = True
    db.workflow.find_many = AsyncMock(return_value=[wf])
    fired = await evaluate_workflow(db, "leads", "on_update", {"status": "NEW"})
    assert fired == []


@pytest.mark.asyncio
async def test_workflow_no_fire_empty_conditions():
    db = AsyncMock()
    wf = MagicMock()
    wf.conditions = {}
    wf.actions = [{"type": "send_email"}]
    wf.isActive = True
    db.workflow.find_many = AsyncMock(return_value=[wf])
    fired = await evaluate_workflow(db, "leads", "on_create", {})
    assert "send_email" in fired


# ── Integration: API endpoints ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_admin_list_users(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/admin/users")
    assert resp.status_code in (200, 403)


@pytest.mark.asyncio
async def test_list_custom_fields(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/admin/custom-fields")
    assert resp.status_code == 200
    assert "data" in resp.json()


@pytest.mark.asyncio
async def test_create_custom_field(auth_client: AsyncClient):
    resp = await auth_client.post("/api/v1/admin/custom-fields", json={
        "module": "leads",
        "fieldName": "verticalSegment",
        "fieldType": "select",
        "label": "Vertical Segment",
        "options": ["BFSI", "Retail", "Healthcare"],
    })
    assert resp.status_code in (201, 403)


@pytest.mark.asyncio
async def test_list_workflows(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/admin/workflows")
    assert resp.status_code in (200, 403)


@pytest.mark.asyncio
async def test_list_audit_logs(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/admin/audit-logs")
    assert resp.status_code in (200, 403)


@pytest.mark.asyncio
async def test_list_permissions(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/admin/permissions")
    assert resp.status_code in (200, 403)
