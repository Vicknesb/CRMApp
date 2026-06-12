> **Epic context:** EPIC-NFR · Non-Functional & Hardening

### NFR-1 · Story · Performance (§5.1)
- **Points:** 5 **SRS:** §5.1, §11.2 **Depends on:** core modules
- **Description:** pagination, DB indexes, caching, query tuning; k6 load test (200 users, page <2s, API P95 <500ms, bulk 10k <5min).
- **AC:** [ ] load test meets all §5.1 targets.
- **Unit Tests:** [ ] pagination correctness; [ ] cache hit; **Perf:** [ ] k6 report archived.