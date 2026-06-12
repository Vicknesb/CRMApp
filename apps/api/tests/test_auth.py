import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta, timezone

from app.core.security import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.core.rbac import can, redact_fields
from app.core.enums import UserRole
from app.middleware.error_handler import UnauthorizedError


# ── Security helpers ──────────────────────────────────────────────────────────

def test_password_hash_and_verify() -> None:
    hashed = hash_password("MySecret123")
    assert verify_password("MySecret123", hashed)
    assert not verify_password("WrongPass", hashed)


def test_token_issue_and_verify() -> None:
    token = create_access_token({"sub": "user-123", "role": "SALES_REP"})
    payload = decode_token(token)
    assert payload["sub"] == "user-123"


def test_expired_token_raises() -> None:
    token = create_access_token({"sub": "x"}, expires_delta=timedelta(seconds=-1))
    with pytest.raises(ValueError, match="Invalid or expired token"):
        decode_token(token)


# ── RBAC ability map ──────────────────────────────────────────────────────────

def test_admin_can_do_anything() -> None:
    assert can(UserRole.ADMIN, "leads", "delete")
    assert can(UserRole.ADMIN, "invoices", "delete")
    assert can(UserRole.ADMIN, "admin", "update")


def test_sales_rep_cannot_delete_leads() -> None:
    assert not can(UserRole.SALES_REP, "leads", "delete")


def test_sales_rep_can_read_leads() -> None:
    assert can(UserRole.SALES_REP, "leads", "read")


def test_support_agent_cannot_access_invoices() -> None:
    assert not can(UserRole.SUPPORT_AGENT, "invoices", "read")


def test_read_only_cannot_write() -> None:
    assert not can(UserRole.READ_ONLY, "leads", "create")


# ── Field redaction ───────────────────────────────────────────────────────────

def test_redact_fields_hides_restricted() -> None:
    data = {"id": "1", "score": 90, "firstName": "Test", "utmSource": "google"}
    result = redact_fields(data, "leads", UserRole.SALES_REP)
    assert "score" not in result
    assert "utmSource" not in result
    assert result["firstName"] == "Test"


def test_redact_fields_admin_sees_all() -> None:
    data = {"id": "1", "score": 90, "firstName": "Test"}
    result = redact_fields(data, "leads", UserRole.ADMIN)
    assert result == data


# ── Audit logging ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_audit_failure_swallowed() -> None:
    from app.core.audit import record_audit
    bad_db = MagicMock()
    bad_db.auditlog = MagicMock()
    bad_db.auditlog.create = AsyncMock(side_effect=Exception("DB down"))
    # Should not raise
    await record_audit(bad_db, "user-1", "LOGIN", "auth")


@pytest.mark.asyncio
async def test_audit_row_written() -> None:
    from app.core.audit import record_audit
    mock_db = MagicMock()
    mock_db.auditlog = MagicMock()
    mock_db.auditlog.create = AsyncMock()
    await record_audit(mock_db, "user-1", "UPDATE", "leads", record_id="lead-1",
                       old_values={"status": "NEW"}, new_values={"status": "QUALIFIED"})
    mock_db.auditlog.create.assert_called_once()
    call_args = mock_db.auditlog.create.call_args[1]["data"]
    assert call_args["action"] == "UPDATE"
    assert call_args["module"] == "leads"


# ── Auth service (unit, mocked DB) ───────────────────────────────────────────

@pytest.mark.asyncio
async def test_login_bad_creds_401() -> None:
    from app.modules.auth.service import login
    mock_db = MagicMock()
    mock_db.user = MagicMock()
    mock_db.user.find_first = AsyncMock(return_value=None)
    with pytest.raises(UnauthorizedError, match="Invalid email or password"):
        await login(mock_db, "bad@example.com", "wrongpass", None)


@pytest.mark.asyncio
async def test_register_duplicate_email_raises() -> None:
    from app.modules.auth.service import register
    mock_user = MagicMock()
    mock_db = MagicMock()
    mock_db.user = MagicMock()
    mock_db.user.find_first = AsyncMock(return_value=mock_user)
    with pytest.raises(ValueError, match="Email already registered"):
        await register(mock_db, "dup@example.com", "Password1", "A", "B")
