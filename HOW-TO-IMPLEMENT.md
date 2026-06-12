# HOW TO IMPLEMENT — CRM Build Playbook

This is your day-to-day guide for turning the JIRA backlog into working code.
Three ways to work: **(A) single ticket**, **(B) full epic via agent**, or **(C) manual CRISP**.

- **Slim agent context:** `AGENT-CONTEXT.md` (stack, conventions, DoD, CRISP template — loaded by agent automatically)
- **Backlog index:** `CRM_IMPLEMENTATION_TASKS.md` (full detail — for human reference)
- **Epic ticket files:** `tickets/epic-*.md` (full epic, read once for planning)
- **Per-ticket files:** `tickets/<prefix>/<TICKET-ID>.md` (e.g. `tickets/lead/LEAD-6.md` — agent loads per ticket)
- **Agent:** `.claude/agents/epic-implementer.md` (`claude-sonnet-4-6`, handles both epic and single-ticket mode)

---

## Build order (never skip dependencies)
```
PLAT → AUTH → (LEAD, CONT, ACCT, PIPE, ACTV) → (TICK, SLA, KB) → INTG(email)
     → (PROJ, CONTR, INV) → (CAMP, ANLY, COMM) → ADMN → DATA → NFR → VERIFY
```
Within an epic, follow each ticket's **Depends on**. Go top-to-bottom and you won't hit missing pieces.

---

# PART A — Manual workflow (one ticket at a time)

### The 6-step loop
1. **Pick** the next ticket whose `Depends on` is satisfied.
2. **Orient** — have Claude read the ticket + repo and plan (no code yet).
3. **CRISP + implement** — Claude generates the CRISP prompt and implements (see 3 options below).
4. **Verify** — run the ticket's Acceptance Criteria + Unit Tests until green.
5. **Commit** — tick `[x]` in the epic file, `git commit -m "<ID>: <summary>"`.
6. **Next** — repeat; when the epic's tickets are done, run its `*-CHECK` ticket.

### Step 2 — Orientation prompt (paste into Claude Code)
```
I'm implementing a CRM from a JIRA backlog. Read:
- CRM_IMPLEMENTATION_TASKS.md (stack §1, conventions §2, Global DoD §4, §4A CRISP rule)
- tickets/<epic file> (find ticket <ID>)
Then, before any code: (1) your understanding of <ID>, (2) what exists vs missing in the repo,
(3) exact files you'll create, (4) assumptions to confirm. Do NOT implement yet.
```

### Step 3 — You do NOT hand-write CRISP. Pick one:
- **Option A (recommended):** Claude writes the CRISP, you approve, it implements.
  ```
  Take ticket <ID> from tickets/<epic file>. Using the §4A JIRA→CRISP rule in
  CRM_IMPLEMENTATION_TASKS.md, write the CRISP prompt and show me. Don't implement yet — wait for "go".
  ```
- **Option B (fastest):** collapse it.
  ```
  Implement ticket <ID> from tickets/<epic file>. Follow §4A CRISP + conventions (§2) + Global DoD (§4).
  Plan first, then implement, then run the Acceptance Criteria + Unit Tests.
  ```
- **Option C:** paste a ready CRISP block yourself (use the EPIC-PLAT set below or master §4A template) — only when you want to tweak it first.

### Step 4 — Verify
Run what the ticket's **Acceptance Criteria** + **Unit Tests** specify, e.g. `pnpm install && pnpm -r build`, `pytest`, `vitest`. Stay on the ticket until green.

### Step 5 — Commit (one ticket = one commit)
```
git checkout -b <epic-key-lower>           # once per epic
# set the ticket's [ ] -> [x] in the epic file
git add -A
git commit -m "<ID>: <summary>"
```

---

# PART B — Agent workflow (whole epic, auto-verified + report)

Use the **`epic-implementer`** subagent (`claude-sonnet-4-6`) to implement an entire epic end-to-end.

### Invoke it
```
Implement EPIC-PLAT
```
(For later epics: `Implement EPIC-AUTH`, `Implement EPIC-LEAD`, …)

### Invoke for a single ticket
```
Implement PLAT-1
Implement LEAD-6
```
The agent auto-detects the ticket ID, finds `tickets/plat/PLAT-1.md`, checks dependencies in
`PROGRESS.md`, implements + tests, auto-commits, and prints a mini-report. Same hooks fire.

### What the agent guarantees (both modes)
- Loads `AGENT-CONTEXT.md` (slim) + only the specific ticket file per ticket — not large master files.
- CRISP conversion applied internally — no token-wasting output.
- Writes **Unit Tests** and **won't mark done unless tests + AC pass**.
- **One commit per ticket** auto-committed by hook; `crm-reviewer` (Haiku) reviews each commit.
- **Epic mode only:** runs `*-CHECK`, flips epic in both trackers, writes `reports/<EPIC-KEY>-completion-report.md`.
- **Single-ticket mode:** checks `Depends on` first — reports BLOCKED if unmet, never fakes.

