> **Epic context:** EPIC-PLAT · Platform & Infrastructure

### PLAT-6 · Task · Error handling + structured logging
- **Points:** 2 **SRS:** §5.6 **Depends on:** PLAT-2
- **Description:** FastAPI exception handlers → envelope; Pydantic validation → 422 with field errors; structlog JSON w/ request id. FE error boundary + toast.
- **Acceptance Criteria:** [ ] Raised errors return envelope; 422 lists invalid fields; logs are JSON.
- **Unit Tests:** [ ] `test_validation_error_returns_422_fields`; [ ] handler maps domain error → status.
- **DoD:** Global DoD + AC.