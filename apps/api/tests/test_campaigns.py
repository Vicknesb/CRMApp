import pytest
from decimal import Decimal
from httpx import AsyncClient
from app.modules.campaign.service import get_metrics_summary
from unittest.mock import AsyncMock, MagicMock


# ── Unit: metrics summary rates ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_metrics_open_rate():
    db = AsyncMock()
    metrics = [
        MagicMock(metricKey="sent", value=Decimal("1000")),
        MagicMock(metricKey="opens", value=Decimal("250")),
        MagicMock(metricKey="clicks", value=Decimal("100")),
        MagicMock(metricKey="conversions", value=Decimal("20")),
    ]
    db.campaignmetric.find_many = AsyncMock(return_value=metrics)
    summary = await get_metrics_summary(db, "camp-1")
    assert summary.openRate == 25.0
    assert summary.clickRate == 10.0
    assert summary.conversionRate == 2.0


@pytest.mark.asyncio
async def test_metrics_zero_sent():
    db = AsyncMock()
    db.campaignmetric.find_many = AsyncMock(return_value=[])
    summary = await get_metrics_summary(db, "camp-1")
    assert summary.openRate == 0.0
    assert summary.sent == 0


# ── Integration: API endpoints ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_campaigns_empty(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/campaigns")
    assert resp.status_code == 200
    assert "data" in resp.json()


@pytest.mark.asyncio
async def test_create_campaign(auth_client: AsyncClient):
    resp = await auth_client.post("/api/v1/campaigns", json={
        "name": "Q3 Email Blast",
        "type": "EMAIL",
        "status": "DRAFT",
        "currency": "INR",
    })
    if resp.status_code == 403:
        pytest.skip("Role restriction")
    assert resp.status_code == 201
    campaign_id = resp.json()["data"]["id"]

    # Add segment
    resp = await auth_client.post(f"/api/v1/campaigns/{campaign_id}/segments", json={
        "name": "IT Decision Makers",
        "filters": {"industry": "Technology", "tier": "ENTERPRISE"},
    })
    assert resp.status_code in (201, 403)

    # Ingest metric
    resp = await auth_client.post(f"/api/v1/campaigns/{campaign_id}/metrics", json={
        "metricKey": "sent", "value": "500",
    })
    assert resp.status_code in (201, 403)


@pytest.mark.asyncio
async def test_campaign_not_found(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/campaigns/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404
