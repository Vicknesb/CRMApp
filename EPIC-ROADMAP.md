# CRM — Epic Roadmap (Build Order)

> Work top to bottom. Run the command in each row to implement that epic, or target a single ticket directly.
> Tick `[x]` when the epic's `*-CHECK` ticket passes (the `epic-implementer` agent marks this automatically).
> Detail per epic: `tickets/epic-*.md` · Per-ticket files: `tickets/<prefix>/<ID>.md` · Tracker: `PROGRESS.md`

**Overall:** `0 / 22` epics complete · `0 / 266` tickets complete

| # | Done | Command | Epic | SRS | Tickets |
|---|------|---------|------|-----|---------|
| 1  | [ ] | `Implement EPIC-PLAT`   | Platform & Infrastructure        | §2.3, §5.6        | PLAT-1…12  |
| 2  | [ ] | `Implement EPIC-DB`     | Database & Schema (all tables)   | §2.3, §3, §8      | DB-1…16    |
| 3  | [ ] | `Implement EPIC-AUTH`   | Authentication & Access          | §5.2, AD-001      | AUTH-1…10  |
| 4  | [ ] | `Implement EPIC-LEAD`   | Lead Management                  | §3.1, LM-001/2/3  | LEAD-1…16  |
| 5  | [ ] | `Implement EPIC-CONT`   | Contact Management               | §3.2.1, CO-001/2  | CONT-1…11  |
| 6  | [ ] | `Implement EPIC-ACCT`   | Account Management               | §3.2.2, AC-001/2  | ACCT-1…12  |
| 7  | [ ] | `Implement EPIC-PIPE`   | Opportunity & Pipeline           | §3.3, PL-001/2/3  | PIPE-1…16  |
| 8  | [ ] | `Implement EPIC-ACTV`   | Activity & Task Management       | §3.4              | ACTV-1…12  |
| 9  | [ ] | `Implement EPIC-TICK`   | Service Ticketing                | §3.5.1, TK-001    | TICK-1…11  |
| 10 | [ ] | `Implement EPIC-SLA`    | SLA Management                   | §3.5.2, TK-002    | SLA-1…11   |
| 11 | [ ] | `Implement EPIC-KB`     | Knowledge Base                   | §3.5.3, TK-003    | KB-1…11    |
| 12 | [ ] | `Implement EPIC-INTG`   | Integration Framework            | §6                | INTG-1…12  |
| 13 | [ ] | `Implement EPIC-PROJ`   | Project & Delivery               | §3.6, PR-001/2    | PROJ-1…15  |
| 14 | [ ] | `Implement EPIC-CONTR`  | Contract & Renewal               | §3.7, CT-001      | CONTR-1…13 |
| 15 | [ ] | `Implement EPIC-INV`    | Invoicing & Revenue              | §3.8, IN-001/2    | INV-1…13   |
| 16 | [ ] | `Implement EPIC-CAMP`   | Marketing & Campaigns            | §3.9, MK-001      | CAMP-1…13  |
| 17 | [ ] | `Implement EPIC-ANLY`   | Analytics & Reporting            | §9, AN-001/2      | ANLY-1…14  |
| 18 | [ ] | `Implement EPIC-COMM`   | Communication & Collaboration    | §3.10             | COMM-1…12  |
| 19 | [ ] | `Implement EPIC-ADMN`   | Admin & Configuration            | AD-001/2, §7.2    | ADMN-1…11  |
| 20 | [ ] | `Implement EPIC-DATA`   | Data Management & Compliance     | §8                | DATA-1…9   |
| 21 | [ ] | `Implement EPIC-NFR`    | Non-Functional & Hardening       | §5, §7.3          | NFR-1…10   |
| 22 | [ ] | `Implement EPIC-VERIFY` | UAT, Go-Live & SRS Verification  | §11               | VERIFY-1…6 |

### ⛔ On-hold (opt-in only)
| # | Done | Command | Epic | Tickets |
|---|------|---------|------|---------|
| — | [ ] | `Implement EPIC-SEED` | Dummy/Demo Data (ON-HOLD) | SEED-1…17 |

---

## Ticket Detail — All Epics

### 1 · EPIC-PLAT · Platform & Infrastructure (0/12)
> `Implement EPIC-PLAT` · SRS §2.3, §5.6 · Depends on: none

