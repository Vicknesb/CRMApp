> **Epic context:** EPIC-DB · Database & Schema (Foundational Data Layer)

### DB-8 · Story · Project & Delivery tables
- **Points:** 3 **SRS:** §3.6 **Depends on:** DB-4 · **Covers:** PROJ-1
- **Description:** `Project` (scope, dates, budget, status, account/deal FKs), `Phase`, `Milestone`, `ProjectTask` (assignee, effort), `Document`.
- **Acceptance Criteria:** [ ] tables + FKs Project→Account/Opportunity; milestone→phase.
- **Unit Tests:** [ ] project FK integrity; [ ] milestone ordering field.
- **DoD:** Global DoD + AC.