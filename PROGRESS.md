# CRM — Master Progress Checklist

> Single source of truth for completion. Tick `[x]` when a ticket's Acceptance Criteria + Unit Tests pass and it's committed.
> **266 tickets · 22 epics** in the main flow, **+1 on-hold epic (EPIC-SEED, 17 tickets)**. Tick the epic box only after its `*-CHECK` ticket passes. Finish with EPIC-VERIFY.
>
> Backlog detail: `tickets/epic-*.md` · Playbook: `HOW-TO-IMPLEMENT.md` · Agent: `.claude/agents/epic-implementer.md`

**Overall:** `193 / 266` tickets · `3 / 22` epics complete.

---

## ☑ EPIC-PLAT · Platform & Infrastructure (12/12)
- [x] PLAT-1 · Monorepo scaffold
- [x] PLAT-2 · FastAPI scaffold (layered)
- [x] PLAT-3 · Prisma Client Python + Postgres wiring
- [x] PLAT-4 · React SPA scaffold (Vite + Tailwind + DaisyUI)
- [x] PLAT-5 · Shared package (types + Zod + enums)
- [x] PLAT-6 · Error handling + structured logging
- [x] PLAT-7 · App shell (Sidebar/Header/PageShell) + UI kit
- [x] PLAT-8 · Testing harness (pytest + vitest + test DB)
- [x] PLAT-9 · Dockerization + docker-compose
- [x] PLAT-10 · OpenAPI docs
- [x] PLAT-11 · CI/CD pipeline
- [x] PLAT-12 · ✔ Check — Platform module-wide

## ☑ EPIC-DB · Database & Schema (all modules) (16/16)
- [x] DB-1 · Provision PostgreSQL database, roles & extensions
- [x] DB-2 · Prisma schema foundation (datasource, generator, conventions, enums)
- [x] DB-3 · Identity & access tables
- [x] DB-4 · Lead, Contact & Account tables
- [x] DB-5 · Opportunity & Pipeline tables
- [x] DB-6 · Activity & Task tables
- [x] DB-7 · Ticketing, SLA & Knowledge Base tables
- [x] DB-8 · Project & Delivery tables
- [x] DB-9 · Contract & Invoicing tables
- [x] DB-10 · Campaign & Communication tables
- [x] DB-11 · Admin/Config, Integration & Data-management tables
- [x] DB-12 · Cross-module relations, indexes, constraints & cascade rules
- [x] DB-13 · Initial migration (generate + apply)
- [x] DB-14 · Seed data (reference + demo) for all modules
- [x] DB-15 · ERD + data dictionary documentation
- [x] DB-16 · ✔ Check — Database module-wide

## ☑ EPIC-AUTH · Authentication & Access (10/10)
- [x] AUTH-1 · Identity schema (User, Role, Team, Session, AuditLog)
- [x] AUTH-2 · Register/Login/Logout/Session API
- [x] AUTH-3 · 2FA (TOTP) enrollment + enforcement
- [x] AUTH-4 · Auth dependencies (require_auth/require_role)
- [x] AUTH-5 · Session timeout + refresh
- [x] AUTH-6 · Password reset + email verification
- [x] AUTH-7 · RBAC policy layer (field + record level)
- [x] AUTH-8 · Audit logging service
- [x] AUTH-9 · SPA auth (login/register/2FA, guard, context)
- [x] AUTH-10 · ✔ Check — Auth module-wide

## ☐ EPIC-LEAD · Lead Management (13/16)
- [x] LEAD-1 · Lead schema (Lead, LeadSource, LeadScoreRule)
- [x] LEAD-2 · Lead Pydantic/Zod schemas
- [x] LEAD-3 · Lead CRUD API
- [x] LEAD-4 · Multi-source capture + UTM
- [x] LEAD-5 · Duplicate detection & merge
- [x] LEAD-6 · Lead scoring engine
- [x] LEAD-7 · Qualification (MQL/SQL/BANT)
- [x] LEAD-8 · Auto-assignment (territory/round-robin)
- [x] LEAD-9 · One-click conversion (Account+Contact+Opportunity)
- [x] LEAD-10 · Frontend hooks
- [x] LEAD-11 · UI: Lead list page
- [x] LEAD-12 · UI: Lead create/edit form
- [ ] LEAD-13 · UI: Lead Kanban board
- [ ] LEAD-14 · UI: Lead detail + score panel
- [ ] LEAD-15 · Seed/fixtures
- [ ] LEAD-16 · ✔ Check — Lead module-wide

