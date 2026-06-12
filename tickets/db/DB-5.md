> **Epic context:** EPIC-DB · Database & Schema (Foundational Data Layer)

### DB-5 · Story · Opportunity & Pipeline tables
- **Points:** 5 **SRS:** §3.3 **Depends on:** DB-4 · **Covers:** PIPE-1
- **Description:** `Pipeline`, `Stage` (order, probability), `Opportunity` (value, closeDate, serviceType, stage/account/contact FKs), `Product` (catalog), `Proposal`, `Quote`, `QuoteLineItem`, `StageHistory`.
- **Acceptance Criteria:** [ ] tables + FKs to Account/Contact/Stage; proposal/quote→opportunity.
- **Unit Tests:** [ ] opportunity FK integrity; [ ] stage-history append; [ ] quote line-item cascade.
- **DoD:** Global DoD + AC.