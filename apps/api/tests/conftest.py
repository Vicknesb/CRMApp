import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def client() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
async def auth_client() -> AsyncClient:
    """Client pre-authenticated as the seeded admin user."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        resp = await ac.post("/auth/login", json={
            "email": "admin@crm.local", "password": "Admin@123456"
        })
        # If 2FA is enforced, skip token injection — tests requiring a real DB
        # with seed data will handle auth via cookie set by /auth/login.
        if resp.status_code == 200:
            body = resp.json()
            # requires2FA flag means we can't complete auth without TOTP
            if body.get("data", {}).get("requires2FA"):
                pytest.skip("2FA required — seed admin without 2FA for integration tests")
        yield ac
