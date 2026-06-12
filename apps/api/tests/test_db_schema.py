"""
Schema-level tests that run against a real test PostgreSQL DB.
Requires TEST_DATABASE_URL env var and `prisma migrate deploy` to have run.
These are skipped when the DB is not available (CI will have it).
"""
import os
import pytest
from prisma import Prisma


@pytest.fixture
async def db():
    client = Prisma(datasource={"url": os.getenv("TEST_DATABASE_URL", os.getenv("DATABASE_URL", ""))})
    await client.connect()
    yield client
    await client.disconnect()


@pytest.mark.asyncio
async def test_create_read_user(db: Prisma) -> None:
    user = await db.user.create(
        data={
            "email": f"test_{os.urandom(4).hex()}@test.com",
            "passwordHash": "hashed",
            "firstName": "Test",
            "lastName": "User",
        }
    )
    fetched = await db.user.find_unique(where={"id": user.id})
    assert fetched is not None
    assert fetched.firstName == "Test"
    await db.user.delete(where={"id": user.id})


@pytest.mark.asyncio
async def test_unique_email_constraint(db: Prisma) -> None:
    email = f"unique_{os.urandom(4).hex()}@test.com"
    user = await db.user.create(
        data={"email": email, "passwordHash": "h", "firstName": "A", "lastName": "B"}
    )
    with pytest.raises(Exception):
        await db.user.create(
            data={"email": email, "passwordHash": "h", "firstName": "C", "lastName": "D"}
        )
    await db.user.delete(where={"id": user.id})


@pytest.mark.asyncio
async def test_account_contact_m2m(db: Prisma) -> None:
    account = await db.account.create(data={"name": f"Acct_{os.urandom(4).hex()}"})
    contact = await db.contact.create(
        data={"firstName": "John", "lastName": "Doe", "email": f"jd_{os.urandom(4).hex()}@test.com"}
    )
    link = await db.contactaccount.create(
        data={"contactId": contact.id, "accountId": account.id}
    )
    assert link.contactId == contact.id
    await db.contactaccount.delete(where={"contactId_accountId": {"contactId": contact.id, "accountId": account.id}})
    await db.contact.delete(where={"id": contact.id})
    await db.account.delete(where={"id": account.id})


@pytest.mark.asyncio
async def test_account_parent_hierarchy(db: Prisma) -> None:
    parent = await db.account.create(data={"name": f"Parent_{os.urandom(4).hex()}"})
    child = await db.account.create(data={"name": f"Child_{os.urandom(4).hex()}", "parentId": parent.id})
    fetched = await db.account.find_unique(where={"id": child.id})
    assert fetched is not None
    assert fetched.parentId == parent.id
    await db.account.delete(where={"id": child.id})
    await db.account.delete(where={"id": parent.id})


@pytest.mark.asyncio
async def test_sla_tracker_unique_per_ticket(db: Prisma) -> None:
    user = await db.user.create(
        data={"email": f"sla_{os.urandom(4).hex()}@test.com", "passwordHash": "h", "firstName": "S", "lastName": "L"}
    )
    ticket = await db.ticket.create(
        data={
            "number": f"TKT-{os.urandom(4).hex()}",
            "title": "Test Ticket",
            "description": "desc",
        }
    )
    policy = await db.slapolicy.create(
        data={
            "name": f"SLA_{os.urandom(4).hex()}",
            "accountTier": "SMB",
            "priority": "LOW",
            "firstResponseHours": 24,
            "resolutionHours": 72,
        }
    )
    from datetime import datetime, timedelta
    now = datetime.now()
    tracker = await db.slatracker.create(
        data={
            "ticketId": ticket.id,
            "policyId": policy.id,
            "firstResponseDue": now + timedelta(hours=24),
            "resolutionDue": now + timedelta(hours=72),
        }
    )
    with pytest.raises(Exception):
        await db.slatracker.create(
            data={
                "ticketId": ticket.id,
                "policyId": policy.id,
                "firstResponseDue": now + timedelta(hours=24),
                "resolutionDue": now + timedelta(hours=72),
            }
        )
    await db.slatracker.delete(where={"id": tracker.id})
    await db.ticket.delete(where={"id": ticket.id})
    await db.slapolicy.delete(where={"id": policy.id})
    await db.user.delete(where={"id": user.id})


@pytest.mark.asyncio
async def test_invoice_line_item_cascade_delete(db: Prisma) -> None:
    account = await db.account.create(data={"name": f"Inv_{os.urandom(4).hex()}"})
    from datetime import datetime, timedelta
    now = datetime.now()
    invoice = await db.invoice.create(
        data={
            "number": f"INV-{os.urandom(4).hex()}",
            "accountId": account.id,
            "issueDate": now,
            "dueDate": now + timedelta(days=30),
            "subTotal": 1000,
            "taxAmount": 180,
            "totalAmount": 1180,
        }
    )
    line = await db.invoicelineitem.create(
        data={
            "invoiceId": invoice.id,
            "description": "Service fee",
            "quantity": 1,
            "unitPrice": 1000,
            "total": 1000,
        }
    )
    await db.invoice.delete(where={"id": invoice.id})
    fetched = await db.invoicelineitem.find_unique(where={"id": line.id})
    assert fetched is None
    await db.account.delete(where={"id": account.id})
