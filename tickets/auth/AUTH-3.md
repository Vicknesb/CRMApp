> **Epic context:** EPIC-AUTH · Authentication & Access

### AUTH-3 · Story · 2FA (TOTP) enrollment + enforcement
- **Points:** 3 **SRS:** §5.2 **Depends on:** AUTH-2
- **Description:** `/auth/2fa/setup` (QR/secret, encrypted), `/auth/2fa/verify`, enforce on login when enabled; backup codes.
- **Acceptance Criteria:** [ ] Authenticator enrollment; login requires valid 6-digit when on.
- **Unit Tests:** [ ] TOTP verify valid/invalid/expired window; [ ] secret encrypted at rest.
- **DoD:** Global DoD + AC.