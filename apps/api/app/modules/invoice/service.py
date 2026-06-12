from __future__ import annotations
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import Optional, List
from prisma import Prisma
from app.modules.invoice.schemas import (
    InvoiceCreate, InvoiceUpdate, PaymentCreate,
    RevenueReport, AgingBucket,
)
from app.core.audit import record_audit
from fastapi import HTTPException
import random, string


def _gen_number() -> str:
    now = datetime.now(timezone.utc)
    suffix = "".join(random.choices(string.digits, k=5))
    return f"INV-{now.strftime('%Y%m')}-{suffix}"


async def create_invoice(db: Prisma, data: InvoiceCreate, actor_id: str):
    number = _gen_number()
    sub_total = sum(item.unitPrice * item.quantity for item in data.lineItems)
    tax_amount = sub_total * data.taxRate / Decimal("100")
    total = sub_total + tax_amount

    invoice = await db.invoice.create(data={
        "number": number,
        "accountId": data.accountId,
        "contractId": data.contractId,
        "opportunityId": data.opportunityId,
        "issueDate": data.issueDate,
        "dueDate": data.dueDate,
        "subTotal": sub_total,
        "taxRate": data.taxRate,
        "taxAmount": tax_amount,
        "totalAmount": total,
        "currency": data.currency.value,
        "notes": data.notes,
    })

    for item in data.lineItems:
        await db.invoicelineitem.create(data={
            "invoiceId": invoice.id,
            "description": item.description,
            "quantity": item.quantity,
            "unitPrice": item.unitPrice,
            "total": item.unitPrice * item.quantity,
            "hsnCode": item.hsnCode,
        })

    await record_audit(db, actor_id, "CREATE", "invoices", record_id=invoice.id)
    return await get_invoice(db, invoice.id)


async def get_invoice(db: Prisma, invoice_id: str):
    invoice = await db.invoice.find_first(
        where={"id": invoice_id, "deletedAt": None},
        include={"lineItems": True, "payments": True},
    )
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


async def list_invoices(db: Prisma, status: Optional[str] = None, account_id: Optional[str] = None,
                        skip: int = 0, limit: int = 50):
    where: dict = {"deletedAt": None}
    if status:
        where["status"] = status
    if account_id:
        where["accountId"] = account_id
    return await db.invoice.find_many(where=where, skip=skip, take=limit, order={"createdAt": "desc"})


async def update_invoice(db: Prisma, invoice_id: str, data: InvoiceUpdate, actor_id: str):
    await get_invoice(db, invoice_id)
    payload = {k: v for k, v in data.model_dump(exclude_none=True).items()}
    if "status" in payload:
        payload["status"] = payload["status"].value
    invoice = await db.invoice.update(where={"id": invoice_id}, data=payload)
    await record_audit(db, actor_id, "UPDATE", "invoices", record_id=invoice_id)
    return invoice


async def delete_invoice(db: Prisma, invoice_id: str, actor_id: str):
    await get_invoice(db, invoice_id)
    await db.invoice.update(where={"id": invoice_id},
                             data={"deletedAt": datetime.now(timezone.utc)})
    await record_audit(db, actor_id, "DELETE", "invoices", record_id=invoice_id)


async def record_payment(db: Prisma, invoice_id: str, data: PaymentCreate, actor_id: str):
    invoice = await get_invoice(db, invoice_id)
    payment = await db.payment.create(data={
        "invoiceId": invoice_id,
        "amount": data.amount,
        "currency": data.currency.value,
        "method": data.method.value,
        "reference": data.reference,
        "paidAt": data.paidAt,
    })
    # Check if fully paid
    all_payments = await db.payment.find_many(where={"invoiceId": invoice_id})
    paid_total = sum(p.amount for p in all_payments)
    if paid_total >= invoice.totalAmount:
        await db.invoice.update(where={"id": invoice_id}, data={"status": "PAID"})
    await record_audit(db, actor_id, "PAYMENT", "invoices", record_id=invoice_id)
    return payment


async def check_overdue(db: Prisma):
    """Mark sent invoices past due date as OVERDUE."""
    now = datetime.now(timezone.utc)
    overdue = await db.invoice.find_many(
        where={"status": "SENT", "dueDate": {"lt": now}, "deletedAt": None}
    )
    for inv in overdue:
        await db.invoice.update(where={"id": inv.id}, data={"status": "OVERDUE"})
    return len(overdue)


async def revenue_report(db: Prisma, period: str = "monthly") -> List[RevenueReport]:
    invoices = await db.invoice.find_many(
        where={"status": "PAID", "deletedAt": None},
        order={"issueDate": "asc"},
    )
    buckets: dict = {}
    for inv in invoices:
        if period == "monthly":
            key = inv.issueDate.strftime("%Y-%m")
        elif period == "quarterly":
            q = (inv.issueDate.month - 1) // 3 + 1
            key = f"{inv.issueDate.year}-Q{q}"
        else:
            key = str(inv.issueDate.year)
        if key not in buckets:
            buckets[key] = {"total": Decimal("0"), "count": 0}
        buckets[key]["total"] += inv.totalAmount
        buckets[key]["count"] += 1
    return [
        RevenueReport(period=k, totalRevenue=v["total"], currency="INR", invoiceCount=v["count"])
        for k, v in sorted(buckets.items())
    ]


async def aging_report(db: Prisma) -> List[AgingBucket]:
    now = datetime.now(timezone.utc)
    invoices = await db.invoice.find_many(
        where={"status": {"in": ["SENT", "OVERDUE"]}, "deletedAt": None}
    )
    buckets = {"0-30": Decimal("0"), "31-60": Decimal("0"), "61-90": Decimal("0"), "90+": Decimal("0")}
    counts = {k: 0 for k in buckets}
    for inv in invoices:
        age = (now - inv.dueDate.replace(tzinfo=timezone.utc)).days
        if age <= 30:
            key = "0-30"
        elif age <= 60:
            key = "31-60"
        elif age <= 90:
            key = "61-90"
        else:
            key = "90+"
        buckets[key] += inv.totalAmount
        counts[key] += 1
    return [
        AgingBucket(bucket=k, totalAmount=v, invoiceCount=counts[k])
        for k, v in buckets.items()
    ]
