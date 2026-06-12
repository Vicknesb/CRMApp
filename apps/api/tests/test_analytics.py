import pytest
from httpx import AsyncClient
from app.modules.analytics.service import ALLOWED_MODULES, run_custom_report
from app.modules.analytics.schemas import CustomReportDefinition, ReportFilter
from unittest.mock import AsyncMock, MagicMock


# ── Unit: allowed module/field guard ─────────────────────────────────────────

@pytest.mark.asyncio
async def test_custom_report_rejects_unknown_module():
    from fastapi import HTTPException
    db = AsyncMock()
    defn = CustomReportDefinition(module="users", fields=["id", "passwordHash"])
    with pytest.raises(HTTPException) as exc:
        await run_custom_report(db, defn)
    assert exc.value.status_code == 422


@pytest.mark.asyncio
async def test_custom_report_rejects_disallowed_field():
    from fastapi import HTTPException
    db = AsyncMock()
    defn = CustomReportDefinition(module="leads", fields=["id", "passwordHash"])
    with pytest.raises(HTTPException) as exc:
        await run_custom_report(db, defn)
    assert exc.value.status_code == 422


def test_all_allowed_modules_defined():
    assert "leads" in ALLOWED_MODULES
    assert "opportunities" in ALLOWED_MODULES
    assert "invoices" in ALLOWED_MODULES


# ── Integration: API endpoints ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_dashboard_endpoint(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/analytics/dashboard")
    assert resp.status_code == 200
    body = resp.json()
    assert "data" in body
    assert "widgets" in body["data"]


@pytest.mark.asyncio
async def test_list_reports(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/analytics/reports")
    assert resp.status_code == 200
    keys = resp.json()["data"]
    assert "pipeline_summary" in keys
    assert "invoice_aging" in keys
    assert len(keys) == 10


@pytest.mark.asyncio
async def test_prebuilt_report_ticket_volume(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/analytics/reports/ticket_volume")
    assert resp.status_code == 200
    data = resp.json()["data"]["data"]
    assert "OPEN" in data


@pytest.mark.asyncio
async def test_unknown_report_returns_404(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/analytics/reports/nonexistent_report")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_custom_report_injection_blocked(auth_client: AsyncClient):
    resp = await auth_client.post("/api/v1/analytics/reports/run", json={
        "module": "leads",
        "fields": ["id", "passwordHash"],
    })
    assert resp.status_code == 422
