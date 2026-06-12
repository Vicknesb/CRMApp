import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_lead(auth_client: AsyncClient):
    resp = await auth_client.post("/api/v1/leads", json={
        "firstName": "Test", "lastName": "Lead", "email": "lead@test.com",
        "company": "TestCo", "source": "WEBSITE"
    })
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["email"] == "lead@test.com"
    return data["id"]


@pytest.mark.asyncio
async def test_list_leads(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/leads")
    assert resp.status_code == 200
    body = resp.json()
    assert "data" in body
    assert "meta" in body


@pytest.mark.asyncio
async def test_update_lead(auth_client: AsyncClient):
    create = await auth_client.post("/api/v1/leads", json={
        "firstName": "Up", "lastName": "Lead", "email": "uplead@test.com",
        "company": "TestCo", "source": "REFERRAL"
    })
    lead_id = create.json()["data"]["id"]
    resp = await auth_client.patch(f"/api/v1/leads/{lead_id}", json={"firstName": "Updated"})
    assert resp.status_code == 200
    assert resp.json()["data"]["firstName"] == "Updated"


@pytest.mark.asyncio
async def test_delete_lead(auth_client: AsyncClient):
    create = await auth_client.post("/api/v1/leads", json={
        "firstName": "Del", "lastName": "Lead", "email": "dellead@test.com",
        "company": "TestCo", "source": "EVENT"
    })
    lead_id = create.json()["data"]["id"]
    resp = await auth_client.delete(f"/api/v1/leads/{lead_id}")
    assert resp.status_code == 204
    get_resp = await auth_client.get(f"/api/v1/leads/{lead_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_score_lead(auth_client: AsyncClient):
    create = await auth_client.post("/api/v1/leads", json={
        "firstName": "Score", "lastName": "Lead", "email": "scorelead@test.com",
        "company": "BigCo", "source": "INBOUND"
    })
    lead_id = create.json()["data"]["id"]
    resp = await auth_client.post(f"/api/v1/leads/{lead_id}/score")
    assert resp.status_code == 200
    assert "score" in resp.json()["data"]
