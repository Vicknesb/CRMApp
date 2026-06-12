> **Epic context:** EPIC-PLAT · Platform & Infrastructure

### PLAT-8 · Task · Testing harness (pytest + vitest + test DB)
- **Points:** 3 **SRS:** §5.6 **Depends on:** PLAT-3, PLAT-4
- **Description:** pytest + httpx ASGI client + test Postgres (migrate/seed/truncate fixtures); Vitest + RTL; coverage gate 80%.
- **Acceptance Criteria:** [ ] `pytest` + `vitest` run with coverage; sample tests pass; <80% fails.
- **Unit Tests:** [ ] sample service unit test; [ ] sample component test.
- **DoD:** Global DoD + AC.