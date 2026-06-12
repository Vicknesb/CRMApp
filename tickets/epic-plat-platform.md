# EPIC-PLAT · Platform & Infrastructure

> **Epic goal:** Stand up the monorepo, FastAPI + Prisma backend, React SPA, testing, Docker, and CI/CD that every other epic builds on.
> **SRS:** §2.3 (operating environment), §5.6 (maintainability). **Priority:** Must. **Depends on:** none.

---

### PLAT-1 · Task · Monorepo scaffold
- **Points:** 2 **SRS:** §5.6 **Depends on:** —
- **Description:** pnpm-workspace monorepo with `apps/api`, `apps/web`, `packages/shared`, root tooling.
- **Acceptance Criteria:**
  - [ ] `pnpm-workspace.yaml`, root scripts (`dev/build/test/lint`), `.gitignore`, `.env.example`, editor/lint/format configs.
  - [ ] `apps/api`, `apps/web`, `packages/shared` initialized.
- **Unit Tests:** [ ] CI smoke: `pnpm install` + `pnpm -r build` succeed (verified in PLAT-11).
- **DoD:** Global DoD + AC.

### PLAT-2 · Task · FastAPI scaffold (layered)
- **Points:** 3 **SRS:** §2.3 **Depends on:** PLAT-1
- **Description:** FastAPI app with `core/`, `db/`, `middleware/`, `modules/` layout, config via Pydantic Settings, `/health`, and **CORS** configured for the SPA origin with credentials.
- **Acceptance Criteria:**
  - [ ] `app/main.py` boots; `GET /health` → `{data:{status:"ok"},error:null}`.
  - [ ] Response-envelope helpers; settings loaded + validated from env.
  - [ ] **CORS middleware** enabled: allowed origin = the SPA URL (env `WEB_ORIGIN`, e.g. `http://localhost:5173`), `allow_credentials=True`, sensible allowed methods/headers — so the browser sends/accepts the httpOnly auth cookie cross-origin.
- **Unit Tests:** [ ] `test_health_ok`; [ ] envelope helper shapes `data/error/meta`; [ ] **CORS preflight (`OPTIONS`) returns the SPA origin in `Access-Control-Allow-Origin` with `Access-Control-Allow-Credentials: true`; a disallowed origin is rejected.**
- **DoD:** Global DoD + AC.

### PLAT-3 · Task · Prisma Client Python + Postgres wiring
- **Points:** 3 **SRS:** §2.3 **Depends on:** PLAT-2
- **Description:** `prisma/schema.prisma` (provider `prisma-client-py`), datasource Postgres, generated client wrapper, connection lifecycle on startup/shutdown.
- **Acceptance Criteria:**
  - [ ] `prisma generate` + `prisma migrate dev` work; client connects on app startup.
  - [ ] `db` dependency injects a connected Prisma client.
- **Unit Tests:** [ ] `test_db_connects`; [ ] migration applies on fresh DB.
- **DoD:** Global DoD + AC.

### PLAT-4 · Task · React SPA scaffold (Vite + Tailwind + DaisyUI)
- **Points:** 3 **SRS:** §7.1 **Depends on:** PLAT-1
- **Description:** Vite React+TS, Tailwind+DaisyUI lemonade, React Router, TanStack Query, axios apiClient (credentials + envelope unwrap).
- **Acceptance Criteria:**
  - [ ] Themed shell page renders; apiClient unwraps `{data,error}` and normalizes errors.
- **Unit Tests:** [ ] `apiClient` unwraps data + throws normalized error on `error` payload.
- **DoD:** Global DoD + AC.

### PLAT-5 · Task · Shared package (types + Zod + enums)
- **Points:** 2 **Depends on:** PLAT-1
- **Description:** `@crm/shared` exporting `ApiResponse<T>`, domain enums, Zod schemas; enums mirrored to a Python `enums.py`.
- **Acceptance Criteria:** [ ] Both apps import shared enums/types and typecheck.
- **Unit Tests:** [ ] Zod schema round-trip parse test.
- **DoD:** Global DoD + AC.

