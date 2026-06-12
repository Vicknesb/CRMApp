from datetime import datetime, timezone
from prisma import Prisma
from app.core.audit import record_audit
from app.middleware.error_handler import NotFoundError
from app.modules.contact.schemas import ContactCreate, ContactUpdate, InteractionCreate


async def create_contact(db: Prisma, body: ContactCreate, owner_id: str) -> object:
    data = body.model_dump(exclude_none=True)
    data["ownerId"] = owner_id
    contact = await db.contact.create(data=data)
    await record_audit(db, owner_id, "CREATE", "contacts", record_id=contact.id, new_values=data)
    return contact


async def get_contact(db: Prisma, contact_id: str) -> object:
    contact = await db.contact.find_first(where={"id": contact_id, "deletedAt": None})
    if not contact:
        raise NotFoundError(f"Contact {contact_id} not found")
    return contact


async def list_contacts(db: Prisma, page: int, page_size: int, search: str | None) -> tuple[list, int]:
    where: dict = {"deletedAt": None}
    if search:
        where["OR"] = [
            {"firstName": {"contains": search, "mode": "insensitive"}},
            {"lastName": {"contains": search, "mode": "insensitive"}},
            {"email": {"contains": search, "mode": "insensitive"}},
        ]
    skip = (page - 1) * page_size
    contacts = await db.contact.find_many(where=where, skip=skip, take=page_size,
                                          order={"createdAt": "desc"})
    total = await db.contact.count(where=where)
    return contacts, total


async def update_contact(db: Prisma, contact_id: str, body: ContactUpdate, actor_id: str) -> object:
    contact = await db.contact.find_first(where={"id": contact_id, "deletedAt": None})
    if not contact:
        raise NotFoundError(f"Contact {contact_id} not found")
    data = body.model_dump(exclude_none=True)
    updated = await db.contact.update(where={"id": contact_id}, data=data)
    await record_audit(db, actor_id, "UPDATE", "contacts", record_id=contact_id, new_values=data)
    return updated


async def delete_contact(db: Prisma, contact_id: str, actor_id: str) -> None:
    contact = await db.contact.find_first(where={"id": contact_id, "deletedAt": None})
    if not contact:
        raise NotFoundError(f"Contact {contact_id} not found")
    await db.contact.update(where={"id": contact_id},
                            data={"deletedAt": datetime.now(timezone.utc)})
    await record_audit(db, actor_id, "DELETE", "contacts", record_id=contact_id)


async def log_interaction(db: Prisma, contact_id: str, body: InteractionCreate, actor_id: str) -> object:
    contact = await db.contact.find_first(where={"id": contact_id, "deletedAt": None})
    if not contact:
        raise NotFoundError(f"Contact {contact_id} not found")
    interaction = await db.interaction.create(data={
        "contactId": contact_id,
        "type": body.type,
        "summary": body.summary,
        "happenedAt": body.happenedAt,
    })
    return interaction


async def get_interactions(db: Prisma, contact_id: str) -> list:
    return await db.interaction.find_many(
        where={"contactId": contact_id},
        order={"happenedAt": "desc"},
    )


async def link_account(db: Prisma, contact_id: str, account_id: str, is_primary: bool) -> object:
    return await db.contactaccount.upsert(
        where={"contactId_accountId": {"contactId": contact_id, "accountId": account_id}},
        data={
            "create": {"contactId": contact_id, "accountId": account_id, "isPrimary": is_primary},
            "update": {"isPrimary": is_primary},
        },
    )