## ☐ EPIC-CONT · Contact Management (8/11)
- [x] CONT-1 · Contact schema (Contact, ContactRole, Interaction)
- [x] CONT-2 · Schemas (Pydantic/Zod)
- [x] CONT-3 · Contact CRUD API
- [x] CONT-4 · Multi-account association
- [x] CONT-5 · Interaction/history logging
- [x] CONT-6 · Frontend hooks
- [x] CONT-7 · UI: Contact list + detail panel
- [x] CONT-8 · UI: Contact form
- [ ] CONT-9 · UI: Interaction timeline component
- [ ] CONT-10 · Seed/fixtures
- [ ] CONT-11 · ✔ Check — Contact module-wide

## ☐ EPIC-ACCT · Account Management (9/12)
- [x] ACCT-1 · Account schema (+hierarchy, tier, healthScore)
- [x] ACCT-2 · Schemas (Pydantic/Zod)
- [x] ACCT-3 · Account CRUD API
- [x] ACCT-4 · Tier management
- [x] ACCT-5 · Parent-child hierarchy
- [x] ACCT-6 · Health score calculation
- [x] ACCT-7 · Account 360 aggregation
- [x] ACCT-8 · Frontend hooks
- [x] ACCT-9 · UI: Account list/cards
- [x] ACCT-10 · UI: Account form
- [ ] ACCT-11 · UI: Account 360 view
- [ ] ACCT-12 · ✔ Check — Account module-wide

## ☐ EPIC-PIPE · Opportunity & Sales Pipeline (10/16)
- [x] PIPE-1 · Pipeline schema (Pipeline, Stage, Opportunity, Proposal, Quote, Product)
- [x] PIPE-2 · Schemas (Pydantic/Zod)
- [x] PIPE-3 · Deal CRUD API
- [x] PIPE-4 · Color-coding metadata (value/age/priority)
- [x] PIPE-5 · Multiple pipelines + custom stages
- [x] PIPE-6 · Stage move + probability + history
- [x] PIPE-7 · Revenue forecasting (weighted)
- [ ] PIPE-8 · Proposal/quote generation + approval workflow
- [ ] PIPE-9 · Proposal email send + tracking + versioning
- [x] PIPE-10 · Frontend hooks
- [ ] PIPE-11 · UI: Kanban board
- [x] PIPE-12 · UI: Deal list view
- [x] PIPE-13 · UI: Deal form
- [ ] PIPE-14 · UI: Deal detail timeline
- [ ] PIPE-15 · UI: Proposal builder
- [ ] PIPE-16 · ✔ Check — Pipeline module-wide

## ☐ EPIC-ACTV · Activity & Task Management (8/12)
- [x] ACTV-1 · Activity/Task schema (Activity, Task, Reminder)
- [x] ACTV-2 · Schemas (Pydantic/Zod)
- [x] ACTV-3 · Activity logging API
- [x] ACTV-4 · Tasks & reminders API
- [ ] ACTV-5 · Calendar feed
- [x] ACTV-6 · Overdue alerts + completion tracking
- [x] ACTV-7 · Frontend hooks
- [ ] ACTV-8 · UI: Activity feed
- [x] ACTV-9 · UI: Task board
- [ ] ACTV-10 · UI: Calendar view
- [ ] ACTV-11 · UI: Log Activity & New Task modals
- [ ] ACTV-12 · ✔ Check — Activity module-wide