| Ticket | Title | Done |
|--------|-------|------|
| PLAT-1  | Monorepo scaffold | [ ] |
| PLAT-2  | FastAPI scaffold (layered) | [ ] |
| PLAT-3  | Prisma Client Python + Postgres wiring | [ ] |
| PLAT-4  | React SPA scaffold (Vite + Tailwind + DaisyUI) | [ ] |
| PLAT-5  | Shared package (types + Zod + enums) | [ ] |
| PLAT-6  | Error handling + structured logging | [ ] |
| PLAT-7  | App shell (Sidebar/Header/PageShell) + UI kit | [ ] |
| PLAT-8  | Testing harness (pytest + vitest + test DB) | [ ] |
| PLAT-9  | Dockerization + docker-compose | [ ] |
| PLAT-10 | OpenAPI docs | [ ] |
| PLAT-11 | CI/CD pipeline | [ ] |
| PLAT-12 | ✔ Check — Platform module-wide | [ ] |

---

### 2 · EPIC-DB · Database & Schema — all tables (0/16)
> `Implement EPIC-DB` · SRS §2.3, §3, §8 · Depends on: EPIC-PLAT

| Ticket | Title | Done |
|--------|-------|------|
| DB-1  | Provision PostgreSQL database, roles & extensions | [ ] |
| DB-2  | Prisma schema foundation (datasource, generator, conventions, enums) | [ ] |
| DB-3  | Identity & access tables | [ ] |
| DB-4  | Lead, Contact & Account tables | [ ] |
| DB-5  | Opportunity & Pipeline tables | [ ] |
| DB-6  | Activity & Task tables | [ ] |
| DB-7  | Ticketing, SLA & Knowledge Base tables | [ ] |
| DB-8  | Project & Delivery tables | [ ] |
| DB-9  | Contract & Invoicing tables | [ ] |
| DB-10 | Campaign & Communication tables | [ ] |
| DB-11 | Admin/Config, Integration & Data-management tables | [ ] |
| DB-12 | Cross-module relations, indexes, constraints & cascade rules | [ ] |
| DB-13 | Initial migration (generate + apply) | [ ] |
| DB-14 | Seed data (reference + demo) for all modules | [ ] |
| DB-15 | ERD + data dictionary documentation → generates `docs/SCHEMA-SUMMARY.md` | [ ] |
| DB-16 | ✔ Check — Database module-wide | [ ] |

---

### 3 · EPIC-AUTH · Authentication & Access (0/10)
> `Implement EPIC-AUTH` · SRS §5.2, AD-001 · Depends on: EPIC-DB

| Ticket | Title | Done |
|--------|-------|------|
| AUTH-1  | Identity schema (User, Role, Team, Session, AuditLog) | [ ] |
| AUTH-2  | Register / Login / Logout / Session API | [ ] |
| AUTH-3  | 2FA (TOTP) enrollment + enforcement | [ ] |
| AUTH-4  | Auth dependencies (require_auth / require_role) | [ ] |
| AUTH-5  | Session timeout + refresh | [ ] |
| AUTH-6  | Password reset + email verification | [ ] |
| AUTH-7  | RBAC policy layer (field + record level) | [ ] |
| AUTH-8  | Audit logging service | [ ] |
| AUTH-9  | SPA auth (login/register/2FA, guard, context) | [ ] |
| AUTH-10 | ✔ Check — Auth module-wide | [ ] |

---

### 4 · EPIC-LEAD · Lead Management (0/16)
> `Implement EPIC-LEAD` · SRS §3.1, LM-001/2/3 · Depends on: EPIC-AUTH

| Ticket | Title | Done |
|--------|-------|------|
| LEAD-1  | Lead schema (Lead, LeadSource, LeadScoreRule) | [ ] |
| LEAD-2  | Lead Pydantic/Zod schemas | [ ] |
| LEAD-3  | Lead CRUD API | [ ] |
| LEAD-4  | Multi-source capture + UTM | [ ] |
| LEAD-5  | Duplicate detection & merge | [ ] |
| LEAD-6  | Lead scoring engine | [ ] |
| LEAD-7  | Qualification (MQL/SQL/BANT) | [ ] |
| LEAD-8  | Auto-assignment (territory/round-robin) | [ ] |
| LEAD-9  | One-click conversion (Account+Contact+Opportunity) | [ ] |
| LEAD-10 | Frontend hooks | [ ] |
| LEAD-11 | UI: Lead list page | [ ] |
| LEAD-12 | UI: Lead create/edit form | [ ] |
| LEAD-13 | UI: Lead Kanban board | [ ] |
| LEAD-14 | UI: Lead detail + score panel | [ ] |
| LEAD-15 | Seed/fixtures for lead demos | [ ] |
| LEAD-16 | ✔ Check — Lead module-wide | [ ] |

