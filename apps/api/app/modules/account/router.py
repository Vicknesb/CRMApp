from fastapi import APIRouter, Depends, Query, status
from prisma import Prisma
from typing import Optional

from app.core.dependencies import get_current_user
from app.core.envelope import ok
from app.db.client import get_db
from app.modules.account import service
from app.modules.account.schemas import AccountCreate, AccountUpdate

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_account(body: AccountCreate, db: Prisma = Depends(get_db),
                         current_user=Depends(get_current_user)) -> dict:
    return ok((await service.create_account(db, body, current_user.id)).__dict__)


@router.get("")
async def list_accounts(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
                        tier: Optional[str] = None, search: Optional[str] = None,
                        db: Prisma = Depends(get_db), current_user=Depends(get_current_user)) -> dict:
    accounts, total = await service.list_accounts(db, page, page_size, tier, search)
    return ok([a.__dict__ for a in accounts],
              meta={"total": total, "page": page, "page_size": page_size})


@router.get("/{account_id}")
async def get_account(account_id: str, db: Prisma = Depends(get_db),
                      current_user=Depends(get_current_user)) -> dict:
    return ok((await service.get_account(db, account_id)).__dict__)


@router.patch("/{account_id}")
async def update_account(account_id: str, body: AccountUpdate, db: Prisma = Depends(get_db),
                         current_user=Depends(get_current_user)) -> dict:
    return ok((await service.update_account(db, account_id, body, current_user.id)).__dict__)


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(account_id: str, db: Prisma = Depends(get_db),
                         current_user=Depends(get_current_user)) -> None:
    await service.delete_account(db, account_id, current_user.id)


@router.get("/{account_id}/360")
async def account_360(account_id: str, db: Prisma = Depends(get_db),
                      current_user=Depends(get_current_user)) -> dict:
    return ok(await service.get_account_360(db, account_id))


@router.post("/{account_id}/health-score")
async def recalc_health(account_id: str, db: Prisma = Depends(get_db),
                        current_user=Depends(get_current_user)) -> dict:
    score = await service.calculate_health_score(db, account_id)
    return ok({"accountId": account_id, "healthScore": score})
