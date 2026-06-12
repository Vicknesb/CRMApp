from fastapi import APIRouter, Depends, Query, status
from prisma import Prisma
from typing import Optional

from app.core.dependencies import get_current_user
from app.core.envelope import ok
from app.db.client import get_db
from app.modules.pipeline import service
from app.modules.pipeline.schemas import OpportunityCreate, OpportunityUpdate, StageMove

router = APIRouter(prefix="/opportunities", tags=["pipeline"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_opportunity(body: OpportunityCreate, db: Prisma = Depends(get_db),
                              current_user=Depends(get_current_user)) -> dict:
    return ok((await service.create_opportunity(db, body, current_user.id)).__dict__)


@router.get("")
async def list_opportunities(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
                              stage_id: Optional[str] = None, account_id: Optional[str] = None,
                              db: Prisma = Depends(get_db), current_user=Depends(get_current_user)) -> dict:
    opps, total = await service.list_opportunities(db, page, page_size, stage_id, account_id)
    return ok([o.__dict__ for o in opps], meta={"total": total, "page": page, "page_size": page_size})


@router.get("/forecast")
async def revenue_forecast(db: Prisma = Depends(get_db),
                            current_user=Depends(get_current_user)) -> dict:
    return ok(await service.forecast(db))


@router.get("/{opp_id}")
async def get_opportunity(opp_id: str, db: Prisma = Depends(get_db),
                           current_user=Depends(get_current_user)) -> dict:
    return ok((await service.get_opportunity(db, opp_id)).__dict__)


@router.patch("/{opp_id}")
async def update_opportunity(opp_id: str, body: OpportunityUpdate,
                              db: Prisma = Depends(get_db), current_user=Depends(get_current_user)) -> dict:
    return ok((await service.update_opportunity(db, opp_id, body, current_user.id)).__dict__)


@router.post("/{opp_id}/stage")
async def move_stage(opp_id: str, body: StageMove, db: Prisma = Depends(get_db),
                     current_user=Depends(get_current_user)) -> dict:
    return ok((await service.move_stage(db, opp_id, body, current_user.id)).__dict__)


@router.delete("/{opp_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_opportunity(opp_id: str, db: Prisma = Depends(get_db),
                              current_user=Depends(get_current_user)) -> None:
    await service.delete_opportunity(db, opp_id, current_user.id)
