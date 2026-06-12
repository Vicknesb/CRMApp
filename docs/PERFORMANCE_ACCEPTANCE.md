# Performance Acceptance Evidence (VERIFY-3)

> SRS §11.2 — all responses must be < 2 s at P95 under normal load.

## Test Configuration
- Tool: `locust` (or `k6`)
- Target: staging environment (2 vCPU / 4 GB RAM)
- Duration: 10 minutes ramp-up + 20 minutes steady
- Virtual users: 50 concurrent

## Acceptance Criteria

| Endpoint | P95 Target | Notes |
|----------|-----------|-------|
| `GET /api/v1/leads` (paginated) | < 500 ms | Indexed on `createdAt`, `assignedTo` |
| `POST /api/v1/leads` | < 300 ms | Single write |
| `GET /api/v1/analytics/dashboard` | < 1 500 ms | Aggregates across modules |
| `GET /api/v1/tickets` (with SLA info) | < 700 ms | JOIN with sla_policies |
| `GET /api/v1/invoices/aging` | < 1 000 ms | Date-range aggregation |
| `POST /api/v1/data/import` (500 rows) | < 5 000 ms | Bulk, not P95 bound |

## Slow-Request Monitoring
The `PerformanceMiddleware` (`apps/api/app/middleware/performance.py`) emits a
`slow_request` structured log event when any request exceeds 2 000 ms.
Wire this log to an alert in your observability stack.

## Load-Test Runbook
```bash
pip install locust
locust -f tests/load/locustfile.py --headless -u 50 -r 5 \
       --run-time 30m --host https://crm-staging.example.internal
```
Results are written to `tests/load/results/`. Accept if P95 < 2 000 ms across
all endpoints and error rate < 0.5 %.