---

### 5 · EPIC-CONT · Contact Management (0/11)
> `Implement EPIC-CONT` · SRS §3.2.1, CO-001/2 · Depends on: EPIC-AUTH

| Ticket | Title | Done |
|--------|-------|------|
| CONT-1  | Contact schema (Contact, ContactRole, Interaction) | [ ] |
| CONT-2  | Contact schemas (Pydantic/Zod) | [ ] |
| CONT-3  | Contact CRUD API | [ ] |
| CONT-4  | Multi-account association | [ ] |
| CONT-5  | Interaction/history logging | [ ] |
| CONT-6  | Frontend hooks | [ ] |
| CONT-7  | UI: Contact list + detail panel | [ ] |
| CONT-8  | UI: Contact form | [ ] |
| CONT-9  | UI: Interaction timeline component | [ ] |
| CONT-10 | Seed/fixtures | [ ] |
| CONT-11 | ✔ Check — Contact module-wide | [ ] |

---

### 6 · EPIC-ACCT · Account Management (0/12)
> `Implement EPIC-ACCT` · SRS §3.2.2, AC-001/2 · Depends on: EPIC-AUTH

| Ticket | Title | Done |
|--------|-------|------|
| ACCT-1  | Account schema (+hierarchy, tier, healthScore) | [ ] |
| ACCT-2  | Account schemas (Pydantic/Zod) | [ ] |
| ACCT-3  | Account CRUD API | [ ] |
| ACCT-4  | Tier management | [ ] |
| ACCT-5  | Parent-child hierarchy | [ ] |
| ACCT-6  | Health score calculation | [ ] |
| ACCT-7  | Account 360 aggregation | [ ] |
| ACCT-8  | Frontend hooks | [ ] |
| ACCT-9  | UI: Account list/cards | [ ] |
| ACCT-10 | UI: Account form | [ ] |
| ACCT-11 | UI: Account 360 view | [ ] |
| ACCT-12 | ✔ Check — Account module-wide | [ ] |

---

### 7 · EPIC-PIPE · Opportunity & Pipeline (0/16)
> `Implement EPIC-PIPE` · SRS §3.3, PL-001/2/3 · Depends on: EPIC-AUTH, EPIC-CONT, EPIC-ACCT

| Ticket | Title | Done |
|--------|-------|------|
| PIPE-1  | Pipeline schema (Pipeline, Stage, Opportunity, Proposal, Quote, Product) | [ ] |
| PIPE-2  | Pipeline schemas (Pydantic/Zod) | [ ] |
| PIPE-3  | Deal CRUD API | [ ] |
| PIPE-4  | Color-coding metadata (value/age/priority) | [ ] |
| PIPE-5  | Multiple pipelines + custom stages | [ ] |
| PIPE-6  | Stage move + probability + history | [ ] |
| PIPE-7  | Revenue forecasting (weighted) | [ ] |
| PIPE-8  | Proposal/quote generation + approval workflow | [ ] |
| PIPE-9  | Proposal email send + tracking + versioning | [ ] |
| PIPE-10 | Frontend hooks | [ ] |
| PIPE-11 | UI: Kanban board | [ ] |
| PIPE-12 | UI: Deal list view | [ ] |
| PIPE-13 | UI: Deal form | [ ] |
| PIPE-14 | UI: Deal detail timeline | [ ] |
| PIPE-15 | UI: Proposal builder | [ ] |
| PIPE-16 | ✔ Check — Pipeline module-wide | [ ] |

---

### 8 · EPIC-ACTV · Activity & Task Management (0/12)
> `Implement EPIC-ACTV` · SRS §3.4 · Depends on: EPIC-AUTH