## ☐ EPIC-TICK · Service Ticketing (9/11)
- [x] TICK-1 · Ticket schema (Ticket, Category, Priority, TicketNote)
- [x] TICK-2 · Schemas (Pydantic/Zod)
- [x] TICK-3 · Ticket CRUD API (multi-channel)
- [x] TICK-4 · Categorization, priority, linking
- [x] TICK-5 · Internal/customer notes
- [x] TICK-6 · Frontend hooks
- [x] TICK-7 · UI: Ticket queue
- [x] TICK-8 · UI: Ticket form
- [ ] TICK-9 · UI: Ticket detail
- [ ] TICK-10 · Seed/fixtures
- [ ] TICK-11 · ✔ Check — Ticketing module-wide

## ☐ EPIC-SLA · SLA Management (9/11)
- [x] SLA-1 · SLA schema (SLAPolicy, SLATracker)
- [x] SLA-2 · Schemas (Pydantic/Zod)
- [x] SLA-3 · SLA policy CRUD API
- [x] SLA-4 · Response/resolution tracking
- [x] SLA-5 · Escalation engine
- [x] SLA-6 · SLA compliance reports
- [x] SLA-7 · Frontend hooks
- [x] SLA-8 · UI: SLA config (admin)
- [x] SLA-9 · UI: SLA countdown in ticket
- [ ] SLA-10 · UI: SLA compliance report view
- [ ] SLA-11 · ✔ Check — SLA module-wide

## ☐ EPIC-KB · Knowledge Base (9/11)
- [x] KB-1 · KB schema (Article, KbCategory, ArticleRating)
- [x] KB-2 · Schemas (Pydantic/Zod)
- [x] KB-3 · Article CRUD + search API
- [x] KB-4 · Suggestion engine
- [x] KB-5 · Usage + helpfulness tracking
- [x] KB-6 · Frontend hooks
- [x] KB-7 · UI: KB list + category filters
- [x] KB-8 · UI: Article editor
- [x] KB-9 · UI: Article view + rating
- [x] KB-10 · Seed/fixtures
- [ ] KB-11 · ✔ Check — KB module-wide

## ☐ EPIC-PROJ · Project & Delivery (14/15)
- [x] PROJ-1 · Project schema (Project, Phase, Milestone, ProjectTask, Document)
- [x] PROJ-2 · Schemas (Pydantic/Zod)
- [x] PROJ-3 · Project CRUD API
- [x] PROJ-4 · Phases & milestones
- [x] PROJ-5 · Task assignment + effort + status rollup
- [x] PROJ-6 · Project status tracking
- [x] PROJ-7 · Jira bidirectional sync
- [x] PROJ-8 · Document management
- [x] PROJ-9 · Status report generation (PDF)
- [x] PROJ-10 · Frontend hooks
- [x] PROJ-11 · UI: Project list
- [x] PROJ-12 · UI: Project form
- [x] PROJ-13 · UI: Project detail (milestones/tasks/docs)
- [x] PROJ-14 · Seed/fixtures
- [ ] PROJ-15 · ✔ Check — Project module-wide

## ☐ EPIC-CONTR · Contract & Renewal (12/13)
- [x] CONTR-1 · Contract schema (Contract, Amendment, Signature)
- [x] CONTR-2 · Schemas (Pydantic/Zod)
- [x] CONTR-3 · Contract CRUD API (+auto-renew flag)
- [x] CONTR-4 · Renewal reminders (90/60/30)
- [x] CONTR-5 · Version history + eSignature
- [x] CONTR-6 · Amendments / change orders
- [x] CONTR-7 · Frontend hooks
- [x] CONTR-8 · UI: Contracts table
- [x] CONTR-9 · UI: Contract form
- [x] CONTR-10 · UI: Contract detail + renewal timeline
- [x] CONTR-11 · Seed/fixtures
- [x] CONTR-12 · UI: Renewal pipeline widget
- [ ] CONTR-13 · ✔ Check — Contract module-wide

## ☐ EPIC-INV · Invoicing & Revenue (12/13)
- [x] INV-1 · Invoice schema (Invoice, LineItem, Payment)
- [x] INV-2 · Schemas (Pydantic/Zod)
- [x] INV-3 · Invoice generation from deals/contracts
- [x] INV-4 · Payment status tracking
- [x] INV-5 · Revenue recognition + multi-currency
- [x] INV-6 · Accounting integration (Zoho/QuickBooks)
- [x] INV-7 · Frontend hooks
- [x] INV-8 · UI: Invoice list
- [x] INV-9 · UI: Invoice form (line items + GST)
- [x] INV-10 · UI: Invoice detail / PDF + record payment
- [x] INV-11 · UI: Invoice aging report
- [x] INV-12 · Seed/fixtures
- [ ] INV-13 · ✔ Check — Invoicing module-wide

