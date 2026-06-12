# Go-Live Readiness Checklist (VERIFY-6)

> To be signed off by the delivery lead before production deployment.

## Infrastructure
- [ ] PostgreSQL provisioned with connection pooling (PgBouncer recommended)
- [ ] TLS certificates configured (auto-renew via Let's Encrypt or ACM)
- [ ] Environment variables set: `DATABASE_URL`, `JWT_SECRET`, `WEB_ORIGIN`, `SMTP_*`
- [ ] Feature flags reviewed (`FEATURE_*` env vars)
- [ ] Docker images built and pushed to registry
- [ ] Health probes (`/health/live`, `/health/ready`) wired to load-balancer

## Security
- [ ] `JWT_SECRET` rotated (≥ 256-bit random)
- [ ] 2FA enforced for all ADMIN users
- [ ] CORS `allow_origins` restricted to production domain only
- [ ] Integration tokens encrypted at rest (AES-256 key in vault)
- [ ] OWASP scan run (see `reports/security-scan.md`)
- [ ] Penetration test sign-off (NFR-4)

## Database
- [ ] Prisma migrations applied on production DB (`prisma migrate deploy`)
- [ ] Indexes verified (`docs/SCHEMA-SUMMARY.md`)
- [ ] Backup schedule confirmed (daily + WAL archiving)
- [ ] Seed data NOT applied to production (EPIC-SEED is dev/demo only)

## Application
- [ ] Full pytest suite green (`pytest --tb=short -q`)
- [ ] Vitest suite green (`pnpm test`)
- [ ] Coverage ≥ 80% confirmed in CI report
- [ ] All `PROGRESS.md` tickets ticked (266 / 266)
- [ ] OpenAPI `/docs` reviewed — no debug routes exposed

## Monitoring & Alerting
- [ ] Structured logs (structlog JSON) shipping to log aggregator
- [ ] Slow-request alerts wired (> 2 s threshold from `X-Response-Time-Ms`)
- [ ] SLA breach notification channel configured
- [ ] Error rate alert configured (5xx > 1% over 5 min)

## UAT Sign-off
- [ ] UAT test plan executed (§11.4)
- [ ] Lead-to-invoice end-to-end flow verified
- [ ] Ticket/SLA breach escalation verified
- [ ] 2FA login + session timeout verified
- [ ] Data import (CSV) + GDPR erasure verified
- [ ] Stakeholder sign-off obtained (product owner + IT lead)

## Rollback Plan
- [ ] Previous Docker image tagged and available
- [ ] DB snapshot taken immediately before deployment
- [ ] Rollback runbook documented and tested
