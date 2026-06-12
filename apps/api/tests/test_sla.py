import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_sla_policy(auth_client: AsyncClient):
    resp = await auth_client.post("/api/v1/sla/policies", json={
        "name": "Gold SLA", "priority": "HIGH",
        "responseMinutes": 60, "resolutionMinutes": 480, "businessHoursOnly": True
    })
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["name"] == "Gold SLA"


@pytest.mark.asyncio
async def test_list_sla_policies(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/sla/policies")
    assert resp.status_code == 200
    assert "data" in resp.json()


@pytest.mark.asyncio
async def test_compliance_report(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/sla/compliance-report")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert "complianceRate" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_check_breaches(auth_client: AsyncClient):
    resp = await auth_client.post("/api/v1/sla/check-breaches")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert "responseBreachesMarked" in data
