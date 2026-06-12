from datetime import datetime, timezone
from decimal import Decimal
from prisma import Prisma
from app.core.audit import record_audit
from app.middleware.error_handler import NotFoundError
from app.modules.pipeline.schemas import OpportunityCreate, OpportunityUpdate, StageMove


async def create_opportunity(db: Prisma, body: OpportunityCreate, owner_id: str) -> object:
    data = body.model_dump(exclude_none=True)
    data["ownerId"] = owner_id
    opp = await db.opportunity.create(data=data)
    await db.stagehistory.create(data={
        "opportunityId": opp.id, "stageId": body.stageId
    })
    await record_audit(db, owner_id, "CREATE", "opportunities", record_id=opp.id, new_values=data)
    return opp


async def get_opportunity(db: Prisma, opp_id: str) -> object:
    opp = await db.opportunity.find_first(where={"id": opp_id, "deletedAt": None})
    if not opp:
        raise NotFoundError(f"Opportunity {opp_id} not found")
    return opp


async def list_opportunities(db: Prisma, page: int, page_size: int,
                             stage_id: str | None, account_id: str | None) -> tuple[list, int]:
    where: dict = {"deletedAt": None}
    if stage_id:
        where["stageId"] = stage_id
    if account_id:
        where["accountId"] = account_id
    skip = (page - 1) * page_size
    opps = await db.opportunity.find_many(where=where, skip=skip, take=page_size,
                                          order={"createdAt": "desc"})
    total = await db.opportunity.count(where=where)
    return opps, total


async def update_opportunity(db: Prisma, opp_id: str, body: OpportunityUpdate, actor_id: str) -> object:
    opp = await db.opportunity.find_first(where={"id": opp_id, "deletedAt": None})
    if not opp:
        raise NotFoundError(f"Opportunity {opp_id} not found")
    data = body.model_dump(exclude_none=True)
    updated = await db.opportunity.update(where={"id": opp_id}, data=data)
    await record_audit(db, actor_id, "UPDATE", "opportunities", record_id=opp_id, new_values=data)
    return updated


async def move_stage(db: Prisma, opp_id: str, body: StageMove, actor_id: str) -> object:
    opp = await db.opportunity.find_first(where={"id": opp_id, "deletedAt": None})
    if not opp:
        raise NotFoundError(f"Opportunity {opp_id} not found")
    stage = await db.stage.find_unique(where={"id": body.stageId})
    if not stage:
        raise NotFoundError(f"Stage {body.stageId} not found")
    # Close out previous stage history
    await db.stagehistory.update_many(
        where={"opportunityId": opp_id, "exitedAt": None},
        data={"exitedAt": datetime.now(timezone.utc)},
    )
    # Record new stage entry
    await db.stagehistory.create(data={"opportunityId": opp_id, "stageId": body.stageId})
    updated = await db.opportunity.update(
        where={"id": opp_id},
        data={"stageId": body.stageId, "probability": stage.probability},
    )
    await record_audit(db, actor_id, "STAGE_MOVE", "opportunities", record_id=opp_id,
                       new_values={"stageId": body.stageId})
    return updated


async def delete_opportunity(db: Prisma, opp_id: str, actor_id: str) -> None:
    opp = await db.opportunity.find_first(where={"id": opp_id, "deletedAt": None})
    if not opp:
        raise NotFoundError(f"Opportunity {opp_id} not found")
    await db.opportunity.update(where={"id": opp_id},
                                data={"deletedAt": datetime.now(timezone.utc)})
    await record_audit(db, actor_id, "DELETE", "opportunities", record_id=opp_id)


async def forecast(db: Prisma) -> dict:
    stages = await db.stage.find_many(order={"order": "asc"})
    by_stage = []
    total_weighted = Decimal("0")
    for stage in stages:
        opps = await db.opportunity.find_many(
            where={"stageId": stage.id, "deletedAt": None}
        )
        stage_value = sum(o.value for o in opps)
        weighted = stage_value * Decimal(stage.probability) / 100
        total_weighted += weighted
        by_stage.append({
            "stageId": stage.id,
            "stageName": stage.name,
            "count": len(opps),
            "totalValue": float(stage_value),
            "weightedValue": float(weighted),
            "probability": stage.probability,
        })
    return {"totalWeightedValue": float(total_weighted), "currency": "INR", "byStage": by_stage}
