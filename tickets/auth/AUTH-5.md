> **Epic context:** EPIC-AUTH · Authentication & Access

### AUTH-5 · Task · Session timeout + refresh
- **Points:** 2 **SRS:** §5.2 **Depends on:** AUTH-2
- **Description:** 30-min inactivity timeout, sliding refresh on activity.
- **Acceptance Criteria:** [ ] Inactive 30m → session invalid; activity extends.
- **Unit Tests:** [ ] timeout boundary with frozen clock.
- **DoD:** Global DoD + AC.