# CLAUDE.md — CRM Application (IT Services)

> **What this file is:** the standing rulebook Claude Code **auto-loads at the start of every session** in this repo.
> It tells Claude the stack, conventions, scope, and workflow so you never have to re-explain them.
>
> **What belongs in this file:** project description · tech stack · architecture/repo layout · data flow ·
> coding conventions · validation rules · testing strategy · security requirements · **scope boundaries** ·
> the backlog/workflow map · Claude Code usage (plan mode, CRISP, agents, hooks) · Definition of Done.
>
> **What does NOT belong here:** per-feature requirements (those live in the SRS + `tickets/*.md`), secrets,
> or transient task notes. Keep this file stable; it evolves only when conventions or scope change.

---

## 1. Project Description

An internal **CRM for an Indian IT services company** covering the full customer lifecycle: lead capture &
qualification, contacts/accounts, sales pipeline, activities, support ticketing & SLAs, knowledge base,
project delivery, contracts, invoicing, marketing campaigns, analytics, and admin. Authoritative requirements
live in `CRM_Requirements_Specification.docx` (SRS v1.0). Currency/notation is Indian (₹, Lakhs/L, Crores/Cr).

---

## 2. Stack

| Layer | Technology |
|-------|-----------|
| Frontend | **React 18 SPA** (Vite + TypeScript), React Router, TanStack Query, Tailwind + **DaisyUI (lemonade)**, react-hook-form + Zod, Recharts |
| Backend | **Python + FastAPI** (async REST), layered `router → service → repository` |
| ORM / DB | **Prisma Client Python** (`prisma-client-py`) + **PostgreSQL** |
| Validation | **Pydantic** (API edge) + **Zod** (forms) |
| Auth | JWT in httpOnly cookies, **2FA (TOTP)**, RBAC dependency injection |
| Testing | **pytest** + httpx/ASGI (API), **Vitest + React Testing Library** (web), test PostgreSQL DB |
| Infra | Docker + docker-compose, GitHub Actions CI/CD, FastAPI OpenAPI (`/docs`), structlog |

---

## 3. Architecture & Repo Layout

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
│       └── src/
│           ├── features/<mod>/    # pages, components, hooks, api
│           ├── components/ (ui/, layout/, charts/)
│           ├── lib/ (apiClient, auth, cn)
│           └── routes.tsx
├── packages/shared/               # TS types + Zod (web); enums mirrored to a Python enums module
├── docker-compose.yml
└── .github/workflows/ci.yml
```

**Data flow:** React SPA → FastAPI REST (`router → service → repository`) → Prisma Client Python → PostgreSQL.
Responses are unwrapped from a standard envelope on the client.

---

## 4. Coding Conventions

### Naming
- **Files/folders:** `kebab-case` (web), `snake_case` (python modules).
- **React components:** `PascalCase` **named exports** (no default exports from component files).
- **Hooks:** `useXxx` (camelCase). **Zod schemas:** suffix `Schema`. **Module-level constants:** `SCREAMING_SNAKE_CASE`.
- **FastAPI routers:** RESTful resource routes; handlers typed and async.
- **Types/Interfaces:** `PascalCase`.

### File structure
- One component per file; co-locate web tests mirroring `features/`.
- API: one module folder per resource with `router.py`, `service.py`, `schemas.py` (Pydantic), `repository.py`.
- Shared types/enums live in `packages/shared`; **no barrel `index.ts` files** — import from the specific path.

### TypeScript
- `strict: true` — no `any`, no `@ts-ignore` without an explanatory comment.
- Explicit return types on exported/async functions.

### Python
- Type hints everywhere; async services; **no bare `except`**; Pydantic models for all request/response I/O.

### Styling
- **Tailwind utility classes only** — no inline `style={{}}` except dynamic values (e.g., chart sizing).
- DaisyUI **lemonade** theme; brand green `#507d2a`; use `cn()` (clsx + tailwind-merge) for conditional classes.
- Mobile-first responsive (`sm:`, `md:`, `lg:`); **no horizontal scroll**. Icons in colored boxes use `stroke="white"`.

### API rules
- **Validate every request body** (Pydantic) before touching Prisma.
- Always return the envelope: **`{ "data": ..., "error": ..., "meta": ... }`**.
- Semantic status codes: **201** create, **422** validation, **401/403** auth, **404** missing.

### Comments
- Only when the **why** is non-obvious. Document external constraints (rate limits, SLA timers, Prisma quirks).

---

## 5. Testing Strategy

- **Target:** ≥80% line coverage on `services`, `routers`, and `features`. CI fails below 80%.
- **Unit:** pure functions/services (scoring, SLA timers, forecasting, validators).
- **Integration:** API routes via httpx/ASGI against a **test PostgreSQL** DB (migrate → seed → truncate between tests).
- **Component:** React Testing Library — test behavior, not implementation.
- **Edge cases:** empty datasets, rate-limited integrations, expired sessions, SLA breaches, zero-metric ranges.
- **No snapshot tests.** Each ticket ships its own unit tests (see `tickets/*.md`).

---

