> **Epic context:** EPIC-DB · Database & Schema (Foundational Data Layer)

### DB-7 · Story · Ticketing, SLA & Knowledge Base tables
- **Points:** 5 **SRS:** §3.5 **Depends on:** DB-4 · **Covers:** TICK-1, SLA-1, KB-1
- **Description:** `Ticket` (category, priority, status, channel, account/contact/project FKs, assignee), `TicketNote` (visibility); `SLAPolicy` (priority×tier), `SLATracker` (dues, met/breach); `Article`, `KbCategory`, `ArticleRating`.
- **Acceptance Criteria:** [ ] tables + FKs; SLATracker→Ticket 1:1; KB search index (pg_trgm).
- **Unit Tests:** [ ] ticket FK integrity; [ ] SLATracker uniqueness per ticket; [ ] KB trigram index present.
- **DoD:** Global DoD + AC.