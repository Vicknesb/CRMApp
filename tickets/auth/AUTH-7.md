> **Epic context:** EPIC-AUTH · Authentication & Access

### AUTH-7 · Story · RBAC policy layer (field + record level)
- **Points:** 5 **SRS:** AD-001 **Depends on:** AUTH-4
- **Description:** Central ability map (CRUD per role per module), record-level ownership checks, field-level redaction helper for responses.
- **Acceptance Criteria:** [ ] SalesExec blocked from Admin routes; field redaction hides restricted fields per role.
- **Unit Tests:** [ ] ability matrix allow/deny; [ ] redaction removes restricted fields; [ ] ownership check.
- **DoD:** Global DoD + AC + Req AD-001.