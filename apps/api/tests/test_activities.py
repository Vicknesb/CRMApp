import pytest
from httpx import AsyncClient
from datetime import datetime


@pytest.mark.asyncio
async def test_log_activity(auth_client: AsyncClient):
    resp = await auth_client.post("/api/v1/activities", json={
        "type": "EMAIL", "subject": "Sent proposal",
        "happenedAt": datetime.utcnow().isoformat()
    })
    assert resp.status_code == 201
    assert resp.json()["data"]["subject"] == "Sent proposal"


@pytest.mark.asyncio
async def test_list_activities(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/activities")
    assert resp.status_code == 200
    assert "data" in resp.json()


@pytest.mark.asyncio
async def test_create_task(auth_client: AsyncClient):
    resp = await auth_client.post("/api/v1/tasks", json={
        "title": "Follow up call", "priority": "HIGH"
    })
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["title"] == "Follow up call"
    return data["id"]


@pytest.mark.asyncio
async def test_update_task_status(auth_client: AsyncClient):
    create = await auth_client.post("/api/v1/tasks", json={"title": "Complete me"})
    tid = create.json()["data"]["id"]
    resp = await auth_client.patch(f"/api/v1/tasks/{tid}", json={"status": "COMPLETED"})
    assert resp.status_code == 200
    assert resp.json()["data"]["status"] == "COMPLETED"


@pytest.mark.asyncio
async def test_overdue_tasks(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/tasks/overdue")
    assert resp.status_code == 200
    assert "data" in resp.json()


@pytest.mark.asyncio
async def test_delete_task(auth_client: AsyncClient):
    create = await auth_client.post("/api/v1/tasks", json={"title": "Delete me"})
    tid = create.json()["data"]["id"]
    resp = await auth_client.delete(f"/api/v1/tasks/{tid}")
    assert resp.status_code == 204