### When to use which
- **`Implement EPIC-<KEY>`:** move fast through a full epic, get a verification report.
- **`Implement <TICKET-ID>`:** implement one specific ticket without running the whole epic.
- **Manual (Part A):** when you want to review the CRISP prompt before code lands.

---

# READY CRISP PROMPTS — EPIC-PLAT (Epic 1, start here)

Copy any block into Claude Code (Option C). These are pre-converted from `tickets/epic-plat-platform.md`.

### PLAT-1 · Monorepo scaffold
```
CONTEXT: New empty CRM monorepo. Ticket PLAT-1 (SRS §5.6). Nothing exists yet.
ROLE: DevOps-minded full-stack engineer.
INSTRUCTIONS:
1. git init + pnpm-workspace.yaml (apps/*, packages/*).
2. Root package.json scripts: dev, build, test, lint (across workspaces).
3. Add tsconfig.base.json, .eslintrc, .prettierrc, .editorconfig, .gitignore, .env.example.
4. Create empty apps/api, apps/web, packages/shared (each with package.json).
STYLE: master §2 + §4 — strict TS, kebab-case.
PARAMETERS: Files: root configs + 3 workspace folders. Scope: scaffold only.
ACCEPTANCE: pnpm install succeeds; pnpm -r build runs; lint passes.
```

### PLAT-2 · FastAPI scaffold (layered)
```
CONTEXT: apps/api empty. Ticket PLAT-2 (SRS §2.3). PLAT-1 done.
ROLE: Backend engineer establishing API architecture.
INSTRUCTIONS:
1. FastAPI app: app/main.py, app/core/ (config via Pydantic Settings), app/db/, app/middleware/, app/modules/.
2. Response-envelope helpers ok()/fail() returning {data,error,meta}.
3. GET /health -> {data:{status:"ok"},error:null}. Validate env at startup.
STYLE: master §2 + §4 — async, type hints, thin routers, logic in services.
PARAMETERS: Files: apps/api/app/**. Stack: FastAPI.
ACCEPTANCE: /health returns envelope; env validated; unit tests test_health_ok + envelope shape pass.
```

### PLAT-3 · Prisma Client Python + Postgres
```
CONTEXT: Ticket PLAT-3 (SRS §2.3). PLAT-2 done.
ROLE: Database engineer.
INSTRUCTIONS:
1. prisma/schema.prisma with provider prisma-client-py, datasource PostgreSQL.
2. Generated client wrapper in app/db/; connect on startup, disconnect on shutdown.
3. A `db` dependency injecting a connected client. Run first migration.
STYLE: master §2 + §4.
PARAMETERS: Files: apps/api/prisma/**, app/db/**. Stack: Prisma Client Python, Postgres.
ACCEPTANCE: prisma generate + migrate dev work; test_db_connects passes.
```

### PLAT-4 · React SPA scaffold (Vite + Tailwind + DaisyUI)
```
CONTEXT: apps/web empty. Ticket PLAT-4 (SRS §7.1). PLAT-1 done.
ROLE: Frontend engineer.
INSTRUCTIONS:
1. Vite React+TS. Install Tailwind, DaisyUI (lemonade), react-router-dom, @tanstack/react-query, axios, react-hook-form, recharts.
2. tailwind.config with lemonade theme + brand #507d2a.
3. src/lib/apiClient.ts (axios, credentials, unwrap {data,error}, normalize errors); QueryClientProvider + BrowserRouter.
STYLE: master §2 + §4 — mobile-first, cn() helper.
PARAMETERS: Files: apps/web/src/**.
ACCEPTANCE: themed shell renders; apiClient unwrap test passes.
```

### PLAT-5 · Shared package (types + Zod + enums)
```
CONTEXT: Ticket PLAT-5. PLAT-1 done.
ROLE: Engineer defining the shared contract layer.
INSTRUCTIONS:
1. packages/shared/src: ApiResponse<T>, domain enums (Role, LeadStatus, TicketPriority, DealStage), schemas/.
2. Mirror enums to a Python enums.py for the API.
STYLE: master §2 — one concept per file, no barrels.
PARAMETERS: Files: packages/shared/src/**. Stack: Zod, TS.
ACCEPTANCE: both apps import shared + typecheck; Zod round-trip test passes.
```

### PLAT-6 · Error handling + structured logging
```
CONTEXT: Ticket PLAT-6 (SRS §5.6). PLAT-2 done.
ROLE: Backend reliability engineer.
INSTRUCTIONS:
1. FastAPI exception handlers -> envelope; Pydantic validation -> 422 with field errors.
2. structlog JSON logs w/ request id; redact secrets. FE error boundary + toast.
STYLE: master §2 + §4.
PARAMETERS: Files: apps/api/app/middleware/error.py, app/core/logging.py; apps/web error boundary.
ACCEPTANCE: errors return envelope; test_validation_error_returns_422_fields passes; logs are JSON.
```

