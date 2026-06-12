# CRM — JIRA Backlog (Epics → Stories → Tickets)

> **Source of truth:** `CRM_Requirements_Specification.docx` (SRS v1.0).
> **Workflow:** Pick one ticket → implement → run its **Unit Tests** → meet **Definition of Done** → commit. After all tickets in an epic pass, run that epic's **`*-CHECK`** ticket (module-wise integration + coverage). Finish with **EPIC-VERIFY**.

---

## 1. Stack (applies to every ticket)

| Layer | Technology |
|-------|-----------|
| Frontend | **React 18 SPA** (Vite + TypeScript), React Router, TanStack Query, Tailwind + **DaisyUI (lemonade)**, react-hook-form + Zod, Recharts |
| Backend | **Python + FastAPI** (async REST), layered: `router → service → repository` |
| ORM / DB | **Prisma Client Python** (`prisma-client-py`) + **PostgreSQL** |
| Validation | **Pydantic** models (request/response) at the API edge |
| Auth | JWT in httpOnly cookies, **2FA (TOTP)**, RBAC dependency injection |
| Testing | **pytest** + httpx/ASGI (API), **Vitest + RTL** (web), test PostgreSQL DB |
| Infra | Docker + docker-compose, GitHub Actions CI/CD, FastAPI OpenAPI (`/docs`), structlog |

### Repo layout
```
crm/
├── apps/
│   ├── api/                       # FastAPI service
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── core/              # config, security, logging
│   │   │   ├── db/                # prisma client wrapper
│   │   │   ├── middleware/
│   │   │   └── modules/<mod>/     # router.py, service.py, schemas.py, repository.py
│   │   ├── prisma/                # schema.prisma, migrations/, seed.py
│   │   └── tests/                 # pytest (unit + integration)
│   └── web/                       # React SPA
│       └── src/features/<mod>/    # pages, components, hooks, api
├── packages/shared/               # TS types + Zod (web); enums mirrored to py
├── docker-compose.yml
└── .github/workflows/ci.yml
```

---

## 2. Conventions (every ticket's "Style")

- **Python:** snake_case modules, type hints everywhere, async services, Pydantic for I/O, no bare `except`.
- **API envelope:** `{ "data": ..., "error": ..., "meta": ... }`. Status codes semantic (201/422/401/403/404).
- **Frontend:** kebab-case files, PascalCase components (named exports), `useXxx` hooks, Zod schemas suffixed `Schema`, Tailwind+DaisyUI lemonade, brand `#507d2a`, `cn()` for conditional classes.
- **Validate every request** with Pydantic before touching Prisma.
- **Coverage ≥90%** on services/routers/features. No snapshot tests.

---

## 3. JIRA Ticket Format (used in every epic file)

```
### <EPIC>-<n> · <Type> · <Summary>
- **Epic:** <EPIC-KEY>   **Points:** <n>   **Priority:** <Must/Should/Nice>   **SRS:** <§ / Req ID>
- **Depends on:** <ticket ids>
- **Description:** <what & why, 1–3 lines>
- **Acceptance Criteria:**
  - [ ] <verifiable outcome>
- **Unit Tests:**
  - [ ] <specific test case(s) to write>
- **Definition of Done:** Global DoD (Section 4) + AC + Unit Tests green.
```
**Types:** `Story` (user-facing/layer slice) · `Task` (technical) · `Sub-task` (small) · `Spike` (investigation) · `Check` (module-wide verification).

---

## 4. Global Definition of Done (applies to ALL tickets)

- [ ] Code follows Section 2 conventions; typed; lint + typecheck pass.
- [ ] Request validation present; API returns the standard envelope.
- [ ] **Unit tests written and passing**; module coverage ≥80%.
- [ ] RBAC enforced where applicable; audit log written on mutations.
- [ ] OpenAPI (`/docs`) reflects new/changed endpoints.
- [ ] No regressions: `pytest` + `vitest` green in CI.
- [ ] Ticket committed referencing its ID in the commit message.

---

## 4A. Implementing a Ticket — JIRA → CRISP conversion

Tickets are **specifications**, not prompts. To implement one, convert it into a **CRISP** prompt for Claude Code. The mapping is mechanical — every CRISP element already exists in the ticket + this master file:

| CRISP | Pull from |
|-------|-----------|
| **C**ontext | Ticket `Description` + epic `goal` + `Depends on` (what already exists) + `SRS` ref |
| **R**ole | The engineer persona for the layer (backend / frontend / DB / QA) — state it |
| **I**nstructions | Ticket `Description` steps + `Acceptance Criteria` + `Unit Tests` |
| **S**tyle | Section 1 (Stack) + Section 2 (Conventions) + Section 4 (Global DoD) |
| **P**arameters | Repo layout paths (Section 1) + `Req IDs` + `Points`/scope |

