# EPIC-LEAD · Lead Management

> **Epic goal:** Capture, qualify, score, dedupe, and convert leads. **SRS:** §3.1 (LM-001/002/003).
> **Mockups:** `02-leads.html`, `form-01-lead.html`. **Depends on:** EPIC-AUTH (+ CONT/ACCT/PIPE schemas for conversion).

---

### LEAD-1 · Story · Lead schema (Lead, LeadSource, LeadScoreRule)
- **Points:** 3 **SRS:** LM-001 **Depends on:** AUTH-1
- **Description:** Models incl. source enum, UTM fields, status (New/MQL/SQL/Unqualified), score, BANT JSON, owner; scoring rules. Seed varied leads.
- **AC:** [ ] Migration + seed; indexes on email/status/owner.
- **Unit Tests:** [ ] repo CRUD; [ ] seed creates all statuses.

### LEAD-2 · Task · Lead Pydantic/Zod schemas
- **Points:** 1 **SRS:** LM-001 **Depends on:** LEAD-1
- **Description:** create/update/convert/score-rule models (API Pydantic + web Zod).
- **AC:** [ ] Used by router + form.
- **Unit Tests:** [ ] valid/invalid payload parsing.

### LEAD-3 · Story · Lead CRUD API
- **Points:** 3 **SRS:** LM-001 **Depends on:** LEAD-2, AUTH-7
- **Description:** list(filter/sort/paginate)/get/create/update/delete; RBAC(Sales/Marketing/Admin); audit.
- **AC:** [ ] CRUD + pagination + 422; RBAC enforced.
- **Unit Tests:** [ ] each endpoint; [ ] pagination; [ ] RBAC deny.

### LEAD-4 · Story · Multi-source capture + UTM
- **Points:** 3 **SRS:** LM-001 **Depends on:** LEAD-3
- **Description:** `/leads/capture` from web/email/LinkedIn/referral/manual; store UTM+source; trigger assign+score+dedupe.
- **AC:** [ ] ≥5 source types store UTM; downstream pipeline runs.
- **Unit Tests:** [ ] capture per source; [ ] UTM persisted; [ ] pipeline invoked.

### LEAD-5 · Story · Duplicate detection & merge
- **Points:** 3 **SRS:** LM-003 **Depends on:** LEAD-3
- **Description:** match email/phone/company; `/leads/:id/duplicates`, `/leads/merge` preserving history.
- **AC:** [ ] dupes flagged; merge loses no data.
- **Unit Tests:** [ ] match logic; [ ] merge consolidates activities.

### LEAD-6 · Story · Lead scoring engine
- **Points:** 3 **SRS:** LM-002 **Depends on:** LEAD-3
- **Description:** evaluate configurable rules → score + breakdown; recompute on update/engagement.
- **AC:** [ ] score reflects rules; rule change re-scores.
- **Unit Tests:** [ ] zero rules; [ ] missing fields; [ ] weighting correctness.

### LEAD-7 · Task · Qualification (MQL/SQL/BANT)
- **Points:** 2 **SRS:** §3.1.2 **Depends on:** LEAD-3
- **Description:** `/leads/:id/qualify` status+BANT; valid transitions.
- **AC:** [ ] status/BANT update; invalid transition → 422.
- **Unit Tests:** [ ] transition matrix.

### LEAD-8 · Task · Auto-assignment (territory/round-robin)
- **Points:** 2 **SRS:** LM-001 **Depends on:** LEAD-3
- **Description:** config-driven assignment; round-robin pointer per team.
- **AC:** [ ] new leads get owner per active rule.
- **Unit Tests:** [ ] round-robin fairness; [ ] territory mapping.

### LEAD-9 · Story · One-click conversion (Account+Contact+Opportunity)
- **Points:** 3 **SRS:** §3.1.3 **Depends on:** LEAD-3, CONT-1, ACCT-1, PIPE-1
- **Description:** transactional convert creating 3 records + copying activities; mark converted.
- **AC:** [ ] atomic create of 3 records; history preserved.
- **Unit Tests:** [ ] success path; [ ] rollback on partial failure.

### LEAD-10 · Task · Frontend hooks
- **Points:** 2 **Depends on:** LEAD-3
- **Description:** `useLeads/useLead/useCreateLead/useUpdateLead/useConvertLead/useLeadDuplicates`.
- **AC:** [ ] fetch/mutate + cache invalidation.
- **Unit Tests:** [ ] hook fetch + invalidation (mock client).

### LEAD-11 · Story · UI: Lead list page
- **Points:** 3 **SRS:** LM-001 **Depends on:** LEAD-10
- **Description:** mirror `02-leads.html` (KPIs, filters, status badges, Add Lead → form).
- **AC:** [ ] real data; filters; CTA routes to form.
- **Unit Tests:** [ ] renders rows; [ ] filter interaction; [ ] CTA navigates.

### LEAD-12 · Story · UI: Lead create/edit form
- **Points:** 3 **SRS:** LM-001/2/3 **Depends on:** LEAD-10
- **Description:** mirror `form-01-lead.html` (sections + live score + dup check); Cancel→list.
- **AC:** [ ] create/edit persists; score panel updates; dup warning.
- **Unit Tests:** [ ] validation errors; [ ] submit calls mutation; [ ] dup banner.

### LEAD-13 · Story · UI: Lead Kanban board
- **Points:** 3 **SRS:** §3.1.2 **Depends on:** LEAD-10, LEAD-7
- **Description:** drag-drop qualification stages (grid, no page scroll).
- **AC:** [ ] drag persists stage; reflects server.
- **Unit Tests:** [ ] DnD triggers qualify mutation.

### LEAD-14 · Task · UI: Lead detail + score panel
- **Points:** 2 **Depends on:** LEAD-10
- **Description:** detail view w/ activities, score breakdown, convert button.
- **AC:** [ ] shows breakdown; convert CTA.
- **Unit Tests:** [ ] renders breakdown; [ ] convert calls hook.

### LEAD-15 · Task · Seed/fixtures for lead demos
- **Points:** 1 **Depends on:** LEAD-1
- **Description:** realistic Indian-company seed leads for UI/testing.
- **AC:** [ ] seed runs; varied scores/sources.
- **Unit Tests:** [ ] seed idempotent.

### LEAD-16 · Check · Lead module-wide check
- **Points:** 2 **Depends on:** LEAD-1…15
- **Description:** capture→score→qualify→convert E2E; coverage gate.
- **AC:** [ ] full lifecycle integration test green; ≥80% coverage; LM-001/2/3 satisfied.
- **Unit Tests:** [ ] E2E integration covering capture→convert.
