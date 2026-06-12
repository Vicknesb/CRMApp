# EPIC-PIPE · Opportunity & Sales Pipeline

> **Epic goal:** Deals, multi-pipeline Kanban, forecasting, proposals/quotes. **SRS:** §3.3 (PL-001/002/003).
> **Mockups:** `05-pipeline.html`, `form-04-deal.html`. **Depends on:** EPIC-AUTH, EPIC-ACCT, EPIC-CONT.

---

### PIPE-1 · Story · Pipeline schema (Pipeline, Stage, Opportunity, Proposal, Quote, Product)
- **Points:** 5 **SRS:** PL-001/002/003 **Depends on:** AUTH-1, ACCT-1, CONT-1
- **Description:** pipelines/stages (order, probability), opportunity (value, closeDate, serviceType, stageId, links), product/service catalog, proposal/quote (items, total, status, version). Seed New Business/Renewals/Upsell.
- **AC:** [ ] migration + multi-pipeline seed.
- **Unit Tests:** [ ] repo CRUD; [ ] seed pipelines.

### PIPE-2 · Task · Pipeline schemas (Pydantic/Zod)
- **Points:** 1 **Depends on:** PIPE-1
- **AC:** [ ] deal/proposal/quote schemas.
- **Unit Tests:** [ ] parse.

### PIPE-3 · Story · Deal CRUD API
- **Points:** 3 **SRS:** PL-001 **Depends on:** PIPE-2, AUTH-7
- **AC:** [ ] CRUD + filter + RBAC + audit.
- **Unit Tests:** [ ] endpoints; [ ] RBAC.

### PIPE-4 · Task · Color-coding metadata (value/age/priority)
- **Points:** 1 **SRS:** §3.3.2 **Depends on:** PIPE-3
- **AC:** [ ] derived flags returned for UI coloring.
- **Unit Tests:** [ ] age/value bucket logic.

### PIPE-5 · Story · Multiple pipelines + custom stages
- **Points:** 3 **SRS:** PL-001 **Depends on:** PIPE-3
- **AC:** [ ] CRUD pipelines/stages; deals scoped to pipeline.
- **Unit Tests:** [ ] stage set per pipeline.

### PIPE-6 · Story · Stage move + probability + history
- **Points:** 2 **SRS:** §3.3.2 **Depends on:** PIPE-3
- **AC:** [ ] `/opportunities/:id/stage` valid transitions; stage history recorded.
- **Unit Tests:** [ ] transition validation; [ ] history append.

### PIPE-7 · Story · Revenue forecasting (weighted)
- **Points:** 3 **SRS:** PL-002 **Depends on:** PIPE-3
- **Description:** `/forecast` Σ(value×probability) grouped by month/quarter.
- **AC:** [ ] weighted totals per period.
- **Unit Tests:** [ ] weighting math; [ ] grouping; [ ] empty pipeline.

### PIPE-8 · Story · Proposal/quote generation + approval workflow
- **Points:** 5 **SRS:** PL-003 **Depends on:** PIPE-3
- **Description:** itemized from catalog; approval required above threshold.
- **AC:** [ ] above-threshold needs approval before send.
- **Unit Tests:** [ ] total calc; [ ] threshold gate; [ ] approval transition.

### PIPE-9 · Story · Proposal email send + tracking + versioning
- **Points:** 3 **SRS:** §3.3.3 **Depends on:** PIPE-8, INTG-2(email)
- **AC:** [ ] send via CRM; open/view tracked; revisions bump version.
- **Unit Tests:** [ ] version increment; [ ] tracking event recorded.

### PIPE-10 · Task · Frontend hooks
- **Points:** 2 **Depends on:** PIPE-3
- **AC:** [ ] `useOpportunities/useDeal/useMoveStage/useForecast/useProposal`.
- **Unit Tests:** [ ] fetch + invalidation.

### PIPE-11 · Story · UI: Kanban board
- **Points:** 3 **SRS:** §7.2 **Depends on:** PIPE-10, PIPE-6
- **Description:** mirror `05-pipeline.html` (5 stages, drag-drop, grid no-scroll, weighted total).
- **AC:** [ ] DnD persists stage.
- **Unit Tests:** [ ] DnD calls move; [ ] column totals.

### PIPE-12 · Story · UI: Deal list view
- **Points:** 2 **SRS:** §3.3.2 **Depends on:** PIPE-10, PIPE-4
- **AC:** [ ] filterable, color-coded by value/age/priority.
- **Unit Tests:** [ ] sort/filter; [ ] color class.

### PIPE-13 · Story · UI: Deal form
- **Points:** 3 **SRS:** PL-001 **Depends on:** PIPE-10
- **Description:** mirror `form-04-deal.html` (basics, stage pills, probability, team); Cancel→pipeline.
- **AC:** [ ] persists.
- **Unit Tests:** [ ] validation; [ ] submit.

### PIPE-14 · Story · UI: Deal detail timeline
- **Points:** 2 **SRS:** §7.2 **Depends on:** PIPE-10
- **AC:** [ ] timeline of activities/docs/notes/stage history.
- **Unit Tests:** [ ] timeline render.

### PIPE-15 · Story · UI: Proposal builder
- **Points:** 3 **SRS:** PL-003 **Depends on:** PIPE-10, PIPE-8
- **AC:** [ ] line items from catalog; totals; submit-for-approval; send.
- **Unit Tests:** [ ] total recompute; [ ] approval submit.

### PIPE-16 · Check · Pipeline module-wide check
- **Points:** 2 **Depends on:** PIPE-1…15
- **AC:** [ ] deal→stage→forecast→proposal E2E; ≥80% coverage; PL-001/002/003 satisfied.
- **Unit Tests:** [ ] integration covering create→move→forecast→proposal.
