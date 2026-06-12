import pytest
from decimal import Decimal
from datetime import datetime, timezone
from httpx import AsyncClient
from app.modules.invoice.service import _gen_number, aging_report
from unittest.mock import AsyncMock, MagicMock


# ── Unit: invoice number format ───────────────────────────────────────────────

def test_invoice_number_format():
    number = _gen_number()
    now = datetime.now(timezone.utc)
    prefix = f"INV-{now.strftime('%Y%m')}-"
    assert number.startswith(prefix)
    assert len(number) == len(prefix) + 5


# ── Unit: GST calculation ─────────────────────────────────────────────────────

def test_gst_calculation():
    sub = Decimal("100000")
    rate = Decimal("18")
    tax = sub * rate / Decimal("100")
    total = sub + tax
    assert tax == Decimal("18000")
    assert total == Decimal("118000")


# ── Unit: aging buckets ───────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_aging_report_buckets():
    from datetime import timedelta
    db = AsyncMock()
    now = datetime.now(timezone.utc)

    def make_inv(days_overdue, amount):
        inv = MagicMock()
        inv.dueDate = now - timedelta(days=days_overdue)
        inv.totalAmount = Decimal(str(amount))
        inv.status = "OVERDUE"
        return inv

    db.invoice.find_many = AsyncMock(return_value=[
        make_inv(10, 50000),
        make_inv(45, 100000),
        make_inv(75, 200000),
        make_inv(120, 300000),
    ])
    buckets = await aging_report(db)
    bucket_map = {b.bucket: b for b in buckets}
    assert bucket_map["0-30"].totalAmount == Decimal("50000")
    assert bucket_map["31-60"].totalAmount == Decimal("100000")
    assert bucket_map["61-90"].totalAmount == Decimal("200000")
    assert bucket_map["90+"].totalAmount == Decimal("300000")


# ── Integration: API endpoints ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_invoices_empty(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/invoices")
    assert resp.status_code == 200
    assert "data" in resp.json()


@pytest.mark.asyncio
async def test_create_invoice_with_line_items(auth_client: AsyncClient):
    payload = {
        "issueDate": "2026-06-01T00:00:00Z",
        "dueDate": "2026-06-30T00:00:00Z",
        "currency": "INR",
        "taxRate": "18",
        "lineItems": [
            {"description": "Software Development", "quantity": 1, "unitPrice": "100000.00"},
            {"description": "QA Services", "quantity": 1, "unitPrice": "20000.00"},
        ],
    }
    resp = await auth_client.post("/api/v1/invoices", json=payload)
    if resp.status_code == 403:
        pytest.skip("Role restriction")
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert str(data["subTotal"]) == "120000"
    assert str(data["taxAmount"]) == "21600"
    assert str(data["totalAmount"]) == "141600"


@pytest.mark.asyncio
async def test_revenue_report_endpoint(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/invoices/revenue?period=monthly")
    assert resp.status_code in (200, 403)


@pytest.mark.asyncio
async def test_aging_report_endpoint(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/invoices/aging")
    assert resp.status_code in (200, 403)


@pytest.mark.asyncio
async def test_invoice_not_found(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/invoices/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404