## ☐ EPIC-CAMP · Marketing & Campaigns (12/13)
- [x] CAMP-1 · Campaign schema (Campaign, AudienceSegment, CampaignMetric, Event)
- [x] CAMP-2 · Schemas (Pydantic/Zod)
- [x] CAMP-3 · Campaign CRUD + segments API
- [x] CAMP-4 · Performance tracking
- [x] CAMP-5 · Drip email sequences
- [x] CAMP-6 · Event management
- [x] CAMP-7 · ROI attribution
- [x] CAMP-8 · Frontend hooks
- [x] CAMP-9 · UI: Campaign list
- [x] CAMP-10 · UI: Campaign form
- [x] CAMP-11 · UI: Campaign analytics
- [x] CAMP-12 · Seed/fixtures
- [ ] CAMP-13 · ✔ Check — Campaign module-wide

## ☐ EPIC-ANLY · Analytics & Reporting (13/14)
- [x] ANLY-1 · Reporting data model / DB views
- [x] ANLY-2 · Role-based dashboard aggregation API
- [x] ANLY-3 · Pre-built reports (all 10 §9.1)
- [x] ANLY-4 · Custom report builder API
- [x] ANLY-5 · Scheduled report delivery
- [x] ANLY-6 · Export PDF/Excel/CSV
- [x] ANLY-7 · Frontend hooks
- [x] ANLY-8 · UI: Analytics dashboard
- [x] ANLY-9 · UI: Role dashboards (home)
- [x] ANLY-10 · UI: Custom report builder
- [x] ANLY-11 · Report scheduling UI
- [x] ANLY-12 · Drill-down navigation
- [x] ANLY-13 · Performance: cache/materialize heavy reports
- [ ] ANLY-14 · ✔ Check — Analytics module-wide

## ☐ EPIC-COMM · Communication & Collaboration (11/12)
- [x] COMM-1 · Schema (Notification, Mention, Comment)
- [x] COMM-2 · Schemas (Pydantic/Zod)
- [x] COMM-3 · Unified communication log
- [x] COMM-4 · In-app notifications + @mention
- [x] COMM-5 · Slack/Teams integration
- [x] COMM-6 · Email templates
- [x] COMM-7 · Comment threads on records
- [x] COMM-8 · Frontend hooks
- [x] COMM-9 · UI: Notification center
- [x] COMM-10 · UI: Comment threads component
- [x] COMM-11 · UI: Email template manager
- [ ] COMM-12 · ✔ Check — Comms module-wide

## ☐ EPIC-ADMN · Admin & Configuration (0/11)
- [x] ADMN-1 · Config schema (CustomField, Layout, Workflow, Permission)
- [ ] ADMN-2 · RBAC field/record permission management
- [ ] ADMN-3 · Custom fields & layouts
- [ ] ADMN-4 · Workflow automation engine
- [ ] ADMN-5 · Frontend hooks
- [ ] ADMN-6 · UI: Admin panel — Users & roles
- [ ] ADMN-7 · UI: Admin panel — Permissions & custom fields
- [ ] ADMN-8 · UI: Admin panel — Workflows & integrations & audit
- [ ] ADMN-9 · UI: Profile & preferences
- [ ] ADMN-10 · Seed/fixtures (config samples)
- [ ] ADMN-11 · ✔ Check — Admin module-wide

