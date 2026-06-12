> **Epic context:** EPIC-LEAD · Lead Management

### LEAD-1 · Story · Lead schema (Lead, LeadSource, LeadScoreRule)
- **Points:** 3 **SRS:** LM-001 **Depends on:** AUTH-1
- **Description:** Models incl. source enum, UTM fields, status (New/MQL/SQL/Unqualified), score, BANT JSON, owner; scoring rules. Seed varied leads.
- **AC:** [ ] Migration + seed; indexes on email/status/owner.
- **Unit Tests:** [ ] repo CRUD; [ ] seed creates all statuses.