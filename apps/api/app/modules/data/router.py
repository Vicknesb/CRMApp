from fastapi import APIRouter, Depends, Query, UploadFile, File, Form
from typing import Optional
import json
from prisma import Prisma
from app.db.client import get_db
from app.core.security import get_current_user, require_role
from app.modules.data import schemas, service

router = APIRouter(prefix="/data", tags=["data"])
ADMIN_ONLY = ["ADMIN"]


@router.post("/import", status_code=201)
async def import_csv(
    module: str = Form(...),
    mappings: str = Form(...),
    file: UploadFile = File(...),
    db: Prisma = Depends(get_db),
    current_user=Depends(require_role(ADMIN_ONLY)),
):
    content = (await file.read()).decode("utf-8-sig")
    mapping_list = json.loads(mappings)
    result = await service.import_csv(db, module, content, mapping_list, current_user.id)
    return {"data": result, "error": None, "meta": {}}


@router.get("/recycle-bin")
async def list_recycle_bin(module: Optional[str] = Query(None), skip: int = 0, limit: int = 50,
                            db: Prisma = Depends(get_db), _=Depends(require_role(ADMIN_ONLY))):
    entries = await service.list_recycle_bin(db, module, skip, limit)
    return {"data": entries, "error": None, "meta": {}}


@router.post("/recycle-bin/{entry_id}/restore")
async def restore_record(entry_id: str, db: Prisma = Depends(get_db),
                          current_user=Depends(require_role(ADMIN_ONLY))):
    await service.restore_record(db, entry_id, current_user.id)
    return {"data": {"restored": True}, "error": None, "meta": {}}


@router.post("/recycle-bin/purge")
async def purge_expired(db: Prisma = Depends(get_db), current_user=Depends(require_role(ADMIN_ONLY))):
    count = await service.purge_expired(db, current_user.id)
    return {"data": {"purged": count}, "error": None, "meta": {}}


@router.post("/gdpr/export")
async def export_subject(body: schemas.DataExportRequest, db: Prisma = Depends(get_db),
                          current_user=Depends(require_role(ADMIN_ONLY))):
    result = await service.export_subject_data(db, body, current_user.id)
    return {"data": result, "error": None, "meta": {}}


@router.post("/gdpr/erase")
async def erase_subject(body: schemas.ErasureRequest, db: Prisma = Depends(get_db),
                         current_user=Depends(require_role(ADMIN_ONLY))):
    result = await service.erase_subject(db, body, current_user.id)
    return {"data": result, "error": None, "meta": {}}


@router.post("/consent")
async def record_consent(body: schemas.ConsentRecord, db: Prisma = Depends(get_db),
                          _=Depends(get_current_user)):
    consent = await service.record_consent(db, body)
    return {"data": consent, "error": None, "meta": {}}


@router.get("/consent/check")
async def check_consent(email: str = Query(...), consentType: str = Query(...),
                         db: Prisma = Depends(get_db), _=Depends(get_current_user)):
    granted = await service.check_consent(db, email, consentType)
    return {"data": {"granted": granted}, "error": None, "meta": {}}