## ☐ EPIC-INTG · Integration Framework (10/12)
- [x] INTG-1 · Connector framework (OAuth, token vault, webhooks)
- [x] INTG-2 · Email sync (Gmail/Outlook) — Must
- [x] INTG-3 · Slack/Teams — Must
- [x] INTG-4 · Jira / Azure DevOps — Must
- [x] INTG-5 · Accounting (Zoho/QuickBooks) — Should
- [x] INTG-6 · eSignature (DocuSign/Zoho Sign) — Should
- [x] INTG-7 · Email marketing (Mailchimp/SendGrid) — Nice
- [x] INTG-8 · Calendar sync (Google/Outlook) — Must
- [x] INTG-9 · LinkedIn Sales Navigator — Should
- [x] INTG-10 · Twilio/MSG91 SMS & telephony — Should
- [x] INTG-11 · UI: Integrations settings hub
- [ ] INTG-12 · ✔ Check — Integrations module-wide

## ☐ EPIC-DATA · Data Management & Compliance (0/9)
- [ ] DATA-1 · CSV/Excel import engine
- [ ] DATA-2 · Legacy API migration (Salesforce/Zoho/HubSpot)
- [ ] DATA-3 · UI: Migration wizard
- [ ] DATA-4 · Soft-delete + recycle bin (30-day)
- [ ] DATA-5 · Archiving (7-year retention, auto-archive >5yr)
- [ ] DATA-6 · GDPR/PDPB: data export (portability)
- [ ] DATA-7 · GDPR/PDPB: erasure / anonymization
- [ ] DATA-8 · Consent management (marketing opt-in)
- [ ] DATA-9 · ✔ Check — Data module-wide

## ☐ EPIC-NFR · Non-Functional & Hardening (0/10)
- [ ] NFR-1 · Performance (§5.1)
- [ ] NFR-2 · Security (§5.2)
- [ ] NFR-3 · Reliability & availability (§5.3)
- [ ] NFR-4 · Scalability (§5.4)
- [ ] NFR-5 · Usability & accessibility (§5.5, §7)
- [ ] NFR-6 · Maintainability (§5.6)
- [ ] NFR-7 · Mobile responsive pass (§7.3)
- [ ] NFR-8 · Browser push notifications (§7.3)
- [ ] NFR-9 · Feature flag system
- [ ] NFR-10 · ✔ Check — NFR module-wide

## ☐ EPIC-VERIFY · UAT, Go-Live & SRS Verification (0/6)
- [ ] VERIFY-1 · ✔ SRS coverage matrix (100% Req IDs)
- [ ] VERIFY-2 · ✔ Full regression + coverage gate
- [ ] VERIFY-3 · ✔ Performance acceptance (§11.2)
- [ ] VERIFY-4 · ✔ Security acceptance (§11.3)
- [ ] VERIFY-5 · UAT sign-off + documentation (§11.4)
- [ ] VERIFY-6 · ✔ Go-Live readiness

---

## ⛔ EPIC-SEED · Dummy/Demo Data — ON HOLD (opt-in, 0/17)
> Skipped in the normal build flow. Implement only when explicitly requested. Tickets: SEED-1…17 (see `tickets/epic-seed.md`).
- [ ] SEED-1 · Dummy-data framework & runner
- [ ] SEED-2 · Users & roles dummy data
- [ ] SEED-3 · Leads dummy data
- [ ] SEED-4 · Contacts dummy data
- [ ] SEED-5 · Accounts dummy data
- [ ] SEED-6 · Opportunities/Pipeline dummy data
- [ ] SEED-7 · Activities & tasks dummy data
- [ ] SEED-8 · Tickets dummy data
- [ ] SEED-9 · SLA policies dummy data
- [ ] SEED-10 · Knowledge Base dummy data
- [ ] SEED-11 · Projects dummy data
- [ ] SEED-12 · Contracts dummy data
- [ ] SEED-13 · Invoices dummy data
- [ ] SEED-14 · Campaigns dummy data
- [ ] SEED-15 · Communication & notifications dummy data
- [ ] SEED-16 · Admin/config dummy data
- [ ] SEED-17 · ✔ Check — Dummy-data module-wide

## How to use
- Tick a ticket `[ ]→[x]` the moment its Acceptance Criteria + Unit Tests pass and it's committed.
- Update the epic's `(0/N)` count and flip its `☐→☑` heading once the `*-CHECK` passes.
- Update the **Overall** line at the top as you go.
- The `epic-implementer` agent updates the per-epic ticket boxes in `tickets/epic-*.md`; mirror those ticks here (or ask it to update this file too).
