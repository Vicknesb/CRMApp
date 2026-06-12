# EPIC-DB · Database & Schema (Foundational Data Layer)

> **Epic goal:** Provision the PostgreSQL database and define the **complete Prisma schema — every table for every module** — with relations, indexes, constraints, the initial migration, and seed data. This is the **single source of truth for the data model**.
> **SRS:** §2.3 (PostgreSQL), §3 (all functional modules), §5.4 (scalability/indexing), §8 (data). **Priority:** Must.
> **Depends on:** PLAT-3 (Prisma Client Python + Postgres wiring). **Runs:** immediately after EPIC-PLAT, before EPIC-AUTH and all module epics.
>
> **Note on module schema tickets:** This epic is authoritative for table definitions. The per-module schema
> tickets (`AUTH-1`, `LEAD-1`, `CONT-1`, `ACCT-1`, `PIPE-1`, `ACTV-1`, `TICK-1`, `SLA-1`, `KB-1`, `PROJ-1`,
> `CONTR-1`, `INV-1`, `CAMP-1`, `COMM-1`, `ADMN-1`) are **satisfied here** — tick them complete when their
> tables land in EPIC-DB. Module epics then build the API/UI/logic on top of these tables.

---

### DB-1 · Task · Provision PostgreSQL database, roles & extensions
- **Points:** 2 **SRS:** §2.3 **Depends on:** PLAT-3
- **Description:** Create the app database, an app role with least privilege, and required extensions (`uuid-ossp`/`pgcrypto`, `citext` for emails, `pg_trgm` for fuzzy/KB search). Document connection string in `.env.example`.
- **Acceptance Criteria:**
  - [ ] Database + role created; extensions enabled.
  - [ ] `DATABASE_URL` documented; app connects via Prisma.
- **Unit Tests:** [ ] connection smoke test; [ ] extensions present query.
- **DoD:** Global DoD + AC.

### DB-2 · Task · Prisma schema foundation (datasource, generator, conventions, enums)
- **Points:** 2 **SRS:** §5.6 **Depends on:** DB-1
- **Description:** Establish `schema.prisma`: datasource Postgres, `prisma-client-py` generator, global conventions (`id` UUID pk, `createdAt`/`updatedAt`, soft-delete `deletedAt`), and all shared enums (Role, LeadStatus, LeadSource, DealStage, TicketCategory, TicketPriority, TicketChannel, ProjectStatus, InvoiceStatus, ContractStatus, CampaignType, AccountTier, NotificationType, etc.).
- **Acceptance Criteria:**
  - [ ] Schema compiles (`prisma validate`); enums defined once and reused.
  - [ ] Convention mixin fields present on every model going forward.
- **Unit Tests:** [ ] `prisma validate` passes; [ ] enum values match `@crm/shared`.
- **DoD:** Global DoD + AC.

### DB-3 · Story · Identity & access tables
- **Points:** 3 **SRS:** §2.2, §5.2, AD-001 **Depends on:** DB-2 · **Covers:** AUTH-1, ADMN-1(perm)
- **Description:** `User`, `Role`, `Team`, `Session`, `AuditLog`, `Permission` (role/module/action/fieldRules), `TwoFactorSecret`.
- **Acceptance Criteria:** [ ] tables created; relations User↔Role/Team, AuditLog→User; unique email (citext).
- **Unit Tests:** [ ] create/read User; [ ] unique-email constraint; [ ] cascade on Session delete.
- **DoD:** Global DoD + AC.

### DB-4 · Story · Lead, Contact & Account tables
- **Points:** 5 **SRS:** §3.1, §3.2 **Depends on:** DB-2 · **Covers:** LEAD-1, CONT-1, ACCT-1
- **Description:** `Lead`, `LeadSource`, `LeadScoreRule`; `Contact`, `ContactRole`, `Interaction`, `ContactAccount` (M2M); `Account` (self-relation hierarchy, tier, healthScore).
- **Acceptance Criteria:** [ ] tables + Contact↔Account M2M + Account self-relation; FK Lead→User(owner).
- **Unit Tests:** [ ] M2M attach/detach; [ ] account parent link; [ ] lead FK integrity.
- **DoD:** Global DoD + AC.

