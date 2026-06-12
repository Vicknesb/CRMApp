from datetime import datetime, timedelta, timezone
from prisma import Prisma
from app.core.audit import record_audit
from app.middleware.error_handler import NotFoundError
from app.modules.sla.schemas import SLAPolicyCreate, SLAPolicyUpdate


async def create_policy(db: Prisma, body: SLAPolicyCreate, actor_id: str) -> object:
    data = body.model_dump()
    policy = await db.slApolicy.create(data=data)
    await record_audit(db, actor_id, "CREATE", "slaPolicies", record_id=policy.id, new_values=data)
    return policy


async def list_policies(db: Prisma) -> list:
    return await db.slApolicy.find_many(order={"name": "asc"})


async def get_policy(db: Prisma, policy_id: str) -> object:
    policy = await db.slApolicy.find_unique(where={"id": policy_id})
    if not policy:
        raise NotFoundError(f"SLA policy {policy_id} not found")
    return policy


async def update_policy(db: Prisma, policy_id: str, body: SLAPolicyUpdate, actor_id: str) -> object:
    await get_policy(db, policy_id)
    data = body.model_dump(exclude_none=True)
    updated = await db.slApolicy.update(where={"id": policy_id}, data=data)
    await record_audit(db, actor_id, "UPDATE", "slaPolicies", record_id=policy_id, new_values=data)
    return updated


async def attach_to_ticket(db: Prisma, ticket_id: str, policy_id: str, actor_id: str) -> object:
    """Attach an SLA policy to a ticket and start the SLA tracker."""
    policy = await get_policy(db, policy_id)
    now = datetime.now(timezone.utc)
    response_due = now + timedelta(minutes=policy.responseMinutes)
    resolution_due = now + timedelta(minutes=policy.resolutionMinutes)

    tracker = await db.slatracker.upsert(
        where={"ticketId": ticket_id},
        data={
            "create": {
                "ticketId": ticket_id,
                "policyId": policy_id,
                "responseDue": response_due,
                "resolutionDue": resolution_due,
            },
            "update": {
                "policyId": policy_id,
                "responseDue": response_due,
                "resolutionDue": resolution_due,
                "responseBreached": False,
                "resolutionBreached": False,
                "respondedAt": None,
                "resolvedAt": None,
            },
        },
    )
    await record_audit(db, actor_id, "SLA_ATTACH", "tickets", record_id=ticket_id,
                       new_values={"policyId": policy_id})
    return tracker


async def get_tracker(db: Prisma, ticket_id: str) -> object:
    tracker = await db.slatracker.find_unique(where={"ticketId": ticket_id})
    if not tracker:
        raise NotFoundError(f"No SLA tracker for ticket {ticket_id}")
    return tracker


async def check_breaches(db: Prisma) -> dict:
    """Mark overdue trackers as breached. Called periodically (or on demand)."""
    now = datetime.now(timezone.utc)
    response_breach = await db.slatracker.update_many(
        where={"responseDue": {"lt": now}, "respondedAt": None, "responseBreached": False},
        data={"responseBreached": True},
    )
    resolution_breach = await db.slatracker.update_many(
        where={"resolutionDue": {"lt": now}, "resolvedAt": None, "resolutionBreached": False},
        data={"resolutionBreached": True},
    )
    return {
        "responseBreachesMarked": response_breach.count if hasattr(response_breach, "count") else 0,
        "resolutionBreachesMarked": resolution_breach.count if hasattr(resolution_breach, "count") else 0,
        "checkedAt": now.isoformat(),
    }


async def compliance_report(db: Prisma) -> dict:
    """Aggregate SLA compliance stats."""
    total = await db.slatracker.count()
    response_breached = await db.slatracker.count(where={"responseBreached": True})
    resolution_breached = await db.slatracker.count(where={"resolutionBreached": True})
    compliant = total - resolution_breached
    return {
        "total": total,
        "compliant": compliant,
        "responseBreaches": response_breached,
        "resolutionBreaches": resolution_breached,
        "complianceRate": round((compliant / total * 100), 2) if total else 100.0,
    }