### PLAT-7 · App shell (Sidebar/Header/PageShell) + UI kit
```
CONTEXT: Ticket PLAT-7 (SRS §7.1/§7.2). PLAT-4 done. Mirror the mockups/ look.
ROLE: Frontend engineer building the design-system shell.
INSTRUCTIONS:
1. components/layout: Sidebar (fixed 230px), Header (bell + avatar -> /profile), PageShell, cn().
2. components/ui: Button, Card, Badge, Table, Modal, Input, Select, Tabs (DaisyUI).
3. light/dark theme toggle persisted per user; no horizontal scroll.
STYLE: master §2 + §4 — reuse mockups/ patterns, lemonade theme.
PARAMETERS: Files: apps/web/src/components/**.
ACCEPTANCE: pages wrap in PageShell; header/sidebar consistent; theme-persist + header-render tests pass.
```

### PLAT-8 · Testing harness (pytest + vitest + test DB)
```
CONTEXT: Ticket PLAT-8 (SRS §5.6). PLAT-3 + PLAT-4 done.
ROLE: QA-focused engineer.
INSTRUCTIONS:
1. pytest + httpx ASGI client + test Postgres fixtures (migrate/seed/truncate).
2. Vitest + RTL + jsdom. Coverage gate 80% (CI fails below).
STYLE: master §2 — behavior-focused, no snapshots.
PARAMETERS: Files: apps/api/tests/**, apps/web vitest config + sample tests.
ACCEPTANCE: pytest + vitest run with coverage; sample tests pass; <80% fails.
```

### PLAT-9 · Dockerization + docker-compose
```
CONTEXT: Ticket PLAT-9 (SRS §2.3). PLAT-2 + PLAT-4 done.
ROLE: DevOps engineer.
INSTRUCTIONS:
1. Multi-stage Dockerfiles (api, web), non-root.
2. docker-compose.yml: api, web, postgres, volumes, env.
STYLE: master §2 — small images.
PARAMETERS: Files: apps/*/Dockerfile, docker-compose.yml.
ACCEPTANCE: docker compose up serves api+web+db; docker compose config validates.
```

### PLAT-10 · OpenAPI docs
```
CONTEXT: Ticket PLAT-10 (SRS §5.6). PLAT-2 done.
ROLE: Backend engineer.
INSTRUCTIONS: enable FastAPI OpenAPI at /docs; tag modules; keep current as routes grow.
STYLE: master §2.
PARAMETERS: Files: apps/api/app/main.py (openapi config).
ACCEPTANCE: /docs renders; test_openapi_json_available passes.
```

### PLAT-11 · CI/CD pipeline
```
CONTEXT: Ticket PLAT-11 (SRS §2.3/§5.2/§11). PLAT-8 done.
ROLE: DevOps engineer.
INSTRUCTIONS:
1. .github/workflows/ci.yml: install -> lint -> typecheck -> pytest (Postgres service) -> vitest -> build.
2. Security stage: pip-audit + pnpm audit + secret scan; fail on High/Critical. Deploy gate on main.
STYLE: master §2.
PARAMETERS: Files: .github/workflows/ci.yml.
ACCEPTANCE: PR runs full pipeline; coverage <80% or High vuln fails build.
```

### PLAT-12 · Check · Platform module-wide check
```
CONTEXT: Ticket PLAT-12. PLAT-1..11 done.
ROLE: QA lead verifying the foundation.
INSTRUCTIONS:
1. e2e smoke: docker compose up -> /health 200, /docs renders, SPA shell loads.
2. Confirm CI green incl. coverage gate; logs are JSON.
STYLE: master §2 + §4.
PARAMETERS: Files: apps/api/tests/test_smoke.py.
ACCEPTANCE: smoke test green; all PLAT tickets [x]; coverage gate active.
```

---

## Quick reference
| Need | Do this |
|------|---------|
| Start the project | `Implement EPIC-PLAT` or `Implement PLAT-1` for just the first ticket |
| Implement one ticket | `Implement <TICKET-ID>` e.g. `Implement LEAD-6` |
| Do a whole epic + get a report | `Implement <EPIC-KEY>` → reads `reports/<EPIC-KEY>-completion-report.md` |
| Convert a ticket to CRISP manually | Option A prompt (Claude writes it) — you don't type CRISP by hand |
| Check what's next | Build order above + each ticket's `Depends on` |
| Find a ticket file | `tickets/<prefix>/<TICKET-ID>.md` e.g. `tickets/lead/LEAD-6.md` |
| Prove SRS coverage at the end | Run EPIC-VERIFY (`tickets/epic-verify.md`) |
