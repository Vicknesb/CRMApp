> **Epic context:** EPIC-AUTH · Authentication & Access

### AUTH-1 · Story · Identity schema (User, Role, Team, Session, AuditLog)
- **Points:** 3 **SRS:** §2.2/§5.2 **Depends on:** PLAT-3
- **Description:** Prisma models for identity + audit; Role enum = 8 SRS roles; seed one user per role.
- **Acceptance Criteria:** [ ] Migration applies; relations User↔Role/Team, AuditLog→User; seed creates 8 users.
- **Unit Tests:** [ ] repo create/find user; [ ] seed idempotency.
- **DoD:** Global DoD + AC.