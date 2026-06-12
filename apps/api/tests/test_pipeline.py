import pytest
from httpx import AsyncClient


async def _get_first_stage_id(auth_client: AsyncClient) -> str:
    resp = await auth_client.get("/api/v1/stages")
    stages = resp.json().get("data", [])
    if stages:
        return stages[0]["id"]
    return ""


@pytest.mark.asyncio
async def test_create_opportunity(auth_client: AsyncClient):
    stage_id = await _get_first_stage_id(auth_client)
    if not stage_id:
        pytest.skip("No pipeline stages seeded")
    resp = await auth_client.post("/api/v1/opportunities", json={
        "title": "Big Deal", "value": 5000000, "stageId": stage_id
    })
    assert resp.status_code == 201
    assert resp.json()["data"]["title"] == "Big Deal"


@pytest.mark.asyncio
async def test_list_opportunities(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/opportunities")
    assert resp.status_code == 200
    assert "data" in resp.json()


@pytest.mark.asyncio
async def test_forecast(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/opportunities/forecast")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert "totalWeightedValue" in data
    assert "byStage" in data
