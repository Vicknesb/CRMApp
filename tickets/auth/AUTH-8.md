> **Epic context:** EPIC-AUTH · Authentication & Access

### AUTH-8 · Task · Audit logging service
- **Points:** 2 **SRS:** §5.2 **Depends on:** AUTH-1
- **Description:** `record_audit(actor, action, entity, before, after)`; hook into mutations; never blocks main op.
- **Acceptance Criteria:** [ ] Mutations write audit rows; failures logged not raised.
- **Unit Tests:** [ ] audit row written; [ ] audit failure swallowed.
- **DoD:** Global DoD + AC.