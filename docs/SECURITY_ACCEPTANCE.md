# Security Acceptance Evidence (VERIFY-4)

> SRS §11.3 / §5.2 — OWASP Top 10 mitigations verified before go-live.

## OWASP Top 10 Checklist

| # | Risk | Mitigation | Status |
|---|------|------------|--------|
| A01 | Broken Access Control | RBAC on every route; field/record-level guards (AUTH-7) | ✅ |
| A02 | Cryptographic Failures | AES-256 at rest for integration tokens; TLS 1.3; httpOnly+SameSite cookies | ✅ |
| A03 | Injection | Prisma parameterized queries; `ALLOWED_MODULES` guard in report builder (ANLY) | ✅ |
| A04 | Insecure Design | Threat model in `docs/ARCHITECTURE.md`; principle of least privilege in RBAC | ✅ |
| A05 | Security Misconfiguration | SecurityHeadersMiddleware: CSP, HSTS, X-Frame-Options, nosniff (NFR-2) | ✅ |
| A06 | Vulnerable Components | `pnpm audit` + `pip-audit` run in CI (PLAT-11) | ✅ |
| A07 | Auth Failures | 2FA TOTP required; 30-min JWT timeout; brute-force lock (AUTH-2, AUTH-3, AUTH-5) | ✅ |
| A08 | Software & Data Integrity | Prisma migrations versioned; no deserialization of untrusted data | ✅ |
| A09 | Logging & Monitoring | Audit log on all mutations (AUTH-8); structlog JSON; slow-request alerts (NFR-1) | ✅ |
| A10 | SSRF | Integration connector URLs validated against allowlist (INTG-1) | ✅ |

## Penetration Test Sign-off
- Scheduled: pre-go-live (coordinate with security team)
- Scope: API endpoints, auth flows, file upload (DATA-1), custom report builder (ANLY)
- Tool: OWASP ZAP automated scan + manual review
- Pass criteria: no High/Critical findings unmitigated

## Dependency Vulnerability Scan
```bash
# Backend
pip-audit -r apps/api/requirements.txt

# Frontend
pnpm audit --audit-level=high
```
Both must exit 0 before deployment.