### DB-5 · Story · Opportunity & Pipeline tables
- **Points:** 5 **SRS:** §3.3 **Depends on:** DB-4 · **Covers:** PIPE-1
- **Description:** `Pipeline`, `Stage` (order, probability), `Opportunity` (value, closeDate, serviceType, stage/account/contact FKs), `Product` (catalog), `Proposal`, `Quote`, `QuoteLineItem`, `StageHistory`.
- **Acceptance Criteria:** [ ] tables + FKs to Account/Contact/Stage; proposal/quote→opportunity.
- **Unit Tests:** [ ] opportunity FK integrity; [ ] stage-history append; [ ] quote line-item cascade.
- **DoD:** Global DoD + AC.

### DB-6 · Story · Activity & Task tables
- **Points:** 3 **SRS:** §3.4 **Depends on:** DB-4 · **Covers:** ACTV-1
- **Description:** `Activity` (polymorphic relatedTo via type+id), `Task` (due/priority/assignee/status), `Reminder`.
- **Acceptance Criteria:** [ ] tables + assignee FK→User; polymorphic columns indexed.
- **Unit Tests:** [ ] task assignment FK; [ ] activity polymorphic index present.
- **DoD:** Global DoD + AC.

### DB-7 · Story · Ticketing, SLA & Knowledge Base tables
- **Points:** 5 **SRS:** §3.5 **Depends on:** DB-4 · **Covers:** TICK-1, SLA-1, KB-1
- **Description:** `Ticket` (category, priority, status, channel, account/contact/project FKs, assignee), `TicketNote` (visibility); `SLAPolicy` (priority×tier), `SLATracker` (dues, met/breach); `Article`, `KbCategory`, `ArticleRating`.
- **Acceptance Criteria:** [ ] tables + FKs; SLATracker→Ticket 1:1; KB search index (pg_trgm).
- **Unit Tests:** [ ] ticket FK integrity; [ ] SLATracker uniqueness per ticket; [ ] KB trigram index present.
- **DoD:** Global DoD + AC.

### DB-8 · Story · Project & Delivery tables
- **Points:** 3 **SRS:** §3.6 **Depends on:** DB-4 · **Covers:** PROJ-1
- **Description:** `Project` (scope, dates, budget, status, account/deal FKs), `Phase`, `Milestone`, `ProjectTask` (assignee, effort), `Document`.
- **Acceptance Criteria:** [ ] tables + FKs Project→Account/Opportunity; milestone→phase.
- **Unit Tests:** [ ] project FK integrity; [ ] milestone ordering field.
- **DoD:** Global DoD + AC.

### DB-9 · Story · Contract & Invoicing tables
- **Points:** 3 **SRS:** §3.7, §3.8 **Depends on:** DB-4, DB-5 · **Covers:** CONTR-1, INV-1
- **Description:** `Contract` (dates, value, terms, autoRenew, status), `Amendment`, `Signature`; `Invoice` (number, status, currency, totals, dueDate, account/contract/deal FKs), `InvoiceLineItem`, `Payment`.
- **Acceptance Criteria:** [ ] tables + FKs; invoice→contract/deal; line-item & payment cascade.
- **Unit Tests:** [ ] invoice FK integrity; [ ] line-item cascade delete; [ ] contract amendment link.
- **DoD:** Global DoD + AC.

### DB-10 · Story · Campaign & Communication tables
- **Points:** 3 **SRS:** §3.9, §3.10 **Depends on:** DB-4 · **Covers:** CAMP-1, COMM-1
- **Description:** `Campaign`, `AudienceSegment`, `CampaignMetric`, `Event`, `CampaignAttribution` (→Lead/Opportunity); `Notification`, `Mention`, `Comment` (polymorphic), `EmailTemplate`.
- **Acceptance Criteria:** [ ] tables + attribution FKs; comment polymorphic index.
- **Unit Tests:** [ ] campaign metric FK; [ ] attribution mapping; [ ] comment polymorphic index.
- **DoD:** Global DoD + AC.