### PLAT-6 · Task · Error handling + structured logging
- **Points:** 2 **SRS:** §5.6 **Depends on:** PLAT-2
- **Description:** FastAPI exception handlers → envelope; Pydantic validation → 422 with field errors; structlog JSON w/ request id. FE error boundary + toast.
- **Acceptance Criteria:** [ ] Raised errors return envelope; 422 lists invalid fields; logs are JSON.
- **Unit Tests:** [ ] `test_validation_error_returns_422_fields`; [ ] handler maps domain error → status.
- **DoD:** Global DoD + AC.

### PLAT-7 · Task · App shell (Sidebar/Header/PageShell) + UI kit
- **Points:** 3 **SRS:** §7.1/§7.2 **Depends on:** PLAT-4
- **Description:** Port mockups: fixed sidebar, header (bell + avatar→/profile), `PageShell`; DaisyUI UI primitives (Button/Card/Badge/Table/Modal/Input/Select/Tabs); theme toggle; no horizontal scroll.
- **Acceptance Criteria:** [ ] Pages wrap in `PageShell`; consistent header/sidebar; theme persists.
- **Unit Tests:** [ ] Header renders bell+avatar link; [ ] theme toggle persists to storage.
- **DoD:** Global DoD + AC.

### PLAT-8 · Task · Testing harness (pytest + vitest + test DB)
- **Points:** 3 **SRS:** §5.6 **Depends on:** PLAT-3, PLAT-4
- **Description:** pytest + httpx ASGI client + test Postgres (migrate/seed/truncate fixtures); Vitest + RTL; coverage gate 80%.
- **Acceptance Criteria:** [ ] `pytest` + `vitest` run with coverage; sample tests pass; <80% fails.
- **Unit Tests:** [ ] sample service unit test; [ ] sample component test.
- **DoD:** Global DoD + AC.

### PLAT-9 · Task · Dockerization + docker-compose
- **Points:** 2 **SRS:** §2.3 **Depends on:** PLAT-2, PLAT-4
- **Description:** Multi-stage Dockerfiles (api, web) + compose with postgres + volumes + env.
- **Acceptance Criteria:** [ ] `docker compose up` serves api+web+db on localhost.
- **Unit Tests:** [ ] compose config validates (`docker compose config`).
- **DoD:** Global DoD + AC.

### PLAT-10 · Task · OpenAPI docs
- **Points:** 1 **SRS:** §5.6 **Depends on:** PLAT-2
- **Description:** FastAPI auto-OpenAPI at `/docs`; tag modules; keep current as endpoints are added.
- **Acceptance Criteria:** [ ] `/docs` renders live schema.
- **Unit Tests:** [ ] `test_openapi_json_available`.
- **DoD:** Global DoD + AC.

### PLAT-11 · Task · CI/CD pipeline
- **Points:** 3 **SRS:** §2.3/§5.2/§11 **Depends on:** PLAT-8
- **Description:** GitHub Actions: install → lint → typecheck → pytest (Postgres service) → vitest → build → security (`pip-audit`/`pnpm audit` + secret scan) → deploy gate.
- **Acceptance Criteria:** [ ] PR runs full pipeline; coverage <80% or High vuln fails build.
- **Unit Tests:** [ ] pipeline green on a trivial PR (meta-validation).
- **DoD:** Global DoD + AC.

### PLAT-12 · Check · Platform module-wide check
- **Points:** 1 **Depends on:** PLAT-1…11
- **Description:** Verify the foundation end-to-end.
- **Acceptance Criteria:**
  - [ ] `docker compose up` → `/health` 200, `/docs` renders, SPA shell loads.
  - [ ] CI green incl. coverage gate; logging emits JSON.
- **Unit Tests:** [ ] e2e smoke test hitting `/health` through the running stack.
- **DoD:** Global DoD + all PLAT tickets closed.
