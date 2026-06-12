from fastapi import APIRouter, Depends, Query, status
from prisma import Prisma
from typing import Optional

from app.core.dependencies import get_current_user, require_role
from app.core.enums import UserRole, TicketStatus, TicketPriority
from app.core.envelope import ok
from app.db.client import get_db
from app.modules.ticket import service
from app.modules.ticket.schemas import TicketCreate, TicketNoteCreate, TicketUpdate

router = APIRouter(prefix="/tickets", tags=["tickets"])

_support_roles = require_role(UserRole.SUPPORT_AGENT, UserRole.ADMIN, UserRole.SALES_MANAGER)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_ticket(body: TicketCreate, db: Prisma = Depends(get_db),
                        current_user=Depends(get_current_user)) -> dict:
    return ok((await service.create_ticket(db, body, current_user.id)).__dict__)


@router.get("")
async def list_tickets(
    status: Optional[TicketStatus] = None,
    priority: Optional[TicketPriority] = None,
    assignee_id: Optional[str] = None,
    account_id: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Prisma = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict:
    tickets, total = await service.list_tickets(
        db, status, priority, assignee_id, account_id, search, page, page_size
    )
    return ok([t.__dict__ for t in tickets], meta={"total": total, "page": page, "page_size": page_size})


@router.get("/{ticket_id}")
async def get_ticket(ticket_id: str, db: Prisma = Depends(get_db),
                     current_user=Depends(get_current_user)) -> dict:
    return ok((await service.get_ticket(db, ticket_id)).__dict__)


@router.patch("/{ticket_id}")
async def update_ticket(ticket_id: str, body: TicketUpdate,
                        db: Prisma = Depends(get_db),
                        current_user=Depends(_support_roles)) -> dict:
    return ok((await service.update_ticket(db, ticket_id, body, current_user.id)).__dict__)


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(ticket_id: str, db: Prisma = Depends(get_db),
                        current_user=Depends(require_role(UserRole.ADMIN))) -> None:
    await service.delete_ticket(db, ticket_id, current_user.id)


@router.post("/{ticket_id}/notes", status_code=status.HTTP_201_CREATED)
async def add_note(ticket_id: str, body: TicketNoteCreate,
                   db: Prisma = Depends(get_db),
                   current_user=Depends(get_current_user)) -> dict:
    return ok((await service.add_note(db, ticket_id, body, current_user.id)).__dict__)


@router.get("/{ticket_id}/notes")
async def list_notes(ticket_id: str, db: Prisma = Depends(get_db),
                     current_user=Depends(get_current_user)) -> dict:
    notes = await service.list_notes(db, ticket_id)
    return ok([n.__dict__ for n in notes])