| Ticket | Title | Done |
|--------|-------|------|
| ACTV-1  | Activity/Task schema (Activity, Task, Reminder) | [ ] |
| ACTV-2  | Schemas (Pydantic/Zod) | [ ] |
| ACTV-3  | Activity logging API | [ ] |
| ACTV-4  | Tasks & reminders API | [ ] |
| ACTV-5  | Calendar feed | [ ] |
| ACTV-6  | Overdue alerts + completion tracking | [ ] |
| ACTV-7  | Frontend hooks | [ ] |
| ACTV-8  | UI: Activity feed | [ ] |
| ACTV-9  | UI: Task board | [ ] |
| ACTV-10 | UI: Calendar view | [ ] |
| ACTV-11 | UI: Log Activity & New Task modals | [ ] |
| ACTV-12 | ✔ Check — Activity module-wide | [ ] |

---

### 9 · EPIC-TICK · Service Ticketing (0/11)
> `Implement EPIC-TICK` · SRS §3.5.1, TK-001 · Depends on: EPIC-AUTH, EPIC-ACCT

| Ticket | Title | Done |
|--------|-------|------|
| TICK-1  | Ticket schema (Ticket, Category, Priority, TicketNote) | [ ] |
| TICK-2  | Schemas (Pydantic/Zod) | [ ] |
| TICK-3  | Ticket CRUD API (multi-channel) | [ ] |
| TICK-4  | Categorization, priority, linking | [ ] |
| TICK-5  | Internal/customer notes | [ ] |
| TICK-6  | Frontend hooks | [ ] |
| TICK-7  | UI: Ticket queue | [ ] |
| TICK-8  | UI: Ticket form | [ ] |
| TICK-9  | UI: Ticket detail | [ ] |
| TICK-10 | Seed/fixtures | [ ] |
| TICK-11 | ✔ Check — Ticketing module-wide | [ ] |

---

### 10 · EPIC-SLA · SLA Management (0/11)
> `Implement EPIC-SLA` · SRS §3.5.2, TK-002 · Depends on: EPIC-TICK

| Ticket | Title | Done |
|--------|-------|------|
| SLA-1  | SLA schema (SLAPolicy, SLATracker) | [ ] |
| SLA-2  | Schemas (Pydantic/Zod) | [ ] |
| SLA-3  | SLA policy CRUD API | [ ] |
| SLA-4  | Response/resolution tracking | [ ] |
| SLA-5  | Escalation engine | [ ] |
| SLA-6  | SLA compliance reports | [ ] |
| SLA-7  | Frontend hooks | [ ] |
| SLA-8  | UI: SLA config (admin) | [ ] |
| SLA-9  | UI: SLA countdown in ticket | [ ] |
| SLA-10 | UI: SLA compliance report view | [ ] |
| SLA-11 | ✔ Check — SLA module-wide | [ ] |

---

### 11 · EPIC-KB · Knowledge Base (0/11)
> `Implement EPIC-KB` · SRS §3.5.3, TK-003 · Depends on: EPIC-TICK

| Ticket | Title | Done |
|--------|-------|------|
| KB-1  | KB schema (Article, KbCategory, ArticleRating) | [ ] |
| KB-2  | Schemas (Pydantic/Zod) | [ ] |
| KB-3  | Article CRUD + search API | [ ] |
| KB-4  | Suggestion engine | [ ] |
| KB-5  | Usage + helpfulness tracking | [ ] |
| KB-6  | Frontend hooks | [ ] |
| KB-7  | UI: KB list + category filters | [ ] |
| KB-8  | UI: Article editor | [ ] |
| KB-9  | UI: Article view + rating | [ ] |
| KB-10 | Seed/fixtures | [ ] |
| KB-11 | ✔ Check — KB module-wide | [ ] |

---

### 12 · EPIC-INTG · Integration Framework (0/12)
> `Implement EPIC-INTG` · SRS §6 · Depends on: EPIC-AUTH

| Ticket | Title | Done |
|--------|-------|------|
| INTG-1  | Connector framework (OAuth, token vault, webhooks) | [ ] |
| INTG-2  | Email sync (Gmail/Outlook) — Must | [ ] |
| INTG-3  | Slack/Teams — Must | [ ] |
| INTG-4  | Jira / Azure DevOps — Must | [ ] |
| INTG-5  | Accounting (Zoho/QuickBooks) — Should | [ ] |
| INTG-6  | eSignature (DocuSign/Zoho Sign) — Should | [ ] |
| INTG-7  | Email marketing (Mailchimp/SendGrid) — Nice | [ ] |
| INTG-8  | Calendar sync (Google/Outlook) — Must | [ ] |
| INTG-9  | LinkedIn Sales Navigator — Should | [ ] |
| INTG-10 | Twilio/MSG91 SMS & telephony — Should | [ ] |
| INTG-11 | UI: Integrations settings hub | [ ] |
| INTG-12 | ✔ Check — Integrations module-wide | [ ] |

