from __future__ import annotations
import csv, io
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any
from prisma import Prisma
from app.modules.data.schemas import ImportRequest, ImportResult, DataExportRequest, ErasureRequest, ConsentRecord
from app.core.audit import record_audit
from fastapi import HTTPException

ALLOWED_IMPORT_MODULES = {"leads", "contacts", "accounts"}
CHUNK_SIZE = 500


async def import_csv(db: Prisma, module: str, csv_content: str,
                     mappings: List[Dict[str, str]], actor_id: str) -> ImportResult:
    if module not in ALLOWED_IMPORT_MODULES:
        raise HTTPException(status_code=422, detail=f"Module '{module}' not importable")

    reader = csv.DictReader(io.StringIO(csv_content))
    rows = list(reader)
    imported = 0
    error_rows: list = []

    # Process in chunks
    for i in range(0, len(rows), CHUNK_SIZE):
        chunk = rows[i:i + CHUNK_SIZE]
        for idx, row in enumerate(chunk):
            try:
                mapped: dict = {}
                for m in mappings:
                    val = row.get(m["sourceColumn"])
                    if val is not None:
                        mapped[m["targetField"]] = val

                if module == "leads":
                    if not mapped.get("email"):
                        raise ValueError("email required")
                    await db.lead.create(data={
                        "firstName": mapped.get("firstName", ""),
                        "lastName": mapped.get("lastName", ""),
                        "email": mapped["email"],
                        "phone": mapped.get("phone"),
                        "company": mapped.get("company"),
                    })
                elif module == "contacts":
                    if not mapped.get("email"):
                        raise ValueError("email required")
                    await db.contact.create(data={
                        "firstName": mapped.get("firstName", ""),
                        "lastName": mapped.get("lastName", ""),
                        "email": mapped["email"],
                        "phone": mapped.get("phone"),
                    })
                elif module == "accounts":
                    if not mapped.get("name"):
                        raise ValueError("name required")
                    await db.account.create(data={"name": mapped["name"]})
                imported += 1
            except Exception as e:
                error_rows.append({"row": i + idx + 1, "error": str(e)})

    await record_audit(db, actor_id, "IMPORT", module,
                       record_id=None)
    return ImportResult(total=len(rows), imported=imported,
                        errors=len(error_rows), errorRows=error_rows[:50])


async def list_recycle_bin(db: Prisma, module: str | None = None, skip: int = 0, limit: int = 50):
    where: dict = {}
    if module:
        where["module"] = module
    return await db.recyclebinentry.find_many(where=where, skip=skip, take=limit,
                                              order={"deletedAt": "desc"})


async def restore_record(db: Prisma, entry_id: str, actor_id: str):
    entry = await db.recyclebinentry.find_unique(where={"id": entry_id})
    if not entry:
        raise HTTPException(status_code=404, detail="Recycle bin entry not found")
    # Restore by clearing deletedAt on the original record
    model = getattr(db, entry.module.rstrip("s"), None) or getattr(db, entry.module, None)
    if model:
        await model.update(where={"id": str(entry.recordId)}, data={"deletedAt": None})
    await db.recyclebinentry.delete(where={"id": entry_id})
    await record_audit(db, actor_id, "RESTORE", entry.module, record_id=str(entry.recordId))


async def purge_expired(db: Prisma, actor_id: str) -> int:
    now = datetime.now(timezone.utc)
    expired = await db.recyclebinentry.find_many(where={"purgeAt": {"lte": now}})
    count = 0
    for e in expired:
        await db.recyclebinentry.delete(where={"id": e.id})
        count += 1
    await record_audit(db, actor_id, "PURGE", "recycle_bin")
    return count


async def export_subject_data(db: Prisma, req: DataExportRequest, actor_id: str) -> dict:
    email = req.subjectEmail
    contacts = await db.contact.find_many(where={"email": email})
    leads = await db.lead.find_many(where={"email": email})
    await record_audit(db, actor_id, "DATA_EXPORT", "gdpr")
    return {
        "subjectEmail": email,
        "contacts": len(contacts),
        "leads": len(leads),
        "exportedAt": datetime.now(timezone.utc).isoformat(),
    }


async def erase_subject(db: Prisma, req: ErasureRequest, actor_id: str) -> dict:
    email = req.subjectEmail
    anon = f"anon_{hash(email) & 0xFFFFFF}@deleted.local"
    # Anonymize contacts
    await db.contact.update_many(
        where={"email": email},
        data={"firstName": "DELETED", "lastName": "DELETED", "email": anon, "phone": None},
    )
    # Anonymize leads
    await db.lead.update_many(
        where={"email": email},
        data={"firstName": "DELETED", "lastName": "DELETED", "email": anon, "phone": None},
    )
    await record_audit(db, actor_id, "DATA_ERASURE", "gdpr")
    return {"subjectEmail": email, "anonymized": True, "reason": req.reason}


async def record_consent(db: Prisma, data: ConsentRecord):
    consent = await db.consentrecord.create(data={
        "email": data.email,
        "consentType": data.consentType,
        "granted": data.granted,
        "ipAddress": data.ipAddress,
    })
    return consent


async def check_consent(db: Prisma, email: str, consent_type: str) -> bool:
    record = await db.consentrecord.find_first(
        where={"email": email, "consentType": consent_type},
        order={"grantedAt": "desc"},
    )
    return record.granted if record else False
