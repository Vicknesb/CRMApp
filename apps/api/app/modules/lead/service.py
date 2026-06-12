from prisma import Prisma
from app.core.audit import record_audit
from app.core.enums import LeadStatus
from app.middleware.error_handler import NotFoundError
from app.modules.lead import repository as repo
from app.modules.lead.schemas import (
    ConvertLeadRequest, LeadCreate, LeadListParams, LeadUpdate,
)


async def create_lead(db: Prisma, body: LeadCreate, owner_id: str) -> object:
    existing = await repo.find_duplicate(db, body.email, body.company)
    data = body.model_dump(exclude_none=True)
    data["ownerId"] = owner_id
    lead = await repo.create_lead(db, data)
    await record_audit(db, owner_id, "CREATE", "leads", record_id=lead.id, new_values=data)
    return lead


async def get_lead(db: Prisma, lead_id: str) -> object:
    lead = await repo.get_lead(db, lead_id)
    if not lead:
        raise NotFoundError(f"Lead {lead_id} not found")
    return lead


async def list_leads(db: Prisma, params: LeadListParams) -> tuple[list, int]:
    where: dict = {"deletedAt": None}
    if params.status:
        where["status"] = params.status
    if params.source:
        where["source"] = params.source
    if params.assignee_id:
        where["assigneeId"] = params.assignee_id
    if params.search:
        where["OR"] = [
            {"firstName": {"contains": params.search, "mode": "insensitive"}},
            {"lastName": {"contains": params.search, "mode": "insensitive"}},
            {"email": {"contains": params.search, "mode": "insensitive"}},
            {"company": {"contains": params.search, "mode": "insensitive"}},
        ]
    skip = (params.page - 1) * params.page_size
    leads = await repo.list_leads(db, where, skip, params.page_size)
    total = await repo.count_leads(db, where)
    return leads, total


async def update_lead(db: Prisma, lead_id: str, body: LeadUpdate, actor_id: str) -> object:
    lead = await repo.get_lead(db, lead_id)
    if not lead:
        raise NotFoundError(f"Lead {lead_id} not found")
    data = body.model_dump(exclude_none=True)
    updated = await repo.update_lead(db, lead_id, data)
    await record_audit(db, actor_id, "UPDATE", "leads", record_id=lead_id, new_values=data)
    return updated


async def delete_lead(db: Prisma, lead_id: str, actor_id: str) -> None:
    lead = await repo.get_lead(db, lead_id)
    if not lead:
        raise NotFoundError(f"Lead {lead_id} not found")
    await repo.soft_delete_lead(db, lead_id)
    await record_audit(db, actor_id, "DELETE", "leads", record_id=lead_id)


async def score_lead(db: Prisma, lead_id: str) -> dict:
    lead = await repo.get_lead(db, lead_id)
    if not lead:
        raise NotFoundError(f"Lead {lead_id} not found")
    rules = await repo.get_score_rules(db)
    score = 0
    for rule in rules:
        field_val = getattr(lead, rule.field, None)
        if field_val is not None:
            if rule.operator == "exists":
                score += rule.points
            elif rule.operator == "eq" and str(field_val) == rule.value:
                score += rule.points
    delta = score - lead.score
    await repo.update_lead(db, lead_id, {"score": score})
    if delta != 0:
        await repo.add_score_history(db, lead_id, delta, "Auto-scored by rules")
    return {"leadId": lead_id, "score": score, "delta": delta}


async def assign_lead(db: Prisma, lead_id: str, assignee_id: str, actor_id: str) -> object:
    lead = await repo.get_lead(db, lead_id)
    if not lead:
        raise NotFoundError(f"Lead {lead_id} not found")
    updated = await repo.update_lead(db, lead_id, {"assigneeId": assignee_id})
    await record_audit(db, actor_id, "ASSIGN", "leads", record_id=lead_id,
                       new_values={"assigneeId": assignee_id})
    return updated


async def convert_lead(db: Prisma, lead_id: str, body: ConvertLeadRequest, actor_id: str) -> dict:
    lead = await repo.get_lead(db, lead_id)
    if not lead:
        raise NotFoundError(f"Lead {lead_id} not found")

    result: dict = {"leadId": lead_id}

    if body.createAccount:
        account = await db.account.create(data={
            "name": body.accountName or (lead.company or f"{lead.firstName} {lead.lastName}"),
        })
        result["accountId"] = account.id

    if body.createContact:
        contact = await db.contact.create(data={
            "firstName": lead.firstName,
            "lastName": lead.lastName,
            "email": lead.email,
            "phone": lead.phone,
            "jobTitle": lead.jobTitle,
            "ownerId": actor_id,
        })
        result["contactId"] = contact.id
        if body.createAccount:
            await db.contactaccount.create(data={
                "contactId": contact.id,
                "accountId": result["accountId"],
                "isPrimary": True,
            })

    if body.createOpportunity:
        from datetime import datetime, timedelta
        pipeline = await db.pipeline.find_first(where={"isDefault": True})
        stage = await db.stage.find_first(where={"pipelineId": pipeline.id, "order": 0}) if pipeline else None
        if pipeline and stage:
            opp = await db.opportunity.create(data={
                "title": body.opportunityTitle or f"Opp - {lead.firstName} {lead.lastName}",
                "value": float(lead.budget or 0),
                "closeDate": datetime.utcnow() + timedelta(days=90),
                "stageId": stage.id,
                "accountId": result.get("accountId"),
                "contactId": result.get("contactId"),
                "ownerId": actor_id,
            })
            result["opportunityId"] = opp.id

    await repo.update_lead(db, lead_id, {
        "status": LeadStatus.CONVERTED,
        "convertedAt": __import__("datetime").datetime.utcnow(),
        "accountId": result.get("accountId"),
        "contactId": result.get("contactId"),
        "opportunityId": result.get("opportunityId"),
    })
    await record_audit(db, actor_id, "CONVERT", "leads", record_id=lead_id, new_values=result)
    return result
