import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_account(auth_client: AsyncClient):
    resp = await auth_client.post("/api/v1/accounts", json={
        "name": "Infosys Ltd", "industry": "IT Services", "type": "ENTERPRISE"
    })
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["name"] == "Infosys Ltd"


@pytest.mark.asyncio
async def test_list_accounts(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/accounts")
    assert resp.status_code == 200
    assert "data" in resp.json()


@pytest.mark.asyncio
async def test_update_account(auth_client: AsyncClient):
    create = await auth_client.post("/api/v1/accounts", json={"name": "WiproTest"})
    aid = create.json()["data"]["id"]
    resp = await auth_client.patch(f"/api/v1/accounts/{aid}", json={"employees": 50000})
    assert resp.status_code == 200
    assert resp.json()["data"]["employees"] == 50000


@pytest.mark.asyncio
async def test_health_score(auth_client: AsyncClient):
    create = await auth_client.post("/api/v1/accounts", json={"name": "HealthScoreTest"})
    aid = create.json()["data"]["id"]
    resp = await auth_client.post(f"/api/v1/accounts/{aid}/health-score")
    assert resp.status_code == 200
    assert "healthScore" in resp.json()["data"]


@pytest.mark.asyncio
async def test_delete_account(auth_client: AsyncClient):
    create = await auth_client.post("/api/v1/accounts", json={"name": "ToDelete"})
    aid = create.json()["data"]["id"]
    resp = await auth_client.delete(f"/api/v1/accounts/{aid}")
    assert resp.status_code == 204
