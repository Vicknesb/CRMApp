> **Epic context:** EPIC-PLAT · Platform & Infrastructure

### PLAT-9 · Task · Dockerization + docker-compose
- **Points:** 2 **SRS:** §2.3 **Depends on:** PLAT-2, PLAT-4
- **Description:** Multi-stage Dockerfiles (api, web) + compose with postgres + volumes + env.
- **Acceptance Criteria:** [ ] `docker compose up` serves api+web+db on localhost.
- **Unit Tests:** [ ] compose config validates (`docker compose config`).
- **DoD:** Global DoD + AC.