---

### 13 · EPIC-PROJ · Project & Delivery (0/15)
> `Implement EPIC-PROJ` · SRS §3.6, PR-001/2 · Depends on: EPIC-AUTH, EPIC-ACCT, EPIC-INTG(Jira)

| Ticket | Title | Done |
|--------|-------|------|
| PROJ-1  | Project schema (Project, Phase, Milestone, ProjectTask, Document) | [ ] |
| PROJ-2  | Schemas (Pydantic/Zod) | [ ] |
| PROJ-3  | Project CRUD API | [ ] |
| PROJ-4  | Phases & milestones | [ ] |
| PROJ-5  | Task assignment + effort + status rollup | [ ] |
| PROJ-6  | Project status tracking | [ ] |
| PROJ-7  | Jira bidirectional sync | [ ] |
| PROJ-8  | Document management | [ ] |
| PROJ-9  | Status report generation (PDF) | [ ] |
| PROJ-10 | Frontend hooks | [ ] |
| PROJ-11 | UI: Project list | [ ] |
| PROJ-12 | UI: Project form | [ ] |
| PROJ-13 | UI: Project detail (milestones/tasks/docs) | [ ] |
| PROJ-14 | Seed/fixtures | [ ] |
| PROJ-15 | ✔ Check — Project module-wide | [ ] |

---

### 14 · EPIC-CONTR · Contract & Renewal (0/13)
> `Implement EPIC-CONTR` · SRS §3.7, CT-001 · Depends on: EPIC-ACCT, EPIC-PIPE

| Ticket | Title | Done |
|--------|-------|------|
| CONTR-1  | Contract schema (Contract, Amendment, Signature) | [ ] |
| CONTR-2  | Schemas (Pydantic/Zod) | [ ] |
| CONTR-3  | Contract CRUD API (+auto-renew flag) | [ ] |
| CONTR-4  | Renewal reminders (90/60/30) | [ ] |
| CONTR-5  | Version history + eSignature | [ ] |
| CONTR-6  | Amendments / change orders | [ ] |
| CONTR-7  | Frontend hooks | [ ] |
| CONTR-8  | UI: Contracts table | [ ] |
| CONTR-9  | UI: Contract form | [ ] |
| CONTR-10 | UI: Contract detail + renewal timeline | [ ] |
| CONTR-11 | Seed/fixtures | [ ] |
| CONTR-12 | UI: Renewal pipeline widget | [ ] |
| CONTR-13 | ✔ Check — Contract module-wide | [ ] |

---

### 15 · EPIC-INV · Invoicing & Revenue (0/13)
> `Implement EPIC-INV` · SRS §3.8, IN-001/2 · Depends on: EPIC-CONTR, EPIC-PIPE

| Ticket | Title | Done |
|--------|-------|------|
| INV-1  | Invoice schema (Invoice, LineItem, Payment) | [ ] |
| INV-2  | Schemas (Pydantic/Zod) | [ ] |
| INV-3  | Invoice generation from deals/contracts | [ ] |
| INV-4  | Payment status tracking | [ ] |
| INV-5  | Revenue recognition + multi-currency | [ ] |
| INV-6  | Accounting integration (Zoho/QuickBooks) | [ ] |
| INV-7  | Frontend hooks | [ ] |
| INV-8  | UI: Invoice list | [ ] |
| INV-9  | UI: Invoice form (line items + GST) | [ ] |
| INV-10 | UI: Invoice detail / PDF + record payment | [ ] |
| INV-11 | UI: Invoice aging report | [ ] |
| INV-12 | Seed/fixtures | [ ] |
| INV-13 | ✔ Check — Invoicing module-wide | [ ] |

---

### 16 · EPIC-CAMP · Marketing & Campaigns (0/13)
> `Implement EPIC-CAMP` · SRS §3.9, MK-001 · Depends on: EPIC-LEAD, EPIC-INTG(email)

