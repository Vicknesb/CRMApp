> **Epic context:** EPIC-AUTH · Authentication & Access

### AUTH-9 · Story · SPA auth (login/register/2FA, guard, context)
- **Points:** 3 **SRS:** §5.2 **Depends on:** AUTH-2, PLAT-7
- **Description:** Auth pages (rhf+Zod), `AuthProvider` (via `/auth/session`), `<ProtectedRoute>`, role-based menu visibility, 2FA prompt.
- **Acceptance Criteria:** [ ] Unauthed redirect to /login; role-scoped nav; 2FA flow works.
- **Unit Tests:** [ ] guard redirects unauthed; [ ] login form validation; [ ] 2FA prompt shown when required.
- **DoD:** Global DoD + AC.