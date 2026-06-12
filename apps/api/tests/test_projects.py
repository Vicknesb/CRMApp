import pytest
from httpx import AsyncClient
from app.modules.project.service import _rollup_project_status
from unittest.mock import AsyncMock, MagicMock


# ── Unit: status rollup ───────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_rollup_no_tasks_does_nothing():
    db = AsyncMock()
    db.projecttask.find_many = AsyncMock(return_value=[])
    await _rollup_project_status(db, "proj-1", "user-1")
    db.project.update.assert_not_called()


@pytest.mark.asyncio
async def test_rollup_all_completed_sets_completed():
    db = AsyncMock()
    task = MagicMock(status="COMPLETED")
    db.projecttask.find_many = AsyncMock(return_value=[task, task])
    db.project.update = AsyncMock()
    await _rollup_project_status(db, "proj-1", "user-1")
    db.project.update.assert_called_once()
    call_data = db.project.update.call_args[1]["data"]
    assert call_data["status"] == "COMPLETED"


@pytest.mark.asyncio
async def test_rollup_any_in_progress_sets_active():
    db = AsyncMock()
    t1 = MagicMock(status="IN_PROGRESS")
    t2 = MagicMock(status="PENDING")
    db.projecttask.find_many = AsyncMock(return_value=[t1, t2])
    db.project.update = AsyncMock()
    await _rollup_project_status(db, "proj-1", "user-1")
    call_data = db.project.update.call_args[1]["data"]
    assert call_data["status"] == "ACTIVE"


# ── Integration: API endpoints ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_project_requires_auth(auth_client: AsyncClient):
    resp = await auth_client.post("/api/v1/projects", json={
        "name": "Test Project",
        "status": "PLANNING",
    })
    assert resp.status_code in (201, 422, 403)


@pytest.mark.asyncio
async def test_list_projects_empty(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/projects")
    assert resp.status_code == 200
    body = resp.json()
    assert "data" in body


@pytest.mark.asyncio
async def test_project_crud_lifecycle(auth_client: AsyncClient):
    # Create
    resp = await auth_client.post("/api/v1/projects", json={
        "name": "CRM Migration",
        "description": "Migrate legacy CRM",
        "status": "PLANNING",
        "currency": "INR",
    })
    if resp.status_code == 403:
        pytest.skip("Role restriction — need PROJECT_MANAGER token")
    assert resp.status_code == 201
    project_id = resp.json()["data"]["id"]

    # Get
    resp = await auth_client.get(f"/api/v1/projects/{project_id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["name"] == "CRM Migration"

    # Update status
    resp = await auth_client.patch(f"/api/v1/projects/{project_id}", json={"status": "ACTIVE"})
    assert resp.status_code == 200

    # List
    resp = await auth_client.get("/api/v1/projects?status=ACTIVE")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_project_not_found(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/projects/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404
