> **Epic context:** EPIC-DB · Database & Schema (Foundational Data Layer)

### DB-1 · Task · Provision PostgreSQL database, roles & extensions
- **Points:** 2 **SRS:** §2.3 **Depends on:** PLAT-3
- **Description:** Create the app database, an app role with least privilege, and required extensions (`uuid-ossp`/`pgcrypto`, `citext` for emails, `pg_trgm` for fuzzy/KB search). Document connection string in `.env.example`.
- **Acceptance Criteria:**
  - [ ] Database + role created; extensions enabled.
  - [ ] `DATABASE_URL` documented; app connects via Prisma.
- **Unit Tests:** [ ] connection smoke test; [ ] extensions present query.
- **DoD:** Global DoD + AC.