> **Epic context:** EPIC-PLAT · Platform & Infrastructure

### PLAT-12 · Check · Platform module-wide check
- **Points:** 1 **Depends on:** PLAT-1…11
- **Description:** Verify the foundation end-to-end.
- **Acceptance Criteria:**
  - [ ] `docker compose up` → `/health` 200, `/docs` renders, SPA shell loads.
  - [ ] CI green incl. coverage gate; logging emits JSON.
- **Unit Tests:** [ ] e2e smoke test hitting `/health` through the running stack.
- **DoD:** Global DoD + all PLAT tickets closed.