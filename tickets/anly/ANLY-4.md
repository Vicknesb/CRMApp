> **Epic context:** EPIC-ANLY · Analytics & Reporting

### ANLY-4 · Story · Custom report builder API
- **Points:** 5 **SRS:** §9.2 (AN-001) **Depends on:** ANLY-1
- **Description:** `/reports/run` w/ definition (fields, filters, grouping, sum/avg/count/min/max); field allowlist (no injection).
- **AC:** [ ] arbitrary safe definitions execute.
- **Unit Tests:** [ ] aggregation funcs; [ ] disallowed field rejected; [ ] injection attempt blocked.