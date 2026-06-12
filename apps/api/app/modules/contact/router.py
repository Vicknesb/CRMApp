from fastapi import APIRouter, Depends, Query, status
from prisma import Prisma
from typing import Optional

from app.core.dependencies import get_current_user
from app.core.envelope import ok
from app.db.client import get_db
from app.modules.contact import service
from app.modules.contact.schemas import ContactCreate, ContactUpdate, InteractionCreate

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactCreate, db: Prisma = Depends(get_db),
                         current_user=Depends(get_current_user)) -> dict:
    contact = await service.create_contact(db, body, current_user.id)
    return ok(contact.__dict__)


@router.get("")
async def list_contacts(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
                        search: Optional[str] = None, db: Prisma = Depends(get_db),
                        current_user=Depends(get_current_user)) -> dict:
    contacts, total = await service.list_contacts(db, page, page_size, search)
    return ok([c.__dict__ for c in contacts],
              meta={"total": total, "page": page, "page_size": page_size})


@router.get("/{contact_id}")
async def get_contact(contact_id: str, db: Prisma = Depends(get_db),
                      current_user=Depends(get_current_user)) -> dict:
    return ok((await service.get_contact(db, contact_id)).__dict__)


@router.patch("/{contact_id}")
async def update_contact(contact_id: str, body: ContactUpdate, db: Prisma = Depends(get_db),
                         current_user=Depends(get_current_user)) -> dict:
    return ok((await service.update_contact(db, contact_id, body, current_user.id)).__dict__)


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: str, db: Prisma = Depends(get_db),
                         current_user=Depends(get_current_user)) -> None:
    await service.delete_contact(db, contact_id, current_user.id)


@router.post("/{contact_id}/interactions", status_code=status.HTTP_201_CREATED)
async def log_interaction(contact_id: str, body: InteractionCreate,
                          db: Prisma = Depends(get_db), current_user=Depends(get_current_user)) -> dict:
    return ok((await service.log_interaction(db, contact_id, body, current_user.id)).__dict__)


@router.get("/{contact_id}/interactions")
async def get_interactions(contact_id: str, db: Prisma = Depends(get_db),
                           current_user=Depends(get_current_user)) -> dict:
    interactions = await service.get_interactions(db, contact_id)
    return ok([i.__dict__ for i in interactions])


@router.post("/{contact_id}/accounts/{account_id}", status_code=status.HTTP_201_CREATED)
async def link_account(contact_id: str, account_id: str,
                       is_primary: bool = Query(False),
                       db: Prisma = Depends(get_db), current_user=Depends(get_current_user)) -> dict:
    return ok((await service.link_account(db, contact_id, account_id, is_primary)).__dict__)
