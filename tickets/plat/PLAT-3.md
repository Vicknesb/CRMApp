> **Epic context:** EPIC-PLAT · Platform & Infrastructure

### PLAT-3 · Task · Prisma Client Python + Postgres wiring
- **Points:** 3 **SRS:** §2.3 **Depends on:** PLAT-2
- **Description:** `prisma/schema.prisma` (provider `prisma-client-py`), datasource Postgres, generated client wrapper, connection lifecycle on startup/shutdown.
- **Acceptance Criteria:**
  - [ ] `prisma generate` + `prisma migrate dev` work; client connects on app startup.
  - [ ] `db` dependency injects a connected Prisma client.
- **Unit Tests:** [ ] `test_db_connects`; [ ] migration applies on fresh DB.
- **DoD:** Global DoD + AC.