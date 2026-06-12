# EPIC-SEED · Dummy / Demo Data Loading (ON-HOLD · opt-in)

> ⛔ **STATUS: ON HOLD — do NOT implement unless explicitly instructed.** When working through the backlog
> (manually or via the `epic-implementer` agent), **skip this epic and move to the next** unless the user
> says specifically "implement EPIC-SEED" (or names a SEED ticket).
>
> **Epic goal:** Load a small set of realistic dummy records into **each module's tables** so every screen has
> data to render during development/demos. One ticket per module.
> **SRS:** §2.2 (roles/personas), §7 (UI needs data). **Priority:** Optional (dev/demo convenience).
> **Depends on:** EPIC-DB tables exist (per-ticket dependency on the matching `DB-*`). Reuses the seed
> framework from `DB-14`. Indian-company flavour (Infosys, Wipro, HCL, TCS, Tech Mahindra, etc.), ₹/L/Cr.

---

### SEED-1 · Task · Dummy-data framework & runner
- **Points:** 2 **Depends on:** DB-13
- **Description:** Idempotent loader (`seed_dummy.py`) with a Faker (en_IN locale) helper, deterministic seed,
  per-module toggles, and a single `--module <name>|all` entry point. Safe to re-run (upsert by natural key).
- **Acceptance Criteria:** [ ] runner loads/clears per module; re-run produces no duplicates.
- **Unit Tests:** [ ] idempotency (second run = same row counts); [ ] `--module` selector works.
- **DoD:** Global DoD + AC.

### SEED-2 · Task · Users & roles dummy data
- **Points:** 1 **Depends on:** DB-3, SEED-1
- **Description:** ~8–10 users across all roles (Sales Exec, Account Mgr, Support Eng, PM, Finance, Marketing, Admin, Management).
- **AC:** [ ] one+ user per role; passwords hashed. **Unit Tests:** [ ] row count ≥ roles; [ ] idempotent.

### SEED-3 · Task · Leads dummy data
- **Points:** 1 **Depends on:** DB-4, SEED-1
- **Description:** ~30 leads across sources/statuses (New/MQL/SQL/Unqualified) with scores + UTM.
- **AC:** [ ] varied status/source; owners assigned. **Unit Tests:** [ ] count; [ ] all statuses present; [ ] idempotent.

### SEED-4 · Task · Contacts dummy data
- **Points:** 1 **Depends on:** DB-4, SEED-1
- **Description:** ~40 contacts with role tags, linked to accounts (M2M), some with interactions.
- **AC:** [ ] contacts linked to accounts; role tags set. **Unit Tests:** [ ] count; [ ] M2M links exist; [ ] idempotent.

### SEED-5 · Task · Accounts dummy data
- **Points:** 1 **Depends on:** DB-4, SEED-1
- **Description:** ~15 accounts across tiers (Strategic/Enterprise/Mid-Market/SMB), some parent-child, health scores.
- **AC:** [ ] tiers represented; ≥1 hierarchy. **Unit Tests:** [ ] count; [ ] hierarchy present; [ ] idempotent.

### SEED-6 · Task · Opportunities/Pipeline dummy data
- **Points:** 1 **Depends on:** DB-5, SEED-5
- **Description:** ~22 opportunities across stages + pipelines, with a few proposals/quotes.
- **AC:** [ ] all stages populated; values in ₹L/Cr. **Unit Tests:** [ ] count; [ ] every stage has ≥1 deal; [ ] idempotent.

### SEED-7 · Task · Activities & tasks dummy data
- **Points:** 1 **Depends on:** DB-6, SEED-4
- **Description:** ~50 activities (calls/emails/meetings) + tasks (some overdue, some upcoming) against contacts/accounts/deals.
- **AC:** [ ] mix of types; ≥1 overdue task. **Unit Tests:** [ ] count; [ ] overdue present; [ ] idempotent.

### SEED-8 · Task · Tickets dummy data
- **Points:** 1 **Depends on:** DB-7, SEED-5
- **Description:** ~25 tickets across categories/priorities/channels, with internal + customer notes.
- **AC:** [ ] all priorities/channels present. **Unit Tests:** [ ] count; [ ] P1–P4 present; [ ] idempotent.

### SEED-9 · Task · SLA policies dummy data
- **Points:** 1 **Depends on:** DB-7, SEED-1
- **Description:** SLA policy matrix per priority × client tier; trackers for existing tickets.
- **AC:** [ ] policy per priority×tier. **Unit Tests:** [ ] matrix complete; [ ] idempotent.

### SEED-10 · Task · Knowledge Base dummy data
- **Points:** 1 **Depends on:** DB-7, SEED-1
- **Description:** ~20 KB articles across categories with view counts + helpful ratings.
- **AC:** [ ] categories populated; ratings present. **Unit Tests:** [ ] count; [ ] idempotent.

### SEED-11 · Task · Projects dummy data
- **Points:** 1 **Depends on:** DB-8, SEED-5
- **Description:** ~10 projects with phases, milestones, tasks, statuses (incl. On Hold/Delayed), documents.
- **AC:** [ ] milestones + statuses varied. **Unit Tests:** [ ] count; [ ] statuses present; [ ] idempotent.

### SEED-12 · Task · Contracts dummy data
- **Points:** 1 **Depends on:** DB-9, SEED-5
- **Description:** ~12 contracts incl. some expiring in 30/60/90 days; amendments; signatures.
- **AC:** [ ] near-expiry samples present. **Unit Tests:** [ ] count; [ ] expiry buckets present; [ ] idempotent.

### SEED-13 · Task · Invoices dummy data
- **Points:** 1 **Depends on:** DB-9, SEED-6
- **Description:** ~20 invoices across statuses (Draft/Sent/Paid/Overdue/Cancelled) with line items + GST + payments.
- **AC:** [ ] all statuses; totals computed. **Unit Tests:** [ ] count; [ ] statuses present; [ ] idempotent.

### SEED-14 · Task · Campaigns dummy data
- **Points:** 1 **Depends on:** DB-10, SEED-3
- **Description:** ~8 campaigns with segments, metrics (opens/clicks/conversions), events, attribution to deals.
- **AC:** [ ] metrics + attribution present. **Unit Tests:** [ ] count; [ ] metrics non-empty; [ ] idempotent.

### SEED-15 · Task · Communication & notifications dummy data
- **Points:** 1 **Depends on:** DB-10, SEED-2
- **Description:** Notifications, @mentions, comment threads on records, email templates.
- **AC:** [ ] notifications + comments present. **Unit Tests:** [ ] count; [ ] idempotent.

### SEED-16 · Task · Admin/config dummy data
- **Points:** 1 **Depends on:** DB-11, SEED-2
- **Description:** Sample custom fields, layouts, workflows, permission rules, an integration connection (mock).
- **AC:** [ ] config samples present. **Unit Tests:** [ ] count; [ ] idempotent.

### SEED-17 · Check · Dummy-data module-wide check
- **Points:** 2 **Depends on:** SEED-1…16
- **Description:** Verify a full dummy load across all modules.
- **Acceptance Criteria:**
  - [ ] `seed_dummy.py --module all` populates every module on a migrated DB.
  - [ ] Re-running is idempotent (no duplicates); all key screens have data.
- **Unit Tests:** [ ] integration: migrate → dummy-load → expected counts per module; [ ] idempotency.
- **DoD:** Global DoD + all SEED tickets closed.
