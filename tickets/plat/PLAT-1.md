> **Epic context:** EPIC-PLAT · Platform & Infrastructure

### PLAT-1 · Task · Monorepo scaffold
- **Points:** 2 **SRS:** §5.6 **Depends on:** —
- **Description:** pnpm-workspace monorepo with `apps/api`, `apps/web`, `packages/shared`, root tooling.
- **Acceptance Criteria:**
  - [ ] `pnpm-workspace.yaml`, root scripts (`dev/build/test/lint`), `.gitignore`, `.env.example`, editor/lint/format configs.
  - [ ] `apps/api`, `apps/web`, `packages/shared` initialized.
- **Unit Tests:** [ ] CI smoke: `pnpm install` + `pnpm -r build` succeed (verified in PLAT-11).
- **DoD:** Global DoD + AC.