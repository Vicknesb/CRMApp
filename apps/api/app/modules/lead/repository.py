from prisma import Prisma
from app.core.enums import LeadSource, LeadStatus


async def create_lead(db: Prisma, data: dict) -> object:
    return await db.lead.create(data=data)


async def get_lead(db: Prisma, lead_id: str) -> object | None:
    return await db.lead.find_first(where={"id": lead_id, "deletedAt": None})


async def list_leads(db: Prisma, where: dict, skip: int, take: int) -> list:
    return await db.lead.find_many(where=where, skip=skip, take=take,
                                   order={"createdAt": "desc"})


async def count_leads(db: Prisma, where: dict) -> int:
    return await db.lead.count(where=where)


async def update_lead(db: Prisma, lead_id: str, data: dict) -> object:
    return await db.lead.update(where={"id": lead_id}, data=data)


async def soft_delete_lead(db: Prisma, lead_id: str) -> object:
    from datetime import datetime, timezone
    return await db.lead.update(
        where={"id": lead_id},
        data={"deletedAt": datetime.now(timezone.utc)},
    )


async def find_duplicate(db: Prisma, email: str, company: str | None) -> object | None:
    return await db.lead.find_first(
        where={"email": email, "deletedAt": None}
    )


async def get_score_rules(db: Prisma) -> list:
    return await db.leadscorrule.find_many(where={"isActive": True})


async def add_score_history(db: Prisma, lead_id: str, delta: int, reason: str) -> None:
    await db.leadscorehistory.create(data={
        "leadId": lead_id, "delta": delta, "reason": reason
    })
