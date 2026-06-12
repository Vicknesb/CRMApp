> **Epic context:** EPIC-AUTH · Authentication & Access

### AUTH-10 · Check · Auth module-wide check
- **Points:** 1 **Depends on:** AUTH-1…9
- **Description:** End-to-end auth/RBAC verification.
- **Acceptance Criteria:** [ ] Full register→2FA→login→access→logout flow; RBAC denies cross-role; audit rows present.
- **Unit Tests:** [ ] integration test covering the full flow.
- **DoD:** Global DoD + all AUTH tickets closed; coverage ≥80%.