## 6. Security (SRS §5.2 — non-negotiable)

- RBAC with **field-level and record-level** permissions on every protected route.
- **2FA (TOTP)**; JWT in httpOnly+SameSite cookies; **30-min** session timeout.
- Encrypt at rest (AES-256) / in transit (TLS 1.3); encrypt integration tokens.
- **Audit log** on all data modifications, logins, and admin actions.
- OWASP Top 10 mitigations; no secrets in code; parameterized/ORM queries (guard the custom report builder).

---

## 7. Scope Boundaries — what the CRM does NOT include

Anything not in the SRS §3 functional modules requires an explicit scope-change discussion before building.

| Out of scope (Phase-2 or non-goals) | Reason |
|---|---|
| Native mobile app (iOS/Android) | Phase-1 is responsive web only (SRS §7.3) |
| Building 3rd-party tools themselves | We **integrate** (email, Jira, Slack, accounting, eSign) — not rebuild them |
| Features beyond SRS §3 | Needs scope-change sign-off |
| Multi-tenant SaaS isolation | Single-org deployment assumption |

---

## 8. Backlog & Workflow Map (read these)

| File | Purpose |
|------|---------|
| `AGENT-CONTEXT.md` | **Slim agent context (80 lines)** — stack, conventions, DoD, CRISP template. Loaded by agent instead of full master file. |
| `CRM_IMPLEMENTATION_TASKS.md` | Full backlog index: stack, conventions, **§4A JIRA→CRISP rule**, build order, traceability (human reference) |
| `tickets/epic-*.md` | Full epic files — read once per epic for dependency planning |
| `tickets/<prefix>/<ID>.md` | **Per-ticket files** (e.g. `tickets/lead/LEAD-6.md`) — agent loads only the ticket it's implementing |
| `PROGRESS.md` | Master checklist — tick `[x]` per completed ticket (saving it triggers the auto-commit hook) |
| `HOW-TO-IMPLEMENT.md` | Playbook: `Implement EPIC-<KEY>` (full epic) or `Implement <TICKET-ID>` (single ticket) |
| `.claude/agents/epic-implementer.md` | Agent (`claude-sonnet-4-6`) — implements epic or single ticket, verifies, reports |
| `.claude/agents/crm-reviewer.md` | Post-commit reviewer (`claude-haiku-4-5`) → append-only log to `reports/review-findings.md` |
| `docs/SCHEMA-SUMMARY.md` | Schema summary (generated by DB-15) — agents load this after EPIC-DB instead of full schema.prisma |
| `SPEC.md` | When/how to write a feature spec (the SRS + tickets are the live specs) |
| `docs/BUSINESS-FLOW.md` | Business process flowcharts (lead→deal→project→invoice, ticket/SLA, renewals) |
| `docs/ARCHITECTURE.md` | System/container/deployment diagrams, request lifecycle, auth/RBAC flow |
| `docs/TECH-DESIGN.md` | Technical design: layers, API standards, data, security, integrations, NFRs |
| `WORKFLOW.md` | How implementing an epic or single ticket works (agent + hooks flow) |

**Build order:** PLAT → DB → AUTH → (LEAD, CONT, ACCT, PIPE, ACTV) → (TICK, SLA, KB) → INTG(email) →
(PROJ, CONTR, INV) → (CAMP, ANLY, COMM) → ADMN → DATA → NFR → VERIFY. (EPIC-SEED is on-hold/opt-in.)

---

## 9. Claude Code Usage

- **Plan mode:** enter it before a new API route, DB migration, or multi-file feature; confirm the plan before code.
- **CRISP prompts:** applied internally by the agent using `AGENT-CONTEXT.md §4A` — never output, never hand-written.
- **One ticket = one focused change = one commit** (`<ID>: <summary>`), produced by the auto-commit hook when `PROGRESS.md` is ticked.
- **Agents:**
  - `epic-implementer` (`claude-sonnet-4-6`) — `Implement EPIC-<KEY>` for a full epic, `Implement <TICKET-ID>` for a single ticket.
  - `crm-reviewer` (`claude-haiku-4-5`) — reviews each auto-commit; append-only log to `reports/review-findings.md`.
- **Hooks (`.claude/settings.json`):** auto-commit on PROGRESS.md save → auto-review (Haiku) on commit.
- **Token efficiency:** agent loads `AGENT-CONTEXT.md` (80 lines) + `tickets/<prefix>/<ID>.md` (8 lines) per ticket — not large master files.
- **EPIC-SEED is on hold** — never implement it unless explicitly asked.

---

## 10. Definition of Done (every ticket)

- [ ] Follows §4 conventions; typed; lint + typecheck pass.
- [ ] Request validation present; API returns the `{data,error,meta}` envelope with correct status codes.
- [ ] **Unit tests written and passing**; module coverage ≥80%.
- [ ] RBAC enforced where applicable; audit log written on mutations.
- [ ] OpenAPI (`/docs`) reflects new/changed endpoints.
- [ ] No regressions (full `pytest` + `vitest` green in CI).
- [ ] `PROGRESS.md` ticked; committed as `<ID>: <summary>`.
