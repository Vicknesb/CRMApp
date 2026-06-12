> **Epic context:** EPIC-AUTH · Authentication & Access

### AUTH-4 · Task · Auth dependencies (require_auth / require_role)
- **Points:** 2 **SRS:** §5.2 **Depends on:** AUTH-2
- **Description:** FastAPI dependencies injecting current user; role guard.
- **Acceptance Criteria:** [ ] Protected route 401 without cookie; 403 wrong role.
- **Unit Tests:** [ ] dependency returns user; [ ] role guard allows/denies.
- **DoD:** Global DoD + AC.