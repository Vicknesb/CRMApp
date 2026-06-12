from __future__ import annotations
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import List, Optional
from prisma import Prisma
from app.modules.analytics.schemas import (
    DashboardWidget, DashboardResponse, CustomReportDefinition, ReportResult,
)
from fastapi import HTTPException

# Allowed modules and their safe field lists (injection guard)
ALLOWED_MODULES = {
    "leads": ["id", "status", "score", "source", "createdAt"],
    "opportunities": ["id", "value", "stage", "probability", "closeDate", "createdAt"],
    "accounts": ["id", "tier", "healthScore", "annualRevenue", "createdAt"],
    "tickets": ["id", "status", "priority", "category", "createdAt", "resolvedAt"],
    "invoices": ["id", "status", "totalAmount", "currency", "dueDate", "createdAt"],
    "contracts": ["id", "status", "value", "endDate", "autoRenew"],
}


async def get_dashboard(db: Prisma, role: str) -> DashboardResponse:
    now = datetime.now(timezone.utc)
    widgets: List[DashboardWidget] = []

    # Common widgets
    open_tickets = await db.ticket.count(where={"status": "OPEN", "deletedAt": None})
    widgets.append(DashboardWidget(key="open_tickets", title="Open Tickets", value=open_tickets))

    if role in ("SALES_REP", "SALES_MANAGER", "ADMIN"):
        leads = await db.lead.count(where={"status": "NEW", "deletedAt": None})
        widgets.append(DashboardWidget(key="new_leads", title="New Leads", value=leads))

        opps = await db.opportunity.find_many(
            where={"deletedAt": None, "stage": {"is": {"name": {"not": "CLOSED_LOST"}}}}
        )
        pipeline_value = sum(float(o.value) for o in opps)
        widgets.append(DashboardWidget(key="pipeline_value", title="Pipeline Value",
                                        value=pipeline_value, unit="INR"))

    if role in ("FINANCE", "ADMIN"):
        overdue = await db.invoice.count(where={"status": "OVERDUE", "deletedAt": None})
        widgets.append(DashboardWidget(key="overdue_invoices", title="Overdue Invoices", value=overdue))

        paid = await db.invoice.find_many(where={"status": "PAID", "deletedAt": None})
        rev = sum(float(i.totalAmount) for i in paid)
        widgets.append(DashboardWidget(key="total_revenue", title="Total Revenue",
                                        value=rev, unit="INR"))

    if role in ("PROJECT_MANAGER", "ADMIN"):
        active_projects = await db.project.count(where={"status": "ACTIVE", "deletedAt": None})
        widgets.append(DashboardWidget(key="active_projects", title="Active Projects", value=active_projects))

    if role in ("MARKETING", "ADMIN"):
        active_campaigns = await db.campaign.count(where={"status": "ACTIVE", "deletedAt": None})
        widgets.append(DashboardWidget(key="active_campaigns", title="Active Campaigns", value=active_campaigns))

    return DashboardResponse(role=role, widgets=widgets)


# ── Pre-built reports (all 10 from SRS §9.1) ─────────────────────────────────

async def report_pipeline_summary(db: Prisma) -> dict:
    stages = await db.stage.find_many(include={"opportunities": True})
    return {
        "stages": [
            {"name": s.name, "count": len(s.opportunities),
             "value": sum(float(o.value) for o in s.opportunities)}
            for s in stages
        ]
    }


async def report_lead_conversion_funnel(db: Prisma) -> dict:
    statuses = ["NEW", "CONTACTED", "QUALIFIED", "CONVERTED", "UNQUALIFIED"]
    result = {}
    for s in statuses:
        result[s] = await db.lead.count(where={"status": s, "deletedAt": None})
    return result


async def report_revenue_forecast(db: Prisma) -> dict:
    opps = await db.opportunity.find_many(
        where={"deletedAt": None},
        include={"stage": True},
    )
    weighted_total = sum(float(o.value) * (o.stage.probability / 100) for o in opps if o.stage)
    return {"weightedForecast": weighted_total, "totalPipeline": sum(float(o.value) for o in opps)}


async def report_rep_performance(db: Prisma) -> list:
    users = await db.user.find_many(
        where={"role": {"in": ["SALES_REP", "SALES_MANAGER"]}, "deletedAt": None},
        include={"ownedLeads": True, "opportunities": True},
    )
    return [
        {"id": u.id, "name": f"{u.firstName} {u.lastName}",
         "leads": len(u.ownedLeads), "opportunities": len(u.opportunities)}
        for u in users
    ]


async def report_account_health(db: Prisma) -> list:
    accounts = await db.account.find_many(
        where={"deletedAt": None},
        order={"healthScore": "asc"},
        take=50,
    )
    return [{"id": a.id, "name": a.name, "tier": a.tier, "healthScore": a.healthScore} for a in accounts]


