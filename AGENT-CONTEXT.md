# CRM Agent Context (slim — load this instead of the full master file)

## Stack
React 18 SPA (Vite+TS) · Tailwind+DaisyUI lemonade (#507d2a) · TanStack Query · react-hook-form+Zod
FastAPI (Python, async) · router→service→repository · Pydantic I/O · Prisma Client Python · PostgreSQL
JWT httpOnly cookie · 2FA TOTP · RBAC (field+record level) · pytest + Vitest/RTL · Docker + GitHub Actions

## Repo layout
```
crm/
├── apps/api/app/modules/<mod>/  router.py  service.py  repository.py  schemas.py
├── apps/api/prisma/             schema.prisma  migrations/  seed.py
├── apps/api/tests/
├── apps/web/src/features/<mod>/ pages/  components/  hooks/  api/
├── apps/web/src/components/     ui/  layout/  charts/
├── apps/web/src/lib/            apiClient.ts  auth.ts  cn.ts
└── packages/shared/src/         ApiResponse.ts  enums/  schemas/
```

## Conventions (non-negotiable)
- Python: snake_case, type hints everywhere, async services, no bare `except`
- API response: always `{ "data": ..., "error": ..., "meta": ... }` — status 200/201/422/401/403/404
- Validate every request with Pydantic before any DB access
- Frontend: kebab-case files, PascalCase named exports (no default exports), `useXxx` hooks
- Zod schemas suffixed `Schema`; Tailwind+DaisyUI only; `cn()` for conditional classes
- No barrel index.ts files — import from specific paths
- RBAC enforced + audit log written on every mutation
- Coverage ≥ 80% on services/routers/features — no snapshot tests

## Global Definition of Done (every ticket)
- [ ] Typed; lint + typecheck pass
- [ ] Pydantic validation; `{data,error,meta}` envelope; correct status codes
- [ ] Unit tests written + passing; module coverage ≥ 80%
- [ ] RBAC enforced where applicable; audit log on mutations
- [ ] OpenAPI `/docs` reflects new/changed endpoints
- [ ] No regressions: `pytest` + `vitest` green

## CRISP conversion (§4A) — mechanical mapping
| CRISP | Source |
|-------|--------|
| Context | Ticket Description + epic goal + Depends on + SRS ref |
| Role | engineer persona for the layer (backend/frontend/DB/QA) |
| Instructions | Description steps + Acceptance Criteria + Unit Tests |
| Style | Stack + Conventions + Global DoD above |
| Parameters | Repo layout paths + Req IDs |

## Build order
PLAT → DB → AUTH → (LEAD, CONT, ACCT, PIPE, ACTV) → (TICK, SLA, KB) → INTG(email) → (PROJ, CONTR, INV) → (CAMP, ANLY, COMM) → ADMN → DATA → NFR → VERIFY
⛔ EPIC-SEED = ON HOLD — skip unless user explicitly asks

## Per-ticket files location
Individual tickets live at `tickets/<prefix>/<TICKET-ID>.md` (e.g. `tickets/lead/LEAD-6.md`).
Epic files `tickets/epic-*.md` still exist as the authoritative source.
After EPIC-DB completes, load `docs/SCHEMA-SUMMARY.md` instead of re-reading full schema.prisma.
