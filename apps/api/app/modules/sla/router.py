from fastapi import APIRouter, Depends, status
from prisma import Prisma

from app.core.dependencies import get_current_user, require_role
from app.core.enums import UserRole
from app.core.envelope import ok
from app.db.client import get_db
from app.modules.sla import service
from app.modules.sla.schemas import SLAPolicyCreate, SLAPolicyUpdate

router = APIRouter(tags=["sla"])

_admin = require_role(UserRole.ADMIN)


@router.post("/sla/policies", status_code=status.HTTP_201_CREATED)
async def create_policy(body: SLAPolicyCreate, db: Prisma = Depends(get_db),
                        current_user=Depends(_admin)) -> dict:
    return ok((await service.create_policy(db, body, current_user.id)).__dict__)


@router.get("/sla/policies")
async def list_policies(db: Prisma = Depends(get_db),
                        current_user=Depends(get_current_user)) -> dict:
    policies = await service.list_policies(db)
    return ok([p.__dict__ for p in policies])


@router.get("/sla/policies/{policy_id}")
async def get_policy(policy_id: str, db: Prisma = Depends(get_db),
                     current_user=Depends(get_current_user)) -> dict:
    return ok((await service.get_policy(db, policy_id)).__dict__)


@router.patch("/sla/policies/{policy_id}")
async def update_policy(policy_id: str, body: SLAPolicyUpdate,
                        db: Prisma = Depends(get_db), current_user=Depends(_admin)) -> dict:
    return ok((await service.update_policy(db, policy_id, body, current_user.id)).__dict__)


@router.post("/tickets/{ticket_id}/sla", status_code=status.HTTP_201_CREATED)
async def attach_sla(ticket_id: str, policy_id: str,
                     db: Prisma = Depends(get_db),
                     current_user=Depends(require_role(UserRole.ADMIN, UserRole.SUPPORT_AGENT))) -> dict:
    return ok((await service.attach_to_ticket(db, ticket_id, policy_id, current_user.id)).__dict__)


@router.get("/tickets/{ticket_id}/sla")
async def get_tracker(ticket_id: str, db: Prisma = Depends(get_db),
                      current_user=Depends(get_current_user)) -> dict:
    return ok((await service.get_tracker(db, ticket_id)).__dict__)


@router.post("/sla/check-breaches")
async def check_breaches(db: Prisma = Depends(get_db),
                         current_user=Depends(_admin)) -> dict:
    return ok(await service.check_breaches(db))


@router.get("/sla/compliance-report")
async def compliance_report(db: Prisma = Depends(get_db),
                             current_user=Depends(get_current_user)) -> dict:
    return ok(await service.compliance_report(db))
