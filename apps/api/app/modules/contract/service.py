from __future__ import annotations
from datetime import datetime, timezone, timedelta
from typing import Optional, List
from prisma import Prisma
from app.modules.contract.schemas import (
    ContractCreate, ContractUpdate, AmendmentCreate,
    SignatureRequest, SignatureCallbackPayload, RenewalReminder,
)
from app.core.audit import record_audit
from fastapi import HTTPException
import random, string


def _gen_number() -> str:
    suffix = "".join(random.choices(string.digits, k=6))
    year = datetime.now(timezone.utc).year
    return f"CONTR-{year}-{suffix}"


async def create_contract(db: Prisma, data: ContractCreate, actor_id: str):
    number = _gen_number()
    contract = await db.contract.create(data={
        "number": number,
        "title": data.title,
        "accountId": data.accountId,
        "opportunityId": data.opportunityId,
        "startDate": data.startDate,
        "endDate": data.endDate,
        "value": data.value,
        "currency": data.currency.value,
        "terms": data.terms,
        "autoRenew": data.autoRenew,
        "renewalNoticeDays": data.renewalNoticeDays,
    })
    await record_audit(db, actor_id, "CREATE", "contracts", record_id=contract.id)
    return contract


async def get_contract(db: Prisma, contract_id: str):
    contract = await db.contract.find_first(
        where={"id": contract_id, "deletedAt": None},
        include={"amendments": True, "signatures": True},
    )
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract


async def list_contracts(db: Prisma, status: Optional[str] = None, account_id: Optional[str] = None,
                         skip: int = 0, limit: int = 50):
    where: dict = {"deletedAt": None}
    if status:
        where["status"] = status
    if account_id:
        where["accountId"] = account_id
    return await db.contract.find_many(where=where, skip=skip, take=limit, order={"createdAt": "desc"})


async def update_contract(db: Prisma, contract_id: str, data: ContractUpdate, actor_id: str):
    await get_contract(db, contract_id)
    payload = {k: v for k, v in data.model_dump(exclude_none=True).items()}
    if "status" in payload:
        payload["status"] = payload["status"].value
    if "currency" in payload:
        payload["currency"] = payload["currency"].value
    contract = await db.contract.update(where={"id": contract_id}, data=payload)
    await record_audit(db, actor_id, "UPDATE", "contracts", record_id=contract_id)
    return contract


async def delete_contract(db: Prisma, contract_id: str, actor_id: str):
    await get_contract(db, contract_id)
    await db.contract.update(where={"id": contract_id},
                              data={"deletedAt": datetime.now(timezone.utc)})
    await record_audit(db, actor_id, "DELETE", "contracts", record_id=contract_id)


async def add_amendment(db: Prisma, contract_id: str, data: AmendmentCreate, actor_id: str):
    await get_contract(db, contract_id)
    amendment = await db.amendment.create(data={
        "contractId": contract_id,
        "description": data.description,
        "effectiveAt": data.effectiveAt,
    })
    await record_audit(db, actor_id, "CREATE", "amendments", record_id=amendment.id)
    return amendment


async def request_signature(db: Prisma, contract_id: str, data: SignatureRequest, actor_id: str):
    await get_contract(db, contract_id)
    signature = await db.signature.create(data={
        "contractId": contract_id,
        "signerName": data.signerName,
        "signerEmail": data.signerEmail,
        "provider": data.provider,
        "status": "PENDING",
    })
    await record_audit(db, actor_id, "ESIGN_REQUEST", "signatures", record_id=signature.id)
    return signature


async def handle_signature_callback(db: Prisma, payload: SignatureCallbackPayload):
    signature = await db.signature.find_first(where={"externalId": payload.externalId})
    if not signature:
        raise HTTPException(status_code=404, detail="Signature not found")
    status_map = {"completed": "SIGNED", "declined": "DECLINED"}
    new_status = status_map.get(payload.status.lower(), "PENDING")
    updated = await db.signature.update(
        where={"id": signature.id},
        data={"status": new_status, "signedAt": payload.signedAt},
    )
    return updated


async def get_renewal_reminders(db: Prisma, days: int = 90) -> List[RenewalReminder]:
    """Return contracts expiring within the given days window."""
    now = datetime.now(timezone.utc)
    cutoff = now + timedelta(days=days)
    contracts = await db.contract.find_many(
        where={"deletedAt": None, "status": "ACTIVE", "endDate": {"lte": cutoff, "gte": now}},
        order={"endDate": "asc"},
    )
    reminders = []
    for c in contracts:
        days_until = (c.endDate.replace(tzinfo=timezone.utc) - now).days
        reminders.append(RenewalReminder(
            contractId=c.id,
            number=c.number,
            title=c.title,
            endDate=c.endDate,
            daysUntilExpiry=days_until,
            autoRenew=c.autoRenew,
        ))
    return reminders
