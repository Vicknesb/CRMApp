> **Epic context:** EPIC-DB · Database & Schema (Foundational Data Layer)

### DB-6 · Story · Activity & Task tables
- **Points:** 3 **SRS:** §3.4 **Depends on:** DB-4 · **Covers:** ACTV-1
- **Description:** `Activity` (polymorphic relatedTo via type+id), `Task` (due/priority/assignee/status), `Reminder`.
- **Acceptance Criteria:** [ ] tables + assignee FK→User; polymorphic columns indexed.
- **Unit Tests:** [ ] task assignment FK; [ ] activity polymorphic index present.
- **DoD:** Global DoD + AC.