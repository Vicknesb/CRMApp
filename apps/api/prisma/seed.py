"""
Idempotent seed script for CRM reference + demo data.
Run: python -m prisma generate && python prisma/seed.py
"""
import asyncio
import hashlib
from datetime import datetime, timedelta
from decimal import Decimal

from prisma import Prisma


async def seed(db: Prisma) -> None:
    print("Seeding reference data...")

    # ── Users / Roles ────────────────────────────────────────────────────
    password_hash = hashlib.sha256(b"Admin@1234").hexdigest()

    admin = await db.user.upsert(
        where={"email": "admin@ideas2it.com"},
        data={
            "create": {
                "email": "admin@ideas2it.com",
                "passwordHash": password_hash,
                "firstName": "Admin",
                "lastName": "User",
                "role": "ADMIN",
            },
            "update": {},
        },
    )

    sales_mgr = await db.user.upsert(
        where={"email": "sales.manager@ideas2it.com"},
        data={
            "create": {
                "email": "sales.manager@ideas2it.com",
                "passwordHash": password_hash,
                "firstName": "Ravi",
                "lastName": "Kumar",
                "role": "SALES_MANAGER",
            },
            "update": {},
        },
    )

    sales_rep = await db.user.upsert(
        where={"email": "sales.rep@ideas2it.com"},
        data={
            "create": {
                "email": "sales.rep@ideas2it.com",
                "passwordHash": password_hash,
                "firstName": "Priya",
                "lastName": "Sharma",
                "role": "SALES_REP",
            },
            "update": {},
        },
    )

    # ── Pipelines & Stages ───────────────────────────────────────────────
    pipeline = await db.pipeline.upsert(
        where={"name": "IT Services Sales"},
        data={
            "create": {"name": "IT Services Sales", "isDefault": True},
            "update": {},
        },
    )

    stages_data = [
        ("Prospecting", 0, 10, "#6366f1"),
        ("Qualification", 1, 25, "#3b82f6"),
        ("Proposal", 2, 50, "#f59e0b"),
        ("Negotiation", 3, 75, "#f97316"),
        ("Closed Won", 4, 100, "#22c55e"),
        ("Closed Lost", 5, 0, "#ef4444"),
    ]

    stages = []
    for name, order, prob, color in stages_data:
        stage = await db.stage.upsert(
            where={"pipelineId_order": {"pipelineId": pipeline.id, "order": order}},
            data={
                "create": {
                    "pipelineId": pipeline.id,
                    "name": name,
                    "order": order,
                    "probability": prob,
                    "color": color,
                },
                "update": {"name": name, "probability": prob},
            },
        )
        stages.append(stage)

    # ── SLA Policies ─────────────────────────────────────────────────────
    sla_configs = [
        ("STRATEGIC", "CRITICAL", 1, 4),
        ("STRATEGIC", "HIGH", 2, 8),
        ("STRATEGIC", "MEDIUM", 4, 24),
        ("ENTERPRISE", "CRITICAL", 2, 8),
        ("ENTERPRISE", "HIGH", 4, 16),
        ("ENTERPRISE", "MEDIUM", 8, 48),
        ("SMB", "CRITICAL", 4, 16),
        ("SMB", "HIGH", 8, 48),
        ("SMB", "MEDIUM", 24, 72),
    ]

    for tier, priority, first_resp, resolution in sla_configs:
        await db.slapolicy.upsert(
            where={"accountTier_priority": {"accountTier": tier, "priority": priority}},
            data={
                "create": {
                    "name": f"{tier} {priority} SLA",
                    "accountTier": tier,
                    "priority": priority,
                    "firstResponseHours": first_resp,
                    "resolutionHours": resolution,
                },
                "update": {"firstResponseHours": first_resp, "resolutionHours": resolution},
            },
        )

    # ── KB Categories ────────────────────────────────────────────────────
    kb_categories = ["Getting Started", "Billing & Invoicing", "Technical Support",
                     "Product Features", "Integrations", "FAQs"]
    for cat_name in kb_categories:
        await db.kbcategory.upsert(
            where={"name": cat_name},
            data={"create": {"name": cat_name}, "update": {}},
        )

    # ── Demo Accounts ─────────────────────────────────────────────────────
    account = await db.account.upsert(
        where={"id": "00000000-0000-0000-0000-000000000001"},
        data={
            "create": {
                "id": "00000000-0000-0000-0000-000000000001",
                "name": "Tata Consultancy Services",
                "industry": "IT Services",
                "website": "https://www.tcs.com",
                "tier": "STRATEGIC",
                "healthScore": 85,
                "annualRevenue": Decimal("50000000"),
                "currency": "INR",
            },
            "update": {},
        },
    )

    # ── Demo Contact ──────────────────────────────────────────────────────
    contact = await db.contact.upsert(
        where={"id": "00000000-0000-0000-0000-000000000002"},
        data={
            "create": {
                "id": "00000000-0000-0000-0000-000000000002",
                "firstName": "Ananya",
                "lastName": "Krishnan",
                "email": "ananya.krishnan@tcs.com",
                "jobTitle": "CTO",
                "ownerId": sales_mgr.id,
            },
            "update": {},
        },
    )

    # ── Demo Lead ─────────────────────────────────────────────────────────
    await db.lead.upsert(
        where={"id": "00000000-0000-0000-0000-000000000003"},
        data={
            "create": {
                "id": "00000000-0000-0000-0000-000000000003",
                "firstName": "Vikram",
                "lastName": "Nair",
                "email": "vikram.nair@infosys.com",
                "company": "Infosys",
                "source": "LINKEDIN",
                "status": "QUALIFIED",
                "score": 72,
                "budget": Decimal("2500000"),
                "currency": "INR",
                "ownerId": sales_rep.id,
            },
            "update": {},
        },
    )

    # ── Demo Opportunity ──────────────────────────────────────────────────
    await db.opportunity.upsert(
        where={"id": "00000000-0000-0000-0000-000000000004"},
        data={
            "create": {
                "id": "00000000-0000-0000-0000-000000000004",
                "title": "Digital Transformation - TCS",
                "value": Decimal("7500000"),
                "currency": "INR",
                "closeDate": datetime.now() + timedelta(days=60),
                "serviceType": "Consulting + Implementation",
                "probability": 50,
                "stageId": stages[2].id,
                "accountId": account.id,
                "contactId": contact.id,
                "ownerId": sales_mgr.id,
            },
            "update": {},
        },
    )

    print("✅ Seed complete.")


async def main() -> None:
    db = Prisma()
    await db.connect()
    try:
        await seed(db)
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
