from fastapi import APIRouter, Depends, Query
from typing import Optional
from prisma import Prisma
from app.db.client import get_db
from app.core.security import get_current_user, require_role
from app.modules.invoice import schemas, service

router = APIRouter(prefix="/invoices", tags=["invoices"])

FINANCE_ROLES = ["FINANCE", "ADMIN"]


@router.post("", status_code=201)
async def create_invoice(
    body: schemas.InvoiceCreate,
    db: Prisma = Depends(get_db),
    current_user=Depends(require_role(FINANCE_ROLES)),
):
    invoice = await service.create_invoice(db, body, current_user.id)
    return {"data": invoice, "error": None, "meta": {}}


@router.get("")
async def list_invoices(
    status: Optional[str] = Query(None),
    accountId: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: Prisma = Depends(get_db),
    _=Depends(get_current_user),
):
    invoices = await service.list_invoices(db, status, accountId, skip, limit)
    return {"data": invoices, "error": None, "meta": {"total": len(invoices)}}


@router.get("/revenue")
async def revenue_report(
    period: str = Query("monthly", pattern="^(monthly|quarterly|yearly)$"),
    db: Prisma = Depends(get_db),
    _=Depends(require_role(FINANCE_ROLES)),
):
    report = await service.revenue_report(db, period)
    return {"data": report, "error": None, "meta": {}}


@router.get("/aging")
async def aging_report(
    db: Prisma = Depends(get_db),
    _=Depends(require_role(FINANCE_ROLES)),
):
    report = await service.aging_report(db)
    return {"data": report, "error": None, "meta": {}}


@router.get("/{invoice_id}")
async def get_invoice(
    invoice_id: str,
    db: Prisma = Depends(get_db),
    _=Depends(get_current_user),
):
    invoice = await service.get_invoice(db, invoice_id)
    return {"data": invoice, "error": None, "meta": {}}


@router.patch("/{invoice_id}")
async def update_invoice(
    invoice_id: str,
    body: schemas.InvoiceUpdate,
    db: Prisma = Depends(get_db),
    current_user=Depends(require_role(FINANCE_ROLES)),
):
    invoice = await service.update_invoice(db, invoice_id, body, current_user.id)
    return {"data": invoice, "error": None, "meta": {}}


@router.delete("/{invoice_id}", status_code=204)
async def delete_invoice(
    invoice_id: str,
    db: Prisma = Depends(get_db),
    current_user=Depends(require_role(["ADMIN"])),
):
    await service.delete_invoice(db, invoice_id, current_user.id)


@router.post("/{invoice_id}/payments", status_code=201)
async def record_payment(
    invoice_id: str,
    body: schemas.PaymentCreate,
    db: Prisma = Depends(get_db),
    current_user=Depends(require_role(FINANCE_ROLES)),
):
    payment = await service.record_payment(db, invoice_id, body, current_user.id)
    return {"data": payment, "error": None, "meta": {}}


@router.post("/overdue/check")
async def check_overdue(
    db: Prisma = Depends(get_db),
    _=Depends(require_role(["ADMIN"])),
):
    count = await service.check_overdue(db)
    return {"data": {"markedOverdue": count}, "error": None, "meta": {}}
