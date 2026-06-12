"""NFR hardening tests (NFR-1 through NFR-9)."""
import pytest
from app.core.feature_flags import is_enabled
import os


# NFR-1: Performance middleware sets timing header
@pytest.mark.asyncio
async def test_response_time_header(client):
    resp = await client.get("/health/live")
    assert resp.status_code == 200
    assert "X-Response-Time-Ms" in resp.headers


# NFR-2: Security headers present
@pytest.mark.asyncio
async def test_security_headers(client):
    resp = await client.get("/health/live")
    assert resp.headers.get("X-Content-Type-Options") == "nosniff"
    assert resp.headers.get("X-Frame-Options") == "DENY"
    assert "Strict-Transport-Security" in resp.headers


# NFR-3: Liveness probe
@pytest.mark.asyncio
async def test_liveness(client):
    resp = await client.get("/health/live")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


# NFR-3: Readiness probe
@pytest.mark.asyncio
async def test_readiness(client):
    resp = await client.get("/health/ready")
    assert resp.status_code in (200, 503)


# NFR-9: Feature flags default off
def test_flag_off_by_default():
    os.environ.pop("FEATURE_FAKE_FLAG", None)
    assert is_enabled("FAKE_FLAG") is False


def test_flag_on_when_set():
    os.environ["FEATURE_MY_FEAT"] = "true"
    assert is_enabled("MY_FEAT") is True
    del os.environ["FEATURE_MY_FEAT"]


def test_flag_off_explicit():
    os.environ["FEATURE_MY_FEAT"] = "false"
    assert is_enabled("MY_FEAT") is False
    del os.environ["FEATURE_MY_FEAT"]