### Reusable conversion template (paste, then fill the `<…>` from the ticket)

```
CONTEXT: CRM app — React SPA + FastAPI + Prisma Client Python + PostgreSQL (Tailwind+DaisyUI).
Implementing ticket <ID> (SRS <ref>). Already done: <Depends-on tickets>. <1-line description>.

ROLE: You are a <backend/frontend/DB/QA> engineer. <one-line objective>.

INSTRUCTIONS:
<numbered steps derived from Description + Acceptance Criteria>
<final step: write the Unit Tests listed in the ticket>

STYLE: Follow CRM conventions (master §2) + Global DoD (§4): typed, async services,
Pydantic I/O, {data,error,meta} envelope, RBAC + audit on mutations, DaisyUI lemonade for UI.

PARAMETERS:
- Files: <paths per repo layout in §1>
- Req IDs: <…>   Coverage: ≥80% on this module.

ACCEPTANCE: <ticket Acceptance Criteria, restated as a checklist> + unit tests pass.
```

### Worked example — ticket `LEAD-6` (Lead scoring engine)

```
CONTEXT: CRM app — React SPA + FastAPI + Prisma Client Python + PostgreSQL.
Implementing ticket LEAD-6 (SRS LM-002, §3.1.2). Already done: LEAD-1 (Lead +
LeadScoreRule schema), LEAD-3 (Lead CRUD API). Build the configurable scoring engine.

ROLE: You are a backend engineer building a pure, testable scoring service.

INSTRUCTIONS:
1. Create app/modules/lead/scoring.py: a pure function evaluating the LeadScoreRule
   set against a lead → returns {score, breakdown}.
2. Recompute score on lead create/update and on engagement events.
3. Expose score + breakdown in the lead read model.
4. Write unit tests: zero rules, missing fields, weighting correctness.

STYLE: Follow CRM conventions (master §2) + Global DoD (§4): type hints, async service,
Pydantic I/O, {data,error,meta} envelope, no bare except.

PARAMETERS:
- Files: apps/api/app/modules/lead/scoring.py, service.py, tests/test_lead_scoring.py
- Req ID: LM-002.   Coverage: ≥80% on the lead module.

ACCEPTANCE: score reflects rules; rule change re-scores; the 3 unit tests pass.
```

### The per-ticket loop
1. Pick the next ticket in an epic (respect **Depends on**).
2. Convert → CRISP using the template above.
3. Paste into Claude Code → it implements.
4. Run the ticket's **Unit Tests** → green.
5. Satisfy **Global DoD (§4)** → commit `<ID>: <summary>`.
6. When all tickets in an epic pass, run its **`*-CHECK`** ticket. Finish the project with **EPIC-VERIFY**.

---

## 5. Epic Registry (one file per epic in `tickets/`)

| Epic Key | Epic | File | SRS | Tickets |
|----------|------|------|-----|---------|
| EPIC-PLAT | Platform & Infrastructure | `tickets/epic-plat-platform.md` | §2.3, §5.6 | PLAT-1…12 |
| EPIC-DB | Database & Schema (all modules) | `tickets/epic-db.md` | §2.3, §3, §8 | DB-1…16 |
| EPIC-AUTH | Authentication & Access | `tickets/epic-auth-access.md` | §5.2, AD-001 | AUTH-1…10 |
| EPIC-LEAD | Lead Management | `tickets/epic-lead.md` | §3.1, LM-001/2/3 | LEAD-1…16 |
| EPIC-CONT | Contact Management | `tickets/epic-contact.md` | §3.2.1, CO-001/2 | CONT-1…11 |
| EPIC-ACCT | Account Management | `tickets/epic-account.md` | §3.2.2, AC-001/2 | ACCT-1…12 |
| EPIC-PIPE | Opportunity & Pipeline | `tickets/epic-pipeline.md` | §3.3, PL-001/2/3 | PIPE-1…16 |
| EPIC-ACTV | Activity & Task Mgmt | `tickets/epic-activity.md` | §3.4 | ACTV-1…12 |
| EPIC-TICK | Service Ticketing | `tickets/epic-ticketing.md` | §3.5.1, TK-001 | TICK-1…11 |
| EPIC-SLA  | SLA Management | `tickets/epic-sla.md` | §3.5.2, TK-002 | SLA-1…11 |
| EPIC-KB   | Knowledge Base | `tickets/epic-kb.md` | §3.5.3, TK-003 | KB-1…11 |
| EPIC-PROJ | Project & Delivery | `tickets/epic-project.md` | §3.6, PR-001/2 | PROJ-1…15 |
| EPIC-CONTR| Contract & Renewal | `tickets/epic-contract.md` | §3.7, CT-001 | CONTR-1…13 |
| EPIC-INV  | Invoicing & Revenue | `tickets/epic-invoicing.md` | §3.8, IN-001/2 | INV-1…13 |
| EPIC-CAMP | Marketing & Campaigns | `tickets/epic-campaign.md` | §3.9, MK-001 | CAMP-1…13 |
| EPIC-ANLY | Analytics & Reporting | `tickets/epic-analytics.md` | §9, AN-001/2 | ANLY-1…14 |
| EPIC-COMM | Communication & Collab | `tickets/epic-comms.md` | §3.10 | COMM-1…12 |
| EPIC-ADMN | Admin & Configuration | `tickets/epic-admin.md` | AD-001/2, §7.2 | ADMN-1…11 |
| EPIC-INTG | Integration Framework | `tickets/epic-integrations.md` | §6 | INTG-1…12 |
| EPIC-DATA | Data Mgmt & Compliance | `tickets/epic-data.md` | §8 | DATA-1…9 |
| EPIC-NFR  | Non-Functional & Hardening | `tickets/epic-nfr.md` | §5, §7.3 | NFR-1…10 |
| EPIC-VERIFY| UAT, Go-Live & SRS Verify | `tickets/epic-verify.md` | §11 | VERIFY-1…6 |
| EPIC-SEED ⛔ | Dummy/Demo Data (ON-HOLD, opt-in) | `tickets/epic-seed.md` | §2.2, §7 | SEED-1…17 |

