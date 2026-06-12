from fastapi import APIRouter, Depends, Query
from typing import Optional
from prisma import Prisma
from app.db.client import get_db
from app.core.security import get_current_user, require_role
from app.modules.analytics import schemas, service

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dashboard")
async def dashboard(role: Optional[str] = Query(None),
                    db: Prisma = Depends(get_db),
                    current_user=Depends(get_current_user)):
    effective_role = role or current_user.role
    result = await service.get_dashboard(db, effective_role)
    return {"data": result, "error": None, "meta": {}}


@router.get("/reports")
async def list_reports(_=Depends(get_current_user)):
    return {"data": list(service.REPORT_MAP.keys()), "error": None, "meta": {}}


@router.get("/reports/{report_key}")
async def run_report(report_key: str, db: Prisma = Depends(get_db), _=Depends(get_current_user)):
    result = await service.run_prebuilt_report(db, report_key)
    return {"data": result, "error": None, "meta": {}}


@router.post("/reports/run")
async def run_custom_report(body: schemas.CustomReportDefinition,
                              db: Prisma = Depends(get_db),
                              _=Depends(get_current_user)):
    result = await service.run_custom_report(db, body)
    return {"data": result, "error": None, "meta": {}}
