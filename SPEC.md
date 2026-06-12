# SPEC.md — Specification Guide & Template

> **What this file is:** the guide for *how and when* to write a feature specification for the CRM, plus a
> reusable template. It is **not** the product requirements themselves.
>
> **Where the live specs actually are:**
> - **Master product spec →** `CRM_Requirements_Specification.docx` (SRS v1.0) — the authoritative requirements.
> - **Per-feature specs →** the JIRA tickets in `tickets/epic-*.md` — each ticket already carries Description,
>   Acceptance Criteria, Unit Tests, and an SRS Req ID. **For existing modules, the tickets ARE the spec.**
>
> **When you must write a NEW spec in this file (or a `specs/<feature>.md`):**
> - A feature **not covered by the SRS §3** (a scope change) — get scope sign-off first (see CLAUDE.md §7).
> - A complex change where the ticket isn't enough to align on data model / API / UI before coding.
> - A grader/stakeholder explicitly wants a standalone distilled spec separate from the SRS.
>
> **What belongs in a spec:** problem/goal · requirements · data model · API contract · UI/UX · acceptance
> criteria · **scope boundaries**. **What does NOT:** implementation code, conventions (those live in CLAUDE.md).

---

## What every spec MUST contain (the 5 phases)

| Phase | Answers | Why it's needed |
|-------|---------|-----------------|
| **1. Problem / Goal** | What are we solving, for which SRS role/persona? | Prevents building the wrong thing |
| **2. Requirements** | Functional + non-functional; in-scope list | Defines "what done looks like" |
| **3. Data Model** | New/changed tables, columns, relations (Prisma) | Drives the migration (EPIC-DB) |
| **4. API Contract** | Endpoints, request/response shapes, status codes, validation | FE + BE agree before coding |
| **5. Scope Boundaries** | What we are explicitly **NOT** doing | Stops scope creep; mirrors CLAUDE.md §7 |

A spec is "ready" when each phase is filled, acceptance criteria are testable, and it traces to an SRS Req ID
(or a recorded scope-change approval if the feature is new).

---

## Spec template (copy for a new feature → `specs/<feature>.md`)

```
# SPEC — <Feature Name>
Status: Draft | Approved   ·   SRS Ref: <§ / Req ID or "scope change #N">   ·   Owner: <name>   ·   Date: <>

## 1. Problem / Goal
<What user problem, which role (Sales Exec, Support Eng, …), what outcome.>

## 2. Requirements
Functional:
- [ ] <requirement>
Non-functional (perf, security, a11y per SRS §5):
- [ ] <requirement>
In scope:
- <…>

## 3. Data Model
- New/changed Prisma models + fields + relations + indexes.
- Migration impact (additive? destructive? backfill?).

## 4. API Contract
- METHOD /path → request (Pydantic/Zod), response ({data,error,meta}), status codes (201/422/401/403/404),
  RBAC rule, audit-logged? Y/N.

## 5. UI / UX
- Screens/components, states (loading/empty/error), which mockup it mirrors.

## 6. Acceptance Criteria
- [ ] <verifiable outcome>   (each must be testable)

## 7. Scope Boundaries
- NOT doing: <…>   ·   Deferred: <…>

## 8. Test Plan
- Unit / integration / component tests required to prove acceptance + ≥80% coverage.
```

---

## How a spec connects to the rest of the workflow

```
SPEC.md (the WHAT, before coding)
   └─> becomes / refines tickets in tickets/epic-*.md
          └─> each ticket → CRISP prompt (CRM_IMPLEMENTATION_TASKS.md §4A)
                 └─> Claude Code implements → tests → tick PROGRESS.md → commit → auto-review
```

For the **current SRS-covered backlog you do not need to write new specs** — the tickets already serve that
role. Reach for this template only for net-new or out-of-scope features, then turn the spec into tickets.
