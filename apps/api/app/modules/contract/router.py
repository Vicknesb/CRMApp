from fastapi import APIRouter, Depends, Query
from typing import Optional
from prisma import Prisma
from app.db.client import get_db
from app.core.security import get_current_user, require_role
from app.modules.contract import schemas, service

router = APIRouter(prefix="/contracts", tags=["contracts"])

FINANCE_ROLES = ["FINANCE", "ADMIN", "SALES_MANAGER"]


@router.post("", status_code=201)
async def create_contract(
    body: schemas.ContractCreate,
    db: Prisma = Depends(get_db),
    current_user=Depends(require_role(FINANCE_ROLES)),
):
    contract = await service.create_contract(db, body, current_user.id)
    return {"data": contract, "error": None, "meta": {}}


@router.get("")
async def list_contracts(
    status: Optional[str] = Query(None),
    accountId: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: Prisma = Depends(get_db),
    _=Depends(get_current_user),
):
    contracts = await service.list_contracts(db, status, accountId, skip, limit)
    return {"data": contracts, "error": None, "meta": {"total": len(contracts)}}


@router.get("/renewals")
async def renewal_reminders(
    days: int = Query(90, ge=1, le=365),
    db: Prisma = Depends(get_db),
    _=Depends(get_current_user),
):
    reminders = await service.get_renewal_reminders(db, days)
    return {"data": reminders, "error": None, "meta": {"total": len(reminders)}}


@router.get("/{contract_id}")
async def get_contract(
    contract_id: str,
    db: Prisma = Depends(get_db),
    _=Depends(get_current_user),
):
    contract = await service.get_contract(db, contract_id)
    return {"data": contract, "error": None, "meta": {}}


@router.patch("/{contract_id}")
async def update_contract(
    contract_id: str,
    body: schemas.ContractUpdate,
    db: Prisma = Depends(get_db),
    current_user=Depends(require_role(FINANCE_ROLES)),
):
    contract = await service.update_contract(db, contract_id, body, current_user.id)
    return {"data": contract, "error": None, "meta": {}}


@router.delete("/{contract_id}", status_code=204)
async def delete_contract(
    contract_id: str,
    db: Prisma = Depends(get_db),
    current_user=Depends(require_role(["ADMIN"])),
):
    await service.delete_contract(db, contract_id, current_user.id)


@router.post("/{contract_id}/amendments", status_code=201)
async def add_amendment(
    contract_id: str,
    body: schemas.AmendmentCreate,
    db: Prisma = Depends(get_db),
    current_user=Depends(require_role(FINANCE_ROLES)),
):
    amendment = await service.add_amendment(db, contract_id, body, current_user.id)
    return {"data": amendment, "error": None, "meta": {}}


@router.post("/{contract_id}/signatures", status_code=201)
async def request_signature(
    contract_id: str,
    body: schemas.SignatureRequest,
    db: Prisma = Depends(get_db),
    current_user=Depends(require_role(FINANCE_ROLES)),
):
    signature = await service.request_signature(db, contract_id, body, current_user.id)
    return {"data": signature, "error": None, "meta": {}}


@router.post("/signatures/callback")
async def signature_callback(
    body: schemas.SignatureCallbackPayload,
    db: Prisma = Depends(get_db),
):
    signature = await service.handle_signature_callback(db, body)
    return {"data": signature, "error": None, "meta": {}}
