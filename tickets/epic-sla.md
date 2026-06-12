# EPIC-SLA · SLA Management

> **Epic goal:** SLA policies, response/resolution tracking, escalation, compliance reports. **SRS:** §3.5.2 (TK-002).
> **Depends on:** EPIC-TICK.

---

### SLA-1 · Story · SLA schema (SLAPolicy, SLATracker)
- **Points:** 3 **SRS:** TK-002 **Depends on:** TICK-1
- **Description:** SLAPolicy (priority, clientTier, responseMins, resolutionMins), SLATracker (ticketId, dues, met flags, breached). Seed per priority×tier.
- **AC:** [ ] migration + seeded policy matrix.
- **Unit Tests:** [ ] repo CRUD.

### SLA-2 · Task · Schemas (Pydantic/Zod)
- **Points:** 1 **Depends on:** SLA-1
- **AC:** [ ] policy schema.
- **Unit Tests:** [ ] parse.

### SLA-3 · Task · SLA policy CRUD API
- **Points:** 2 **SRS:** TK-002 **Depends on:** SLA-2, AUTH-7
- **AC:** [ ] admin CRUD; RBAC(Admin).
- **Unit Tests:** [ ] CRUD; [ ] RBAC deny.

### SLA-4 · Story · Response/resolution tracking
- **Points:** 3 **SRS:** TK-002 **Depends on:** SLA-1, TICK-3
- **Description:** on ticket create compute dues from matching policy; mark met/breached on updates.
- **AC:** [ ] tracker created w/ correct dues.
- **Unit Tests:** [ ] due calc per priority/tier; [ ] met/breach flagging.

### SLA-5 · Story · Escalation engine
- **Points:** 3 **SRS:** TK-002 **Depends on:** SLA-4
- **Description:** scheduler scans approaching/breached SLAs → escalate/notify.
- **AC:** [ ] approaching breach triggers escalation event.
- **Unit Tests:** [ ] escalation threshold (frozen clock); [ ] no double-escalate.

### SLA-6 · Story · SLA compliance reports
- **Points:** 2 **SRS:** §9 (AN-001) **Depends on:** SLA-4
- **AC:** [ ] `/sla/compliance` met/breached by priority & client/team.
- **Unit Tests:** [ ] aggregation counts.

### SLA-7 · Task · Frontend hooks
- **Points:** 1 **Depends on:** SLA-3, SLA-6
- **AC:** [ ] `useSlaPolicies/useSlaCompliance`.
- **Unit Tests:** [ ] fetch.

### SLA-8 · Story · UI: SLA config (admin)
- **Points:** 2 **SRS:** TK-002 **Depends on:** SLA-7
- **AC:** [ ] policy matrix editor; persists.
- **Unit Tests:** [ ] edit submit.

### SLA-9 · Story · UI: SLA countdown in ticket
- **Points:** 2 **Depends on:** SLA-7, TICK-9
- **AC:** [ ] live countdown + breach state on queue/detail.
- **Unit Tests:** [ ] timer reflects dues; [ ] breach styling.

### SLA-10 · Task · UI: SLA compliance report view
- **Points:** 2 **Depends on:** SLA-7, SLA-6
- **AC:** [ ] chart met/breached by priority/client.
- **Unit Tests:** [ ] chart binds data.

### SLA-11 · Check · SLA module-wide check
- **Points:** 2 **Depends on:** SLA-1…10
- **AC:** [ ] ticket→SLA track→escalate→report E2E; ≥80% coverage; TK-002 satisfied.
- **Unit Tests:** [ ] integration covering create→breach→escalate.
