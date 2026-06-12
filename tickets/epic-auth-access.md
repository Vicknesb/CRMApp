# EPIC-AUTH · Authentication & Access

> **Epic goal:** Identity model, JWT auth, 2FA, RBAC (incl. field/record-level), and the SPA auth experience.
> **SRS:** §5.2 (security), AD-001 (RBAC), §2.2 (roles). **Priority:** Must. **Depends on:** EPIC-PLAT.

---

### AUTH-1 · Story · Identity schema (User, Role, Team, Session, AuditLog)
- **Points:** 3 **SRS:** §2.2/§5.2 **Depends on:** PLAT-3
- **Description:** Prisma models for identity + audit; Role enum = 8 SRS roles; seed one user per role.
- **Acceptance Criteria:** [ ] Migration applies; relations User↔Role/Team, AuditLog→User; seed creates 8 users.
- **Unit Tests:** [ ] repo create/find user; [ ] seed idempotency.
- **DoD:** Global DoD + AC.

### AUTH-2 · Story · Register / Login / Logout / Session API
- **Points:** 3 **SRS:** §5.2 **Depends on:** AUTH-1
- **Description:** bcrypt hashing; JWT in httpOnly+SameSite cookie; sliding 30-min expiry; `/auth/register|login|logout|session`.
- **Acceptance Criteria:** [ ] Register→login sets cookie; `/auth/session` returns user; logout clears; expired → 401.
- **Unit Tests:** [ ] password hash/verify; [ ] token issue/verify; [ ] `test_login_bad_creds_401`; [ ] expired token → 401.
- **DoD:** Global DoD + AC.

### AUTH-3 · Story · 2FA (TOTP) enrollment + enforcement
- **Points:** 3 **SRS:** §5.2 **Depends on:** AUTH-2
- **Description:** `/auth/2fa/setup` (QR/secret, encrypted), `/auth/2fa/verify`, enforce on login when enabled; backup codes.
- **Acceptance Criteria:** [ ] Authenticator enrollment; login requires valid 6-digit when on.
- **Unit Tests:** [ ] TOTP verify valid/invalid/expired window; [ ] secret encrypted at rest.
- **DoD:** Global DoD + AC.

### AUTH-4 · Task · Auth dependencies (require_auth / require_role)
- **Points:** 2 **SRS:** §5.2 **Depends on:** AUTH-2
- **Description:** FastAPI dependencies injecting current user; role guard.
- **Acceptance Criteria:** [ ] Protected route 401 without cookie; 403 wrong role.
- **Unit Tests:** [ ] dependency returns user; [ ] role guard allows/denies.
- **DoD:** Global DoD + AC.

### AUTH-5 · Task · Session timeout + refresh
- **Points:** 2 **SRS:** §5.2 **Depends on:** AUTH-2
- **Description:** 30-min inactivity timeout, sliding refresh on activity.
- **Acceptance Criteria:** [ ] Inactive 30m → session invalid; activity extends.
- **Unit Tests:** [ ] timeout boundary with frozen clock.
- **DoD:** Global DoD + AC.

### AUTH-6 · Task · Password reset + email verification
- **Points:** 2 **SRS:** §5.2 **Depends on:** AUTH-2, INTG-2(email) [soft]
- **Description:** Token-based reset + verify flows.
- **Acceptance Criteria:** [ ] Reset token single-use, expiring; verify activates.
- **Unit Tests:** [ ] token single-use; [ ] expiry rejected.
- **DoD:** Global DoD + AC.

### AUTH-7 · Story · RBAC policy layer (field + record level)
- **Points:** 5 **SRS:** AD-001 **Depends on:** AUTH-4
- **Description:** Central ability map (CRUD per role per module), record-level ownership checks, field-level redaction helper for responses.
- **Acceptance Criteria:** [ ] SalesExec blocked from Admin routes; field redaction hides restricted fields per role.
- **Unit Tests:** [ ] ability matrix allow/deny; [ ] redaction removes restricted fields; [ ] ownership check.
- **DoD:** Global DoD + AC + Req AD-001.

### AUTH-8 · Task · Audit logging service
- **Points:** 2 **SRS:** §5.2 **Depends on:** AUTH-1
- **Description:** `record_audit(actor, action, entity, before, after)`; hook into mutations; never blocks main op.
- **Acceptance Criteria:** [ ] Mutations write audit rows; failures logged not raised.
- **Unit Tests:** [ ] audit row written; [ ] audit failure swallowed.
- **DoD:** Global DoD + AC.

### AUTH-9 · Story · SPA auth (login/register/2FA, guard, context)
- **Points:** 3 **SRS:** §5.2 **Depends on:** AUTH-2, PLAT-7
- **Description:** Auth pages (rhf+Zod), `AuthProvider` (via `/auth/session`), `<ProtectedRoute>`, role-based menu visibility, 2FA prompt.
- **Acceptance Criteria:** [ ] Unauthed redirect to /login; role-scoped nav; 2FA flow works.
- **Unit Tests:** [ ] guard redirects unauthed; [ ] login form validation; [ ] 2FA prompt shown when required.
- **DoD:** Global DoD + AC.

### AUTH-10 · Check · Auth module-wide check
- **Points:** 1 **Depends on:** AUTH-1…9
- **Description:** End-to-end auth/RBAC verification.
- **Acceptance Criteria:** [ ] Full register→2FA→login→access→logout flow; RBAC denies cross-role; audit rows present.
- **Unit Tests:** [ ] integration test covering the full flow.
- **DoD:** Global DoD + all AUTH tickets closed; coverage ≥80%.