async def report_sla_compliance(db: Prisma) -> dict:
    trackers = await db.slatracker.find_many()
    total = len(trackers)
    met = sum(1 for t in trackers if t.resolutionMet is True)
    return {"total": total, "met": met, "breached": total - met,
            "complianceRate": round(met / total * 100, 1) if total else 0}


async def report_ticket_volume(db: Prisma) -> dict:
    statuses = ["OPEN", "IN_PROGRESS", "WAITING", "RESOLVED", "CLOSED"]
    return {s: await db.ticket.count(where={"status": s, "deletedAt": None}) for s in statuses}


async def report_campaign_roi(db: Prisma) -> list:
    campaigns = await db.campaign.find_many(where={"deletedAt": None}, include={"metrics": True})
    result = []
    for c in campaigns:
        budget = float(c.budget or 0)
        # Use attributions for revenue
        attributions = await db.campaignattribution.find_many(
            where={"campaignId": c.id}, include={"opportunity": True}
        )
        revenue = sum(float(a.opportunity.value) for a in attributions
                      if a.opportunity and getattr(a.opportunity, "status", "") == "CLOSED_WON")
        roi = (revenue - budget) / budget * 100 if budget else 0
        result.append({"id": c.id, "name": c.name, "budget": budget,
                        "attributedRevenue": revenue, "roi": round(roi, 1)})
    return result


async def report_contract_renewal_pipeline(db: Prisma) -> list:
    now = datetime.now(timezone.utc)
    contracts = await db.contract.find_many(
        where={"status": "ACTIVE", "deletedAt": None,
               "endDate": {"lte": now + timedelta(days=90)}},
        order={"endDate": "asc"},
    )
    return [{"id": c.id, "number": c.number, "title": c.title,
             "endDate": c.endDate.isoformat(), "autoRenew": c.autoRenew,
             "daysLeft": (c.endDate.replace(tzinfo=timezone.utc) - now).days}
            for c in contracts]


async def report_invoice_aging(db: Prisma) -> dict:
    now = datetime.now(timezone.utc)
    invoices = await db.invoice.find_many(
        where={"status": {"in": ["SENT", "OVERDUE"]}, "deletedAt": None}
    )
    buckets: dict = {"0-30": 0.0, "31-60": 0.0, "61-90": 0.0, "90+": 0.0}
    for inv in invoices:
        age = (now - inv.dueDate.replace(tzinfo=timezone.utc)).days
        if age <= 30:
            buckets["0-30"] += float(inv.totalAmount)
        elif age <= 60:
            buckets["31-60"] += float(inv.totalAmount)
        elif age <= 90:
            buckets["61-90"] += float(inv.totalAmount)
        else:
            buckets["90+"] += float(inv.totalAmount)
    return buckets


REPORT_MAP = {
    "pipeline_summary": report_pipeline_summary,
    "lead_conversion_funnel": report_lead_conversion_funnel,
    "revenue_forecast": report_revenue_forecast,
    "rep_performance": report_rep_performance,
    "account_health": report_account_health,
    "sla_compliance": report_sla_compliance,
    "ticket_volume": report_ticket_volume,
    "campaign_roi": report_campaign_roi,
    "contract_renewal_pipeline": report_contract_renewal_pipeline,
    "invoice_aging": report_invoice_aging,
}


async def run_prebuilt_report(db: Prisma, report_key: str) -> dict:
    fn = REPORT_MAP.get(report_key)
    if not fn:
        raise HTTPException(status_code=404, detail=f"Report '{report_key}' not found")
    result = await fn(db)
    return {"reportKey": report_key, "data": result}


async def run_custom_report(db: Prisma, defn: CustomReportDefinition) -> ReportResult:
    if defn.module not in ALLOWED_MODULES:
        raise HTTPException(status_code=422, detail=f"Module '{defn.module}' not allowed")
    allowed = ALLOWED_MODULES[defn.module]
    for f in defn.fields:
        if f not in allowed:
            raise HTTPException(status_code=422, detail=f"Field '{f}' not allowed in {defn.module}")
    if defn.aggregateField and defn.aggregateField not in allowed:
        raise HTTPException(status_code=422, detail=f"Aggregate field '{defn.aggregateField}' not allowed")

    # Simple count implementation (full SQL builder would use raw queries)
    model = getattr(db, defn.module.rstrip("s"), None) or getattr(db, defn.module, None)
    if model is None:
        raise HTTPException(status_code=422, detail=f"Cannot resolve model for {defn.module}")

    where: dict = {}
    for f in defn.filters:
        op_map = {"eq": f.value, "gt": {"gt": f.value}, "lt": {"lt": f.value},
                  "gte": {"gte": f.value}, "lte": {"lte": f.value}}
        where[f.field] = op_map.get(f.operator, f.value)

    rows = await model.find_many(where=where, take=500)
    result_rows = []
    for r in rows:
        row = {}
        for field in defn.fields:
            row[field] = getattr(r, field, None)
        result_rows.append(row)

    return ReportResult(columns=defn.fields, rows=result_rows, total=len(result_rows))
