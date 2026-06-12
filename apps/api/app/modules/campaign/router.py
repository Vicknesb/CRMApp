from fastapi import APIRouter, Depends, Query
from typing import Optional
from prisma import Prisma
from app.db.client import get_db
from app.core.security import get_current_user, require_role
from app.modules.campaign import schemas, service

router = APIRouter(prefix="/campaigns", tags=["campaigns"])
MKTG_ROLES = ["MARKETING", "ADMIN"]


@router.post("", status_code=201)
async def create_campaign(body: schemas.CampaignCreate, db: Prisma = Depends(get_db),
                           current_user=Depends(require_role(MKTG_ROLES))):
    c = await service.create_campaign(db, body, current_user.id)
    return {"data": c, "error": None, "meta": {}}


@router.get("")
async def list_campaigns(status: Optional[str] = Query(None), type: Optional[str] = Query(None),
                          skip: int = 0, limit: int = 50,
                          db: Prisma = Depends(get_db), _=Depends(get_current_user)):
    campaigns = await service.list_campaigns(db, status, type, skip, limit)
    return {"data": campaigns, "error": None, "meta": {"total": len(campaigns)}}


@router.get("/{campaign_id}")
async def get_campaign(campaign_id: str, db: Prisma = Depends(get_db), _=Depends(get_current_user)):
    c = await service.get_campaign(db, campaign_id)
    return {"data": c, "error": None, "meta": {}}


@router.patch("/{campaign_id}")
async def update_campaign(campaign_id: str, body: schemas.CampaignUpdate,
                           db: Prisma = Depends(get_db),
                           current_user=Depends(require_role(MKTG_ROLES))):
    c = await service.update_campaign(db, campaign_id, body, current_user.id)
    return {"data": c, "error": None, "meta": {}}


@router.delete("/{campaign_id}", status_code=204)
async def delete_campaign(campaign_id: str, db: Prisma = Depends(get_db),
                           current_user=Depends(require_role(["ADMIN"]))):
    await service.delete_campaign(db, campaign_id, current_user.id)


@router.post("/{campaign_id}/segments", status_code=201)
async def add_segment(campaign_id: str, body: schemas.SegmentCreate,
                       db: Prisma = Depends(get_db), current_user=Depends(require_role(MKTG_ROLES))):
    seg = await service.add_segment(db, campaign_id, body, current_user.id)
    return {"data": seg, "error": None, "meta": {}}


@router.post("/{campaign_id}/metrics", status_code=201)
async def ingest_metric(campaign_id: str, body: schemas.MetricIngest,
                         db: Prisma = Depends(get_db), current_user=Depends(require_role(MKTG_ROLES))):
    m = await service.ingest_metric(db, campaign_id, body, current_user.id)
    return {"data": m, "error": None, "meta": {}}


@router.get("/{campaign_id}/metrics/summary")
async def metrics_summary(campaign_id: str, db: Prisma = Depends(get_db), _=Depends(get_current_user)):
    summary = await service.get_metrics_summary(db, campaign_id)
    return {"data": summary, "error": None, "meta": {}}


@router.get("/{campaign_id}/roi")
async def roi_report(campaign_id: str, db: Prisma = Depends(get_db), _=Depends(get_current_user)):
    roi = await service.get_roi_report(db, campaign_id)
    return {"data": roi, "error": None, "meta": {}}


@router.post("/{campaign_id}/events", status_code=201)
async def create_event(campaign_id: str, body: schemas.EventCreate,
                        db: Prisma = Depends(get_db), current_user=Depends(require_role(MKTG_ROLES))):
    ev = await service.create_event(db, campaign_id, body, current_user.id)
    return {"data": ev, "error": None, "meta": {}}
