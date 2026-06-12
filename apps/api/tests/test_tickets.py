import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_ticket(auth_client: AsyncClient):
    resp = await auth_client.post("/api/v1/tickets", json={
        "subject": "Cannot login to portal",
        "channel": "EMAIL",
        "priority": "HIGH",
    })
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["subject"] == "Cannot login to portal"
    assert data["ticketNumber"].startswith("TKT-")


@pytest.mark.asyncio
async def test_list_tickets(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/tickets")
    assert resp.status_code == 200
    assert "data" in resp.json()


@pytest.mark.asyncio
async def test_update_ticket_status(auth_client: AsyncClient):
    create = await auth_client.post("/api/v1/tickets", json={
        "subject": "Resolve me", "channel": "PORTAL", "priority": "MEDIUM"
    })
    tid = create.json()["data"]["id"]
    resp = await auth_client.patch(f"/api/v1/tickets/{tid}", json={"status": "RESOLVED"})
    assert resp.status_code == 200
    assert resp.json()["data"]["status"] == "RESOLVED"


@pytest.mark.asyncio
async def test_add_note(auth_client: AsyncClient):
    create = await auth_client.post("/api/v1/tickets", json={
        "subject": "Note ticket", "channel": "PHONE", "priority": "LOW"
    })
    tid = create.json()["data"]["id"]
    resp = await auth_client.post(f"/api/v1/tickets/{tid}/notes",
                                  json={"body": "Investigated the issue.", "isInternal": True})
    assert resp.status_code == 201
    assert resp.json()["data"]["body"] == "Investigated the issue."


@pytest.mark.asyncio
async def test_list_notes(auth_client: AsyncClient):
    create = await auth_client.post("/api/v1/tickets", json={
        "subject": "Notes list", "channel": "MANUAL", "priority": "LOW"
    })
    tid = create.json()["data"]["id"]
    await auth_client.post(f"/api/v1/tickets/{tid}/notes",
                           json={"body": "First note", "isInternal": False})
    resp = await auth_client.get(f"/api/v1/tickets/{tid}/notes")
    assert resp.status_code == 200
    assert len(resp.json()["data"]) >= 1


@pytest.mark.asyncio
async def test_search_tickets(auth_client: AsyncClient):
    await auth_client.post("/api/v1/tickets", json={
        "subject": "Unique search term XYZ123", "channel": "EMAIL", "priority": "LOW"
    })
    resp = await auth_client.get("/api/v1/tickets", params={"search": "XYZ123"})
    assert resp.status_code == 200
    assert resp.json()["meta"]["total"] >= 1
