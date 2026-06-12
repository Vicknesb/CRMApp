# EPIC-ACTV · Activity & Task Management

> **Epic goal:** Log activities, manage tasks/reminders, calendar, overdue alerts. **SRS:** §3.4.
> **Mockup:** `14-activities.html`. **Depends on:** EPIC-AUTH (+ CONT/ACCT/PIPE for relations).

---

### ACTV-1 · Story · Activity/Task schema (Activity, Task, Reminder)
- **Points:** 3 **SRS:** §3.4 **Depends on:** AUTH-1
- **Description:** Activity (type call/email/meeting/demo/visit, subject, notes, polymorphic relatedTo, at), Task (title, due, priority, assignee, status), Reminder. Seed.
- **AC:** [ ] migration + seed.
- **Unit Tests:** [ ] repo CRUD; [ ] polymorphic link.

### ACTV-2 · Task · Schemas (Pydantic/Zod)
- **Points:** 1 **Depends on:** ACTV-1
- **AC:** [ ] activity/task/reminder schemas.
- **Unit Tests:** [ ] parse.

### ACTV-3 · Story · Activity logging API
- **Points:** 3 **SRS:** §3.4 **Depends on:** ACTV-2, AUTH-7
- **AC:** [ ] log activities vs contact/account/deal; list by entity; RBAC + audit.
- **Unit Tests:** [ ] create; [ ] entity filter.

### ACTV-4 · Story · Tasks & reminders API
- **Points:** 3 **SRS:** §3.4 **Depends on:** ACTV-2
- **AC:** [ ] task CRUD w/ due/priority/assignee; reminders.
- **Unit Tests:** [ ] CRUD; [ ] assignment.

### ACTV-5 · Story · Calendar feed
- **Points:** 2 **SRS:** §3.4 **Depends on:** ACTV-3, ACTV-4
- **AC:** [ ] `/activities/calendar?range=` aggregates activities+tasks.
- **Unit Tests:** [ ] range query; [ ] boundary dates.

### ACTV-6 · Story · Overdue alerts + completion tracking
- **Points:** 2 **SRS:** §3.4 **Depends on:** ACTV-4
- **AC:** [ ] scheduler flags overdue; completion status.
- **Unit Tests:** [ ] overdue detection (frozen clock); [ ] completion transition.

### ACTV-7 · Task · Frontend hooks
- **Points:** 2 **Depends on:** ACTV-3, ACTV-4
- **AC:** [ ] `useActivities/useTasks/useCalendar/useLogActivity/useCreateTask`.
- **Unit Tests:** [ ] fetch + invalidation.

### ACTV-8 · Story · UI: Activity feed
- **Points:** 2 **SRS:** §7.2 **Depends on:** ACTV-7
- **AC:** [ ] mirror `14-activities.html` feed; overdue alerts banner.
- **Unit Tests:** [ ] feed render; [ ] overdue highlight.

### ACTV-9 · Story · UI: Task board
- **Points:** 2 **Depends on:** ACTV-7
- **AC:** [ ] task list/board w/ priority + status.
- **Unit Tests:** [ ] status change.

### ACTV-10 · Story · UI: Calendar view
- **Points:** 3 **SRS:** §3.4 **Depends on:** ACTV-7, ACTV-5
- **AC:** [ ] month/week calendar of activities+tasks.
- **Unit Tests:** [ ] events render in cells.

### ACTV-11 · Story · UI: Log Activity & New Task modals
- **Points:** 2 **Depends on:** ACTV-7
- **AC:** [ ] modals create activity/task; Cancel closes.
- **Unit Tests:** [ ] validation; [ ] submit.

### ACTV-12 · Check · Activity module-wide check
- **Points:** 2 **Depends on:** ACTV-1…11
- **AC:** [ ] log→task→calendar→overdue E2E; ≥80% coverage; §3.4 satisfied.
- **Unit Tests:** [ ] integration covering log→task→overdue.
