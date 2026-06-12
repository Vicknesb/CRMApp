from datetime import datetime, timezone
from prisma import Prisma
from app.core.audit import record_audit
from app.core.enums import TicketStatus
from app.middleware.error_handler import NotFoundError
from app.modules.ticket.schemas import TicketCreate, TicketNoteCreate, TicketUpdate


async def create_ticket(db: Prisma, body: TicketCreate, reporter_id: str) -> object:
    data = body.model_dump(exclude_none=True)
    data["reporterId"] = reporter_id
    # Generate a sequential ticket number
    count = await db.ticket.count()
    data["ticketNumber"] = f"TKT-{count + 1:05d}"
    ticket = await db.ticket.create(data=data)
    await record_audit(db, reporter_id, "CREATE", "tickets", record_id=ticket.id, new_values=data)
    return ticket


async def get_ticket(db: Prisma, ticket_id: str) -> object:
    ticket = await db.ticket.find_first(where={"id": ticket_id, "deletedAt": None})
    if not ticket:
        raise NotFoundError(f"Ticket {ticket_id} not found")
    return ticket


async def list_tickets(db: Prisma, status: str | None, priority: str | None,
                       assignee_id: str | None, account_id: str | None,
                       search: str | None, page: int, page_size: int) -> tuple[list, int]:
    where: dict = {"deletedAt": None}
    if status:
        where["status"] = status
    if priority:
        where["priority"] = priority
    if assignee_id:
        where["assigneeId"] = assignee_id
    if account_id:
        where["accountId"] = account_id
    if search:
        where["OR"] = [
            {"subject": {"contains": search, "mode": "insensitive"}},
            {"ticketNumber": {"contains": search, "mode": "insensitive"}},
        ]
    skip = (page - 1) * page_size
    tickets = await db.ticket.find_many(where=where, skip=skip, take=page_size,
                                        order={"createdAt": "desc"})
    total = await db.ticket.count(where=where)
    return tickets, total


async def update_ticket(db: Prisma, ticket_id: str, body: TicketUpdate, actor_id: str) -> object:
    ticket = await db.ticket.find_first(where={"id": ticket_id, "deletedAt": None})
    if not ticket:
        raise NotFoundError(f"Ticket {ticket_id} not found")
    data = body.model_dump(exclude_none=True)
    if data.get("status") == TicketStatus.RESOLVED:
        data["resolvedAt"] = datetime.now(timezone.utc)
    updated = await db.ticket.update(where={"id": ticket_id}, data=data)
    await record_audit(db, actor_id, "UPDATE", "tickets", record_id=ticket_id, new_values=data)
    return updated


async def delete_ticket(db: Prisma, ticket_id: str, actor_id: str) -> None:
    ticket = await db.ticket.find_first(where={"id": ticket_id, "deletedAt": None})
    if not ticket:
        raise NotFoundError(f"Ticket {ticket_id} not found")
    await db.ticket.update(where={"id": ticket_id},
                           data={"deletedAt": datetime.now(timezone.utc)})
    await record_audit(db, actor_id, "DELETE", "tickets", record_id=ticket_id)


async def add_note(db: Prisma, ticket_id: str, body: TicketNoteCreate, author_id: str) -> object:
    ticket = await db.ticket.find_first(where={"id": ticket_id, "deletedAt": None})
    if not ticket:
        raise NotFoundError(f"Ticket {ticket_id} not found")
    note = await db.ticketnote.create(data={
        "ticketId": ticket_id,
        "authorId": author_id,
        "body": body.body,
        "isInternal": body.isInternal,
    })
    await record_audit(db, author_id, "NOTE_ADDED", "tickets", record_id=ticket_id)
    return note


async def list_notes(db: Prisma, ticket_id: str) -> list:
    return await db.ticketnote.find_many(
        where={"ticketId": ticket_id},
        order={"createdAt": "asc"},
    )
