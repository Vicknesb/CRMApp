> **Epic context:** EPIC-NFR · Non-Functional & Hardening

### NFR-2 · Story · Security (§5.2)
- **Points:** 5 **SRS:** §5.2, §11.3 **Depends on:** AUTH epic
- **Description:** AES-256 at rest, TLS 1.3, OWASP Top 10 mitigations, session timeout, audit coverage; dependency + pen-test scan.
- **AC:** [ ] scan no High/Critical; encryption + timeout verified.
- **Unit Tests:** [ ] input sanitization; [ ] authz on each module route; **Sec:** [ ] OWASP checklist evidence.