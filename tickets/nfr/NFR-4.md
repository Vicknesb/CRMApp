> **Epic context:** EPIC-NFR · Non-Functional & Hardening

### NFR-4 · Story · Scalability (§5.4)
- **Points:** 3 **SRS:** §5.4 **Depends on:** core modules
- **Description:** stateless API, connection pooling, indexing for 10M rows, LB-ready.
- **AC:** [ ] stateless horizontal scale; acceptable 10M-row query plans.
- **Unit Tests:** [ ] no server-side session state; **Perf:** [ ] EXPLAIN on hot queries.