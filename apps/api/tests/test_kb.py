import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_article(auth_client: AsyncClient):
    resp = await auth_client.post("/api/v1/kb/articles", json={
        "title": "How to reset your password",
        "body": "Go to login page and click Forgot Password.",
        "isPublished": True,
    })
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["title"] == "How to reset your password"


@pytest.mark.asyncio
async def test_list_articles(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/kb/articles", params={"published_only": False})
    assert resp.status_code == 200
    assert "data" in resp.json()


@pytest.mark.asyncio
async def test_search_articles(auth_client: AsyncClient):
    await auth_client.post("/api/v1/kb/articles", json={
        "title": "VPN Setup Guide", "body": "Install the VPN client...", "isPublished": True
    })
    resp = await auth_client.get("/api/v1/kb/articles", params={"search": "VPN", "published_only": True})
    assert resp.status_code == 200
    assert resp.json()["meta"]["total"] >= 1


@pytest.mark.asyncio
async def test_suggest_articles(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/kb/articles/suggest", params={"subject": "password reset"})
    assert resp.status_code == 200
    assert "data" in resp.json()


@pytest.mark.asyncio
async def test_rate_article(auth_client: AsyncClient):
    create = await auth_client.post("/api/v1/kb/articles", json={
        "title": "Rate me", "body": "Content here.", "isPublished": True
    })
    aid = create.json()["data"]["id"]
    resp = await auth_client.post(f"/api/v1/kb/articles/{aid}/rate", json={"helpful": True})
    assert resp.status_code == 201
    assert resp.json()["data"]["helpful"] is True
