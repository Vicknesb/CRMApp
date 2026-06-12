from fastapi import APIRouter, Depends, Query, status
from prisma import Prisma
from typing import Optional

from app.core.dependencies import get_current_user
from app.core.envelope import ok
from app.core.enums import LeadSource, LeadStatus
from app.db.client import get_db
from app.modules.lead import service
from app.modules.lead.schemas import (
    ConvertLeadRequest, LeadCreate, LeadListParams, LeadUpdate,
)

router = APIRouter(prefix="/leads", tags=["leads"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_lead(
    body: LeadCreate,
    db: Prisma = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict:
    lead = await service.create_lead(db, body, current_user.id)
    return ok(lead.__dict__, meta={"module": "leads"})


@router.get("")
async def list_leads(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[LeadStatus] = None,
    source: Optional[LeadSource] = None,
    assignee_id: Optional[str] = None,
    search: Optional[str] = None,
    db: Prisma = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict:
    params = LeadListParams(
        page=page, page_size=page_size, status=status,
        source=source, assignee_id=assignee_id, search=search,
    )
    leads, total = await service.list_leads(db, params)
    return ok(
        [l.__dict__ for l in leads],
        meta={"total": total, "page": page, "page_size": page_size},
    )


@router.get("/{lead_id}")
async def get_lead(
    lead_id: str,
    db: Prisma = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict:
    lead = await service.get_lead(db, lead_id)
    return ok(lead.__dict__)


@router.patch("/{lead_id}")
async def update_lead(
    lead_id: str,
    body: LeadUpdate,
    db: Prisma = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict:
    lead = await service.update_lead(db, lead_id, body, current_user.id)
    return ok(lead.__dict__)


@router.delete("/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lead(
    lead_id: str,
    db: Prisma = Depends(get_db),
    current_user=Depends(get_current_user),
) -> None:
    await service.delete_lead(db, lead_id, current_user.id)


@router.post("/{lead_id}/score")
async def score_lead(
    lead_id: str,
    db: Prisma = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict:
    result = await service.score_lead(db, lead_id)
    return ok(result)


@router.post("/{lead_id}/assign")
async def assign_lead(
    lead_id: str,
    assignee_id: str = Query(...),
    db: Prisma = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict:
    lead = await service.assign_lead(db, lead_id, assignee_id, current_user.id)
    return ok(lead.__dict__)


@router.post("/{lead_id}/convert")
async def convert_lead(
    lead_id: str,
    body: ConvertLeadRequest,
    db: Prisma = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict:
    result = await service.convert_lead(db, lead_id, body, current_user.id)
    return ok(result)
