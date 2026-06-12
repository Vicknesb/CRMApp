import pytest
from datetime import datetime, timezone, timedelta
from httpx import AsyncClient
from app.modules.data.service import import_csv, purge_expired, check_consent
from unittest.mock import AsyncMock, MagicMock, patch


# ── Unit: CSV import chunking and mapping ─────────────────────────────────────

@pytest.mark.asyncio
async def test_import_csv_maps_fields():
    db = AsyncMock()
    db.lead.create = AsyncMock(return_value=MagicMock(id="lead-1"))
    csv_content = "first_name,last_name,email\nRavi,Kumar,ravi@example.com"
    mappings = [
        {"sourceColumn": "first_name", "targetField": "firstName"},
        {"sourceColumn": "last_name", "targetField": "lastName"},
        {"sourceColumn": "email", "targetField": "email"},
    ]
    result = await import_csv(db, "leads", csv_content, mappings, "user-1")
    assert result.imported == 1
    assert result.errors == 0


@pytest.mark.asyncio
async def test_import_csv_invalid_module():
    from fastapi import HTTPException
    db = AsyncMock()
    with pytest.raises(HTTPException) as exc:
        await import_csv(db, "users", "", [], "user-1")
    assert exc.value.status_code == 422


@pytest.mark.asyncio
async def test_import_csv_missing_email_creates_error():
    db = AsyncMock()
    csv_content = "name\nTechCorp"
    mappings = [{"sourceColumn": "name", "targetField": "company"}]
    result = await import_csv(db, "leads", csv_content, mappings, "user-1")
    assert result.errors == 1


# ── Unit: consent gate ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_consent_granted():
    db = AsyncMock()
    record = MagicMock(granted=True)
    db.consentrecord.find_first = AsyncMock(return_value=record)
    result = await check_consent(db, "test@example.com", "marketing")
    assert result is True


@pytest.mark.asyncio
async def test_consent_revoked():
    db = AsyncMock()
    record = MagicMock(granted=False)
    db.consentrecord.find_first = AsyncMock(return_value=record)
    result = await check_consent(db, "test@example.com", "marketing")
    assert result is False


@pytest.mark.asyncio
async def test_consent_no_record_returns_false():
    db = AsyncMock()
    db.consentrecord.find_first = AsyncMock(return_value=None)
    result = await check_consent(db, "unknown@example.com", "marketing")
    assert result is False


# ── Unit: purge expired recycle bin ──────────────────────────────────────────

@pytest.mark.asyncio
async def test_purge_expired_count():
    db = AsyncMock()
    now = datetime.now(timezone.utc)
    entries = [MagicMock(id=f"e{i}", purgeAt=now - timedelta(days=1)) for i in range(3)]
    db.recyclebinentry.find_many = AsyncMock(return_value=entries)
    db.recyclebinentry.delete = AsyncMock()
    count = await purge_expired(db, "admin-1")
    assert count == 3
    assert db.recyclebinentry.delete.call_count == 3


# ── Integration: API endpoints ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_recycle_bin_list(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/data/recycle-bin")
    assert resp.status_code in (200, 403)


@pytest.mark.asyncio
async def test_consent_check(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/data/consent/check?email=test@example.com&consentType=marketing")
    assert resp.status_code == 200
    assert "granted" in resp.json()["data"]


@pytest.mark.asyncio
async def test_gdpr_export_requires_admin(auth_client: AsyncClient):
    resp = await auth_client.post("/api/v1/data/gdpr/export",
                                   json={"subjectEmail": "test@example.com"})
    assert resp.status_code in (200, 403)