> ⛔ **EPIC-SEED is ON HOLD** — skip it in the normal build flow. Implement only when the user explicitly says so.

**Build order:** PLAT → **DB** → AUTH → (LEAD, CONT, ACCT, PIPE, ACTV) → (TICK, SLA, KB) → INTG(email) → (PROJ, CONTR, INV) → (CAMP, ANLY, COMM) → ADMN → DATA → NFR → VERIFY.
> EPIC-DB is foundational: it creates the database + **all tables for every module** up front, so each module epic's schema ticket is already satisfied (see EPIC-DB note).

---

## 6. Traceability (SRS §4 Req ID → Epic/Tickets)

| Req ID | Priority | Epic · Tickets |
|--------|----------|----------------|
| LM-001 | Must | EPIC-LEAD · LEAD-1,4,9,10 |
| LM-002 | Must | EPIC-LEAD · LEAD-6 |
| LM-003 | Should | EPIC-LEAD · LEAD-5 |
| CO-001 | Must | EPIC-CONT · CONT-1,3,8 |
| CO-002 | Must | EPIC-CONT · CONT-4 |
| AC-001 | Should | EPIC-ACCT · ACCT-5 |
| AC-002 | Nice | EPIC-ACCT · ACCT-6 |
| PL-001 | Must | EPIC-PIPE · PIPE-1,5 |
| PL-002 | Must | EPIC-PIPE · PIPE-7 |
| PL-003 | Must | EPIC-PIPE · PIPE-8,9 |
| TK-001 | Must | EPIC-TICK · TICK-3 |
| TK-002 | Must | EPIC-SLA · SLA-4,5 |
| TK-003 | Should | EPIC-KB · KB-4 |
| PR-001 | Must | EPIC-PROJ · PROJ-3,4 |
| PR-002 | Should | EPIC-PROJ · PROJ-7 |
| CT-001 | Must | EPIC-CONTR · CONTR-3,4 |
| IN-001 | Must | EPIC-INV · INV-3 |
| IN-002 | Should | EPIC-INV · INV-6 |
| MK-001 | Should | EPIC-CAMP · CAMP-3,4 |
| AN-001 | Must | EPIC-ANLY · ANLY-2,3,9 |
| AN-002 | Must | EPIC-ANLY · ANLY-6 |
| AD-001 | Must | EPIC-AUTH · AUTH-7 / EPIC-ADMN · ADMN-2 |
| AD-002 | Must | EPIC-ADMN · ADMN-3,4 |

---

## 7. Epic Progress

- [ ] EPIC-PLAT  - [ ] EPIC-DB
- [ ] EPIC-AUTH  - [ ] EPIC-LEAD  - [ ] EPIC-CONT  - [ ] EPIC-ACCT
- [ ] EPIC-PIPE  - [ ] EPIC-ACTV  - [ ] EPIC-TICK  - [ ] EPIC-SLA   - [ ] EPIC-KB
- [ ] EPIC-PROJ  - [ ] EPIC-CONTR - [ ] EPIC-INV   - [ ] EPIC-CAMP  - [ ] EPIC-ANLY
- [ ] EPIC-COMM  - [ ] EPIC-ADMN  - [ ] EPIC-INTG  - [ ] EPIC-DATA  - [ ] EPIC-NFR
- [ ] EPIC-VERIFY
- ⛔ EPIC-SEED (on-hold, opt-in — skip unless explicitly requested)
