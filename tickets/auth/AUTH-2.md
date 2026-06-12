> **Epic context:** EPIC-AUTH · Authentication & Access

### AUTH-2 · Story · Register / Login / Logout / Session API
- **Points:** 3 **SRS:** §5.2 **Depends on:** AUTH-1
- **Description:** bcrypt hashing; JWT in httpOnly+SameSite cookie; sliding 30-min expiry; `/auth/register|login|logout|session`.
- **Acceptance Criteria:** [ ] Register→login sets cookie; `/auth/session` returns user; logout clears; expired → 401.
- **Unit Tests:** [ ] password hash/verify; [ ] token issue/verify; [ ] `test_login_bad_creds_401`; [ ] expired token → 401.
- **DoD:** Global DoD + AC.