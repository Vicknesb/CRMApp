from datetime import datetime, timezone
from prisma import Prisma
from app.core.audit import record_audit
from app.middleware.error_handler import NotFoundError
from app.modules.account.schemas import AccountCreate, AccountUpdate


async def create_account(db: Prisma, body: AccountCreate, owner_id: str) -> object:
    data = body.model_dump(exclude_none=True)
    data["ownerId"] = owner_id
    account = await db.account.create(data=data)
    await record_audit(db, owner_id, "CREATE", "accounts", record_id=account.id, new_values=data)
    return account


async def get_account(db: Prisma, account_id: str) -> object:
    account = await db.account.find_first(where={"id": account_id, "deletedAt": None})
    if not account:
        raise NotFoundError(f"Account {account_id} not found")
    return account


async def list_accounts(db: Prisma, page: int, page_size: int,
                        tier: str | None, search: str | None) -> tuple[list, int]:
    where: dict = {"deletedAt": None}
    if tier:
        where["tier"] = tier
    if search:
        where["name"] = {"contains": search, "mode": "insensitive"}
    skip = (page - 1) * page_size
    accounts = await db.account.find_many(where=where, skip=skip, take=page_size,
                                          order={"name": "asc"})
    total = await db.account.count(where=where)
    return accounts, total


async def update_account(db: Prisma, account_id: str, body: AccountUpdate, actor_id: str) -> object:
    account = await db.account.find_first(where={"id": account_id, "deletedAt": None})
    if not account:
        raise NotFoundError(f"Account {account_id} not found")
    data = body.model_dump(exclude_none=True)
    updated = await db.account.update(where={"id": account_id}, data=data)
    await record_audit(db, actor_id, "UPDATE", "accounts", record_id=account_id, new_values=data)
    return updated


async def delete_account(db: Prisma, account_id: str, actor_id: str) -> None:
    account = await db.account.find_first(where={"id": account_id, "deletedAt": None})
    if not account:
        raise NotFoundError(f"Account {account_id} not found")
    await db.account.update(where={"id": account_id},
                            data={"deletedAt": datetime.now(timezone.utc)})
    await record_audit(db, actor_id, "DELETE", "accounts", record_id=account_id)


async def calculate_health_score(db: Prisma, account_id: str) -> int:
    """Aggregate open tickets, active projects, overdue invoices into a 0-100 score."""
    from app.core.enums import TicketStatus, InvoiceStatus, ProjectStatus
    open_tickets = await db.ticket.count(
        where={"accountId": account_id, "status": {"not": TicketStatus.CLOSED}, "deletedAt": None}
    )
    active_projects = await db.project.count(
        where={"accountId": account_id, "status": ProjectStatus.ACTIVE, "deletedAt": None}
    )
    overdue_invoices = await db.invoice.count(
        where={"accountId": account_id, "status": InvoiceStatus.OVERDUE, "deletedAt": None}
    )
    score = max(0, 100 - (open_tickets * 5) - (overdue_invoices * 10) + (active_projects * 5))
    score = min(100, score)
    await db.account.update(where={"id": account_id}, data={"healthScore": score})
    return score


async def get_account_360(db: Prisma, account_id: str) -> dict:
    account = await get_account(db, account_id)
    contacts = await db.contactaccount.find_many(where={"accountId": account_id})
    opportunities = await db.opportunity.find_many(
        where={"accountId": account_id, "deletedAt": None}, take=5,
        order={"createdAt": "desc"}
    )
    tickets = await db.ticket.find_many(
        where={"accountId": account_id, "deletedAt": None}, take=5,
        order={"createdAt": "desc"}
    )
    return {
        "account": account.__dict__,
        "contactCount": len(contacts),
        "openOpportunities": len([o for o in opportunities]),
        "recentTickets": [t.__dict__ for t in tickets],
    }
