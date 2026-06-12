from __future__ import annotations
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional, List
from prisma import Prisma
from app.modules.campaign.schemas import (
    CampaignCreate, CampaignUpdate, SegmentCreate, MetricIngest,
    EventCreate, CampaignMetricsSummary, ROIReport,
)
from app.core.audit import record_audit
from fastapi import HTTPException


async def create_campaign(db: Prisma, data: CampaignCreate, actor_id: str):
    campaign = await db.campaign.create(data={
        "name": data.name,
        "type": data.type.value,
        "status": data.status.value,
        "startDate": data.startDate,
        "endDate": data.endDate,
        "budget": data.budget,
        "currency": data.currency.value,
        "ownerId": data.ownerId or actor_id,
    })
    await record_audit(db, actor_id, "CREATE", "campaigns", record_id=campaign.id)
    return campaign


async def get_campaign(db: Prisma, campaign_id: str):
    campaign = await db.campaign.find_first(
        where={"id": campaign_id, "deletedAt": None},
        include={"segments": True, "metrics": True},
    )
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


async def list_campaigns(db: Prisma, status: Optional[str] = None,
                         type_filter: Optional[str] = None, skip: int = 0, limit: int = 50):
    where: dict = {"deletedAt": None}
    if status:
        where["status"] = status
    if type_filter:
        where["type"] = type_filter
    return await db.campaign.find_many(where=where, skip=skip, take=limit,
                                        order={"createdAt": "desc"})


async def update_campaign(db: Prisma, campaign_id: str, data: CampaignUpdate, actor_id: str):
    await get_campaign(db, campaign_id)
    payload = {k: v for k, v in data.model_dump(exclude_none=True).items()}
    if "status" in payload:
        payload["status"] = payload["status"].value
    campaign = await db.campaign.update(where={"id": campaign_id}, data=payload)
    await record_audit(db, actor_id, "UPDATE", "campaigns", record_id=campaign_id)
    return campaign


async def delete_campaign(db: Prisma, campaign_id: str, actor_id: str):
    await get_campaign(db, campaign_id)
    await db.campaign.update(where={"id": campaign_id},
                              data={"deletedAt": datetime.now(timezone.utc)})
    await record_audit(db, actor_id, "DELETE", "campaigns", record_id=campaign_id)


async def add_segment(db: Prisma, campaign_id: str, data: SegmentCreate, actor_id: str):
    await get_campaign(db, campaign_id)
    segment = await db.audiencesegment.create(data={
        "campaignId": campaign_id,
        "name": data.name,
        "filters": data.filters,
    })
    await record_audit(db, actor_id, "CREATE", "audience_segments", record_id=segment.id)
    return segment


async def ingest_metric(db: Prisma, campaign_id: str, data: MetricIngest, actor_id: str):
    await get_campaign(db, campaign_id)
    metric = await db.campaignmetric.create(data={
        "campaignId": campaign_id,
        "metricKey": data.metricKey,
        "value": data.value,
    })
    await record_audit(db, actor_id, "METRIC_INGEST", "campaign_metrics", record_id=metric.id)
    return metric


async def get_metrics_summary(db: Prisma, campaign_id: str) -> CampaignMetricsSummary:
    metrics = await db.campaignmetric.find_many(where={"campaignId": campaign_id})
    summary: dict = {}
    for m in metrics:
        key = m.metricKey
        val = float(m.value)
        if key not in summary:
            summary[key] = 0.0
        summary[key] += val

    sent = int(summary.get("sent", 0))
    opens = int(summary.get("opens", 0))
    clicks = int(summary.get("clicks", 0))
    conversions = int(summary.get("conversions", 0))
    return CampaignMetricsSummary(
        sent=sent,
        opens=opens,
        clicks=clicks,
        conversions=conversions,
        openRate=round(opens / sent * 100, 2) if sent else 0.0,
        clickRate=round(clicks / sent * 100, 2) if sent else 0.0,
        conversionRate=round(conversions / sent * 100, 2) if sent else 0.0,
    )


async def create_event(db: Prisma, campaign_id: Optional[str], data: EventCreate, actor_id: str):
    event = await db.event.create(data={
        "campaignId": campaign_id,
        "name": data.name,
        "description": data.description,
        "location": data.location,
        "startsAt": data.startsAt,
        "endsAt": data.endsAt,
    })
    await record_audit(db, actor_id, "CREATE", "events", record_id=event.id)
    return event


async def get_roi_report(db: Prisma, campaign_id: str) -> ROIReport:
    campaign = await get_campaign(db, campaign_id)
    attributions = await db.campaignattribution.find_many(
        where={"campaignId": campaign_id},
        include={"opportunity": True},
    )
    leads = sum(1 for a in attributions if a.leadId)
    deals_won = 0
    attributed_revenue = Decimal("0")
    for a in attributions:
        if a.opportunity and a.opportunity.status == "CLOSED_WON":
            deals_won += 1
            attributed_revenue += a.opportunity.value

    budget = campaign.budget or Decimal("0")
    roi = float((attributed_revenue - budget) / budget * 100) if budget else 0.0
    return ROIReport(
        campaignId=campaign_id,
        campaignName=campaign.name,
        budget=budget,
        attributedRevenue=attributed_revenue,
        roi=roi,
        leadsGenerated=leads,
        dealsWon=deals_won,
    )
