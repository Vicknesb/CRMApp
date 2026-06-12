> **Epic context:** EPIC-PLAT · Platform & Infrastructure

### PLAT-11 · Task · CI/CD pipeline
- **Points:** 3 **SRS:** §2.3/§5.2/§11 **Depends on:** PLAT-8
- **Description:** GitHub Actions: install → lint → typecheck → pytest (Postgres service) → vitest → build → security (`pip-audit`/`pnpm audit` + secret scan) → deploy gate.
- **Acceptance Criteria:** [ ] PR runs full pipeline; coverage <80% or High vuln fails build.
- **Unit Tests:** [ ] pipeline green on a trivial PR (meta-validation).
- **DoD:** Global DoD + AC.