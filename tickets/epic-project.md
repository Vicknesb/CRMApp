# EPIC-PROJ · Project & Delivery Management

> **Epic goal:** Projects with phases/milestones, tasks, Jira sync, documents, status reports. **SRS:** §3.6 (PR-001/002).
> **Mockups:** `07-projects.html`, `form-06-project.html`. **Depends on:** EPIC-AUTH, EPIC-ACCT, EPIC-PIPE, EPIC-INTG(Jira).

---

### PROJ-1 · Story · Project schema (Project, Phase, Milestone, ProjectTask, Document)
- **Points:** 5 **SRS:** PR-001 **Depends on:** AUTH-1, ACCT-1
- **Description:** Project (scope, dates, budget, status), Phase, Milestone (targetDate), ProjectTask (assignee, effort), Document. Seed.
- **AC:** [ ] migration + seed w/ phases/milestones.
- **Unit Tests:** [ ] repo CRUD.

### PROJ-2 · Task · Schemas (Pydantic/Zod)
- **Points:** 1 **Depends on:** PROJ-1
- **AC:** [ ] project/phase/milestone/task/document schemas.
- **Unit Tests:** [ ] parse.

### PROJ-3 · Story · Project CRUD API
- **Points:** 3 **SRS:** PR-001 **Depends on:** PROJ-2, AUTH-7
- **AC:** [ ] CRUD + filter + RBAC(ProjectMgr/Admin) + audit.
- **Unit Tests:** [ ] endpoints; [ ] RBAC.

### PROJ-4 · Story · Phases & milestones
- **Points:** 3 **SRS:** PR-001 **Depends on:** PROJ-3
- **AC:** [ ] CRUD phases/milestones w/ target dates + ordering.
- **Unit Tests:** [ ] ordering; [ ] date validation.

### PROJ-5 · Story · Task assignment + effort + status rollup
- **Points:** 3 **SRS:** §3.6 **Depends on:** PROJ-3
- **AC:** [ ] assign tasks w/ effort; project status rolls up.
- **Unit Tests:** [ ] rollup logic; [ ] assignment.

### PROJ-6 · Task · Project status tracking
- **Points:** 2 **SRS:** §3.6 **Depends on:** PROJ-3
- **AC:** [ ] status transitions (NotStarted/InProgress/OnHold/Completed/Delayed); invalid → 422.
- **Unit Tests:** [ ] transition matrix.

### PROJ-7 · Story · Jira bidirectional sync
- **Points:** 5 **SRS:** PR-002 **Depends on:** PROJ-5, INTG-4(Jira)
- **Description:** map ProjectTask↔Jira issue; inbound webhook + outbound push; conflict handling.
- **AC:** [ ] create/update syncs both directions.
- **Unit Tests:** [ ] outbound push payload; [ ] inbound webhook apply; [ ] conflict resolution (mock Jira).

### PROJ-8 · Task · Document management
- **Points:** 2 **SRS:** §3.6 **Depends on:** PROJ-3
- **AC:** [ ] attach SOW/spec/deliverable; list/download.
- **Unit Tests:** [ ] upload + retrieve.

### PROJ-9 · Story · Status report generation (PDF)
- **Points:** 3 **SRS:** §3.6 (AN-002) **Depends on:** PROJ-4
- **AC:** [ ] PDF reflects phases/milestones/status.
- **Unit Tests:** [ ] report data assembly; [ ] PDF byte output.

### PROJ-10 · Task · Frontend hooks
- **Points:** 2 **Depends on:** PROJ-3
- **AC:** [ ] `useProjects/useProject/useMilestones/useProjectTasks/useJiraSync`.
- **Unit Tests:** [ ] fetch + invalidation.

### PROJ-11 · Story · UI: Project list
- **Points:** 2 **SRS:** §7.2 **Depends on:** PROJ-10
- **AC:** [ ] mirror `07-projects.html` (cards, status, value).
- **Unit Tests:** [ ] render; [ ] filter.

### PROJ-12 · Story · UI: Project form
- **Points:** 3 **SRS:** PR-001 **Depends on:** PROJ-10
- **Description:** mirror `form-06-project.html` (basics, timeline/budget, team chips, dynamic milestones, Jira toggle); Cancel→list.
- **AC:** [ ] persists incl. milestones.
- **Unit Tests:** [ ] dynamic milestone rows; [ ] submit.

### PROJ-13 · Story · UI: Project detail (milestones/tasks/docs)
- **Points:** 3 **Depends on:** PROJ-10
- **AC:** [ ] timeline, tasks, documents, status-report button.
- **Unit Tests:** [ ] sections render; [ ] report trigger.

### PROJ-14 · Task · Seed/fixtures
- **Points:** 1 **Depends on:** PROJ-1
- **AC:** [ ] sample projects seeded.
- **Unit Tests:** [ ] idempotent.

### PROJ-15 · Check · Project module-wide check
- **Points:** 2 **Depends on:** PROJ-1…14
- **AC:** [ ] project→milestones→tasks→Jira sync→report E2E; ≥80% coverage; PR-001/002 satisfied.
- **Unit Tests:** [ ] integration covering create→milestone→sync.