### DB-11 · Story · Admin/Config, Integration & Data-management tables
- **Points:** 3 **SRS:** AD-002, §6, §8 **Depends on:** DB-3 · **Covers:** ADMN-1, INTG-1, DATA(retention)
- **Description:** `CustomField`, `Layout`, `Workflow`; `IntegrationConnection` (provider, encrypted tokens, status), `WebhookEvent`; `ConsentRecord`, `RecycleBinEntry`/soft-delete metadata, `ArchiveRecord`.
- **Acceptance Criteria:** [ ] tables + encrypted-token columns; consent + recycle-bin tables.
- **Unit Tests:** [ ] custom field def store; [ ] integration token column encrypted; [ ] consent record CRUD.
- **DoD:** Global DoD + AC.

### DB-12 · Story · Cross-module relations, indexes, constraints & cascade rules
- **Points:** 3 **SRS:** §5.1, §5.4 **Depends on:** DB-3…11
- **Description:** Finalize all cross-module FKs, `onDelete` rules (Restrict/Cascade/SetNull as appropriate), composite + partial indexes for hot queries (status, ownerId, dates, polymorphic pairs), and uniqueness constraints (invoice number, etc.).
- **Acceptance Criteria:** [ ] all FKs resolve; indexes on documented hot paths; no orphan-prone cascades.
- **Unit Tests:** [ ] referential-integrity tests across modules; [ ] index existence assertions; [ ] unique constraint violations rejected.
- **DoD:** Global DoD + AC.

### DB-13 · Task · Initial migration (generate + apply)
- **Points:** 2 **SRS:** §2.3 **Depends on:** DB-12
- **Description:** Generate the baseline Prisma migration covering the full schema and apply to dev/test DBs.
- **Acceptance Criteria:** [ ] `prisma migrate dev` creates one coherent baseline migration; applies cleanly on an empty DB.
- **Unit Tests:** [ ] migrate-up on fresh DB succeeds; [ ] `prisma migrate status` clean.
- **DoD:** Global DoD + AC.

### DB-14 · Story · Seed data (reference + demo) for all modules
- **Points:** 3 **SRS:** §2.2 **Depends on:** DB-13
- **Description:** `seed.py` with reference data (roles, SLA policies, pipelines/stages, KB categories) and realistic Indian-company demo data across every module for UI/testing. Idempotent.
- **Acceptance Criteria:** [ ] seed populates all modules; re-running is idempotent.
- **Unit Tests:** [ ] seed creates expected row counts; [ ] idempotency (second run = no dupes).
- **DoD:** Global DoD + AC.

### DB-15 · Task · ERD + data dictionary documentation
- **Points:** 2 **SRS:** §5.6 **Depends on:** DB-12
- **Description:** Generate an ERD (e.g., `prisma-erd` or dbdocs) and a `DATA_DICTIONARY.md` listing every table, column, type, and relation.
- **Acceptance Criteria:** [ ] ERD image + data dictionary committed; reflects current schema.
- **Unit Tests:** [ ] doc-generation script runs; [ ] table count matches schema.
- **DoD:** Global DoD + AC.

### DB-16 · Check · Database module-wide check
- **Points:** 2 **Depends on:** DB-1…15
- **Description:** Verify the full data layer end-to-end.
- **Acceptance Criteria:**
  - [ ] Fresh DB → migrate → seed succeeds top to bottom.
  - [ ] Every module's tables exist with correct relations/indexes/constraints.
  - [ ] Referential-integrity + uniqueness tests green; ≥80% coverage on schema/repository tests.
  - [ ] Module schema tickets (AUTH-1, LEAD-1, CONT-1, ACCT-1, PIPE-1, ACTV-1, TICK-1, SLA-1, KB-1, PROJ-1, CONTR-1, INV-1, CAMP-1, COMM-1, ADMN-1) ticked as covered.
- **Unit Tests:** [ ] full migrate+seed integration test; [ ] cross-module FK integrity suite.
- **DoD:** Global DoD + all DB tickets closed.