| Ticket | Title | Done |
|--------|-------|------|
| CAMP-1  | Campaign schema (Campaign, AudienceSegment, CampaignMetric, Event) | [ ] |
| CAMP-2  | Schemas (Pydantic/Zod) | [ ] |
| CAMP-3  | Campaign CRUD + segments API | [ ] |
| CAMP-4  | Performance tracking | [ ] |
| CAMP-5  | Drip email sequences | [ ] |
| CAMP-6  | Event management | [ ] |
| CAMP-7  | ROI attribution | [ ] |
| CAMP-8  | Frontend hooks | [ ] |
| CAMP-9  | UI: Campaign list | [ ] |
| CAMP-10 | UI: Campaign form | [ ] |
| CAMP-11 | UI: Campaign analytics | [ ] |
| CAMP-12 | Seed/fixtures | [ ] |
| CAMP-13 | ✔ Check — Campaign module-wide | [ ] |

---

### 17 · EPIC-ANLY · Analytics & Reporting (0/14)
> `Implement EPIC-ANLY` · SRS §9, AN-001/2 · Depends on: EPIC-PIPE, EPIC-TICK, EPIC-PROJ, EPIC-INV

| Ticket | Title | Done |
|--------|-------|------|
| ANLY-1  | Reporting data model / DB views | [ ] |
| ANLY-2  | Role-based dashboard aggregation API | [ ] |
| ANLY-3  | Pre-built reports (all 10 §9.1) | [ ] |
| ANLY-4  | Custom report builder API | [ ] |
| ANLY-5  | Scheduled report delivery | [ ] |
| ANLY-6  | Export PDF/Excel/CSV | [ ] |
| ANLY-7  | Frontend hooks | [ ] |
| ANLY-8  | UI: Analytics dashboard | [ ] |
| ANLY-9  | UI: Role dashboards (home) | [ ] |
| ANLY-10 | UI: Custom report builder | [ ] |
| ANLY-11 | Report scheduling UI | [ ] |
| ANLY-12 | Drill-down navigation | [ ] |
| ANLY-13 | Performance: cache/materialize heavy reports | [ ] |
| ANLY-14 | ✔ Check — Analytics module-wide | [ ] |

---

### 18 · EPIC-COMM · Communication & Collaboration (0/12)
> `Implement EPIC-COMM` · SRS §3.10 · Depends on: EPIC-AUTH, EPIC-INTG(Slack)

| Ticket | Title | Done |
|--------|-------|------|
| COMM-1  | Schema (Notification, Mention, Comment) | [ ] |
| COMM-2  | Schemas (Pydantic/Zod) | [ ] |
| COMM-3  | Unified communication log | [ ] |
| COMM-4  | In-app notifications + @mention | [ ] |
| COMM-5  | Slack/Teams integration | [ ] |
| COMM-6  | Email templates | [ ] |
| COMM-7  | Comment threads on records | [ ] |
| COMM-8  | Frontend hooks | [ ] |
| COMM-9  | UI: Notification center | [ ] |
| COMM-10 | UI: Comment threads component | [ ] |
| COMM-11 | UI: Email template manager | [ ] |
| COMM-12 | ✔ Check — Comms module-wide | [ ] |

---

### 19 · EPIC-ADMN · Admin & Configuration (0/11)
> `Implement EPIC-ADMN` · SRS AD-001/2, §7.2 · Depends on: EPIC-AUTH

| Ticket | Title | Done |
|--------|-------|------|
| ADMN-1  | Config schema (CustomField, Layout, Workflow, Permission) | [ ] |
| ADMN-2  | RBAC field/record permission management | [ ] |
| ADMN-3  | Custom fields & layouts | [ ] |
| ADMN-4  | Workflow automation engine | [ ] |
| ADMN-5  | Frontend hooks | [ ] |
| ADMN-6  | UI: Admin panel — Users & roles | [ ] |
| ADMN-7  | UI: Admin panel — Permissions & custom fields | [ ] |
| ADMN-8  | UI: Admin panel — Workflows & integrations & audit | [ ] |
| ADMN-9  | UI: Profile & preferences | [ ] |
| ADMN-10 | Seed/fixtures (config samples) | [ ] |
| ADMN-11 | ✔ Check — Admin module-wide | [ ] |

---

### 20 · EPIC-DATA · Data Management & Compliance (0/9)
> `Implement EPIC-DATA` · SRS §8 · Depends on: EPIC-AUTH

