import pytest
from datetime import datetime, timezone, timedelta
from httpx import AsyncClient
from app.modules.contract.service import get_renewal_reminders
from unittest.mock import AsyncMock, MagicMock


# ── Unit: renewal reminder detection ─────────────────────────────────────────

@pytest.mark.asyncio
async def test_renewal_reminders_within_90_days():
    db = AsyncMock()
    now = datetime.now(timezone.utc)
    c = MagicMock()
    c.id = "c1"
    c.number = "CONTR-2026-001"
    c.title = "Support Contract"
    c.endDate = now + timedelta(days=45)
    c.autoRenew = True
    db.contract.find_many = AsyncMock(return_value=[c])

    reminders = await get_renewal_reminders(db, 90)
    assert len(reminders) == 1
    assert reminders[0].daysUntilExpiry <= 90
    assert reminders[0].autoRenew is True


@pytest.mark.asyncio
async def test_renewal_reminders_empty():
    db = AsyncMock()
    db.contract.find_many = AsyncMock(return_value=[])
    reminders = await get_renewal_reminders(db, 30)
    assert reminders == []


# ── Unit: contract number format ─────────────────────────────────────────────

def test_contract_number_format():
    from app.modules.contract.service import _gen_number
    number = _gen_number()
    year = datetime.now(timezone.utc).year
    assert number.startswith(f"CONTR-{year}-")
    assert len(number) == len(f"CONTR-{year}-") + 6


# ── Integration: API endpoints ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_contracts_empty(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/contracts")
    assert resp.status_code == 200
    assert "data" in resp.json()


@pytest.mark.asyncio
async def test_contract_crud(auth_client: AsyncClient):
    payload = {
        "title": "Annual Support Agreement",
        "startDate": "2026-01-01T00:00:00Z",
        "endDate": "2026-12-31T00:00:00Z",
        "value": "500000.00",
        "currency": "INR",
        "autoRenew": True,
    }
    resp = await auth_client.post("/api/v1/contracts", json=payload)
    if resp.status_code == 403:
        pytest.skip("Role restriction")
    assert resp.status_code == 201
    cid = resp.json()["data"]["id"]

    resp = await auth_client.get(f"/api/v1/contracts/{cid}")
    assert resp.status_code == 200
    assert resp.json()["data"]["autoRenew"] is True

    # Add amendment
    resp = await auth_client.post(f"/api/v1/contracts/{cid}/amendments", json={
        "description": "Scope expanded to include cloud services",
        "effectiveAt": "2026-06-01T00:00:00Z",
    })
    assert resp.status_code in (201, 403)


@pytest.mark.asyncio
async def test_renewal_endpoint(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/contracts/renewals?days=90")
    assert resp.status_code == 200
    assert "data" in resp.json()


@pytest.mark.asyncio
async def test_contract_not_found(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/contracts/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404
