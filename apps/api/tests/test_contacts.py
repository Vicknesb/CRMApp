import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_contact(auth_client: AsyncClient):
    resp = await auth_client.post("/api/v1/contacts", json={
        "firstName": "Jane", "lastName": "Doe", "email": "jane@test.com"
    })
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["email"] == "jane@test.com"


@pytest.mark.asyncio
async def test_list_contacts(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/contacts")
    assert resp.status_code == 200
    assert "data" in resp.json()


@pytest.mark.asyncio
async def test_update_contact(auth_client: AsyncClient):
    create = await auth_client.post("/api/v1/contacts", json={
        "firstName": "Bob", "lastName": "Smith", "email": "bob@test.com"
    })
    cid = create.json()["data"]["id"]
    resp = await auth_client.patch(f"/api/v1/contacts/{cid}", json={"title": "CTO"})
    assert resp.status_code == 200
    assert resp.json()["data"]["title"] == "CTO"


@pytest.mark.asyncio
async def test_delete_contact(auth_client: AsyncClient):
    create = await auth_client.post("/api/v1/contacts", json={
        "firstName": "Del", "lastName": "Contact", "email": "delcon@test.com"
    })
    cid = create.json()["data"]["id"]
    resp = await auth_client.delete(f"/api/v1/contacts/{cid}")
    assert resp.status_code == 204
