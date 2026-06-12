> **Epic context:** EPIC-DB · Database & Schema (Foundational Data Layer)

### DB-4 · Story · Lead, Contact & Account tables
- **Points:** 5 **SRS:** §3.1, §3.2 **Depends on:** DB-2 · **Covers:** LEAD-1, CONT-1, ACCT-1
- **Description:** `Lead`, `LeadSource`, `LeadScoreRule`; `Contact`, `ContactRole`, `Interaction`, `ContactAccount` (M2M); `Account` (self-relation hierarchy, tier, healthScore).
- **Acceptance Criteria:** [ ] tables + Contact↔Account M2M + Account self-relation; FK Lead→User(owner).
- **Unit Tests:** [ ] M2M attach/detach; [ ] account parent link; [ ] lead FK integrity.
- **DoD:** Global DoD + AC.