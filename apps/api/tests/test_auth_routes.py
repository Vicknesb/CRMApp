import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.mark.asyncio
async def test_health_still_ok(client: AsyncClient) -> None:
    res = await client.get("/health")
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_session_without_cookie_returns_error(client: AsyncClient) -> None:
    res = await client.get("/auth/session")
    assert res.status_code == 200
    body = res.json()
    assert body["error"] is not None


@pytest.mark.asyncio
async def test_protected_route_without_cookie_returns_401(client: AsyncClient) -> None:
    res = await client.post("/auth/2fa/setup")
    assert res.status_code == 401
