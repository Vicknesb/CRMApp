# EPIC-CAMP · Marketing & Campaign Management

> **Epic goal:** Campaigns, segments, performance, drip sequences, events, ROI. **SRS:** §3.9 (MK-001).
> **Mockups:** `10-campaigns.html`, `form-09-campaign.html`. **Depends on:** EPIC-AUTH, EPIC-LEAD, EPIC-INTG(email marketing).

---

### CAMP-1 · Story · Campaign schema (Campaign, AudienceSegment, CampaignMetric, Event)
- **Points:** 3 **SRS:** MK-001 **Depends on:** AUTH-1
- **Description:** Campaign (type, status, budget, dates), AudienceSegment (criteria JSON), CampaignMetric (sent/opens/clicks/conversions), Event. Seed.
- **AC:** [ ] migration + seed.
- **Unit Tests:** [ ] repo CRUD.

### CAMP-2 · Task · Schemas (Pydantic/Zod)
- **Points:** 1 **Depends on:** CAMP-1
- **AC:** [ ] campaign/segment/event schemas.
- **Unit Tests:** [ ] parse.

### CAMP-3 · Story · Campaign CRUD + segments API
- **Points:** 3 **SRS:** MK-001 **Depends on:** CAMP-2, AUTH-7
- **AC:** [ ] CRUD + segment builder + RBAC(Marketing/Admin) + audit.
- **Unit Tests:** [ ] CRUD; [ ] segment resolution.

### CAMP-4 · Story · Performance tracking
- **Points:** 3 **SRS:** MK-001 **Depends on:** CAMP-3, INTG-7(email marketing)
- **AC:** [ ] ingest metrics; compute open/click/conversion rates.
- **Unit Tests:** [ ] rate math; [ ] metric ingest.

### CAMP-5 · Story · Drip email sequences
- **Points:** 3 **SRS:** §3.9 **Depends on:** CAMP-3
- **AC:** [ ] multi-step nurture w/ delays + triggers.
- **Unit Tests:** [ ] step scheduling (frozen clock); [ ] trigger branch.

### CAMP-6 · Task · Event management
- **Points:** 2 **SRS:** §3.9 **Depends on:** CAMP-3
- **AC:** [ ] webinar/conference CRUD + registrations.
- **Unit Tests:** [ ] registration; [ ] capacity.

### CAMP-7 · Story · ROI attribution
- **Points:** 3 **SRS:** MK-001 (AN-001) **Depends on:** CAMP-3, LEAD-9
- **AC:** [ ] attribute revenue: campaign→leads→deals.
- **Unit Tests:** [ ] attribution mapping; [ ] ROI calc.

### CAMP-8 · Task · Frontend hooks
- **Points:** 2 **Depends on:** CAMP-3
- **AC:** [ ] `useCampaigns/useCampaign/useSegments/useCampaignMetrics`.
- **Unit Tests:** [ ] fetch + invalidation.

### CAMP-9 · Story · UI: Campaign list
- **Points:** 2 **SRS:** §7.2 **Depends on:** CAMP-8
- **AC:** [ ] mirror `10-campaigns.html` (cards, metrics).
- **Unit Tests:** [ ] render; [ ] filter.

### CAMP-10 · Story · UI: Campaign form
- **Points:** 3 **SRS:** MK-001 **Depends on:** CAMP-8
- **Description:** mirror `form-09-campaign.html` (type pills, audience, schedule, budget, health checklist, estimated metrics); Cancel→list.
- **AC:** [ ] persists.
- **Unit Tests:** [ ] validation; [ ] submit.

### CAMP-11 · Story · UI: Campaign analytics
- **Points:** 3 **Depends on:** CAMP-8, CAMP-7
- **AC:** [ ] performance + ROI charts.
- **Unit Tests:** [ ] chart binds metrics.

### CAMP-12 · Task · Seed/fixtures
- **Points:** 1 **Depends on:** CAMP-1
- **AC:** [ ] campaigns + metrics seeded.
- **Unit Tests:** [ ] idempotent.

### CAMP-13 · Check · Campaign module-wide check
- **Points:** 2 **Depends on:** CAMP-1…12
- **AC:** [ ] campaign→metrics→ROI E2E; ≥80% coverage; MK-001 satisfied.
- **Unit Tests:** [ ] integration covering create→track→attribute.
