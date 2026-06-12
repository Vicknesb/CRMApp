> **Epic context:** EPIC-DB · Database & Schema (Foundational Data Layer)

### DB-3 · Story · Identity & access tables
- **Points:** 3 **SRS:** §2.2, §5.2, AD-001 **Depends on:** DB-2 · **Covers:** AUTH-1, ADMN-1(perm)
- **Description:** `User`, `Role`, `Team`, `Session`, `AuditLog`, `Permission` (role/module/action/fieldRules), `TwoFactorSecret`.
- **Acceptance Criteria:** [ ] tables created; relations User↔Role/Team, AuditLog→User; unique email (citext).
- **Unit Tests:** [ ] create/read User; [ ] unique-email constraint; [ ] cascade on Session delete.
- **DoD:** Global DoD + AC.