| Ticket | Title | Done |
|--------|-------|------|
| DATA-1 | CSV/Excel import engine | [ ] |
| DATA-2 | Legacy API migration (Salesforce/Zoho/HubSpot) | [ ] |
| DATA-3 | UI: Migration wizard | [ ] |
| DATA-4 | Soft-delete + recycle bin (30-day) | [ ] |
| DATA-5 | Archiving (7-year retention, auto-archive >5yr) | [ ] |
| DATA-6 | GDPR/PDPB: data export (portability) | [ ] |
| DATA-7 | GDPR/PDPB: erasure / anonymization | [ ] |
| DATA-8 | Consent management (marketing opt-in) | [ ] |
| DATA-9 | ✔ Check — Data module-wide | [ ] |

---

### 21 · EPIC-NFR · Non-Functional & Hardening (0/10)
> `Implement EPIC-NFR` · SRS §5, §7.3 · Depends on: all feature epics

| Ticket | Title | Done |
|--------|-------|------|
| NFR-1  | Performance (§5.1) | [ ] |
| NFR-2  | Security (§5.2) | [ ] |
| NFR-3  | Reliability & availability (§5.3) | [ ] |
| NFR-4  | Scalability (§5.4) | [ ] |
| NFR-5  | Usability & accessibility (§5.5, §7) | [ ] |
| NFR-6  | Maintainability (§5.6) | [ ] |
| NFR-7  | Mobile responsive pass (§7.3) | [ ] |
| NFR-8  | Browser push notifications (§7.3) | [ ] |
| NFR-9  | Feature flag system | [ ] |
| NFR-10 | ✔ Check — NFR module-wide | [ ] |

---

### 22 · EPIC-VERIFY · UAT, Go-Live & SRS Verification (0/6)
> `Implement EPIC-VERIFY` · SRS §11 · Depends on: all epics

| Ticket | Title | Done |
|--------|-------|------|
| VERIFY-1 | ✔ SRS coverage matrix (100% Req IDs) | [ ] |
| VERIFY-2 | ✔ Full regression + coverage gate | [ ] |
| VERIFY-3 | ✔ Performance acceptance (§11.2) | [ ] |
| VERIFY-4 | ✔ Security acceptance (§11.3) | [ ] |
| VERIFY-5 | UAT sign-off + documentation (§11.4) | [ ] |
| VERIFY-6 | ✔ Go-Live readiness | [ ] |

---

### ⛔ EPIC-SEED · Dummy/Demo Data — ON HOLD (0/17)
> `Implement EPIC-SEED` · **Only when explicitly requested** · Never run in normal build flow

| Ticket | Title | Done |
|--------|-------|------|
| SEED-1  | Dummy-data framework & runner | [ ] |
| SEED-2  | Users & roles dummy data | [ ] |
| SEED-3  | Leads dummy data | [ ] |
| SEED-4  | Contacts dummy data | [ ] |
| SEED-5  | Accounts dummy data | [ ] |
| SEED-6  | Opportunities/Pipeline dummy data | [ ] |
| SEED-7  | Activities & tasks dummy data | [ ] |
| SEED-8  | Tickets dummy data | [ ] |
| SEED-9  | SLA policies dummy data | [ ] |
| SEED-10 | Knowledge Base dummy data | [ ] |
| SEED-11 | Projects dummy data | [ ] |
| SEED-12 | Contracts dummy data | [ ] |
| SEED-13 | Invoices dummy data | [ ] |
| SEED-14 | Campaigns dummy data | [ ] |
| SEED-15 | Communication & notifications dummy data | [ ] |
| SEED-16 | Admin/config dummy data | [ ] |
| SEED-17 | ✔ Check — Dummy-data module-wide | [ ] |

---

## Notes
- **Dependency-safe order:** PLAT → DB → AUTH must come first; the rest build on them.
- **EPIC-DB** creates every module's tables up front — each module's schema ticket is already satisfied when you reach it.
- **Single ticket:** `Implement PLAT-1` or `Implement LEAD-6` — agent auto-detects, checks deps, implements, commits.
- **After each epic:** check `reports/<EPIC-KEY>-completion-report.md` and `PROGRESS.md`, then start the next row.
- **After EPIC-DB:** `docs/SCHEMA-SUMMARY.md` is generated (DB-15) — agents load it instead of full schema.prisma.
- Update the **Overall** counts above as epics complete (the agent does this automatically).
