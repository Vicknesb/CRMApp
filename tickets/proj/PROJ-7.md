> **Epic context:** EPIC-PROJ · Project & Delivery Management

### PROJ-7 · Story · Jira bidirectional sync
- **Points:** 5 **SRS:** PR-002 **Depends on:** PROJ-5, INTG-4(Jira)
- **Description:** map ProjectTask↔Jira issue; inbound webhook + outbound push; conflict handling.
- **AC:** [ ] create/update syncs both directions.
- **Unit Tests:** [ ] outbound push payload; [ ] inbound webhook apply; [ ] conflict resolution (mock Jira).