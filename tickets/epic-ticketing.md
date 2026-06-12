# EPIC-TICK · Service Ticketing

> **Epic goal:** Multi-channel ticket creation, categorization, internal/customer notes. **SRS:** §3.5.1 (TK-001).
> **Mockups:** `06-tickets.html`, `form-05-ticket.html`. **Depends on:** EPIC-AUTH, EPIC-ACCT, EPIC-CONT.

---

### TICK-1 · Story · Ticket schema (Ticket, Category, Priority, TicketNote)
- **Points:** 3 **SRS:** TK-001 **Depends on:** AUTH-1, ACCT-1, CONT-1
- **Description:** Ticket (subject, desc, category, priority, status, channel, account/contact/project links, assignee), TicketNote (body, visibility, author). Seed.
- **AC:** [ ] migration + seed across categories/priorities.
- **Unit Tests:** [ ] repo CRUD.

### TICK-2 · Task · Schemas (Pydantic/Zod)
- **Points:** 1 **Depends on:** TICK-1
- **AC:** [ ] create/update/note schemas.
- **Unit Tests:** [ ] parse.

### TICK-3 · Story · Ticket CRUD API (multi-channel)
- **Points:** 3 **SRS:** TK-001 **Depends on:** TICK-2, AUTH-7
- **Description:** create from email/portal/phone/manual (capture channel); filter/paginate; RBAC(Support/Admin); audit.
- **AC:** [ ] create via each channel; CRUD + 422.
- **Unit Tests:** [ ] per-channel create; [ ] RBAC.

### TICK-4 · Task · Categorization, priority, linking
- **Points:** 2 **SRS:** §3.5.1 **Depends on:** TICK-3
- **AC:** [ ] set category/priority; link account/contact/project.
- **Unit Tests:** [ ] invalid link → 422.

### TICK-5 · Story · Internal/customer notes
- **Points:** 2 **SRS:** §3.5.1 **Depends on:** TICK-3
- **AC:** [ ] notes w/ visibility; customer view filters internal.
- **Unit Tests:** [ ] visibility enforcement.

### TICK-6 · Task · Frontend hooks
- **Points:** 2 **Depends on:** TICK-3
- **AC:** [ ] `useTickets/useTicket/useCreateTicket/useUpdateTicket/useTicketNotes`.
- **Unit Tests:** [ ] fetch + invalidation.

### TICK-7 · Story · UI: Ticket queue
- **Points:** 3 **SRS:** §7.2 **Depends on:** TICK-6
- **AC:** [ ] mirror `06-tickets.html` (filters, priority flags, SLA countdown slot).
- **Unit Tests:** [ ] filter; [ ] row render.

### TICK-8 · Story · UI: Ticket form
- **Points:** 3 **SRS:** TK-001 **Depends on:** TICK-6, KB-4
- **Description:** mirror `form-05-ticket.html` (P1–P4 cards w/ SLA times, category, KB suggestions, attachments); Cancel→queue.
- **AC:** [ ] persists; shows KB suggestions.
- **Unit Tests:** [ ] validation; [ ] suggestion fetch.

### TICK-9 · Story · UI: Ticket detail
- **Points:** 3 **Depends on:** TICK-6, TICK-5
- **AC:** [ ] conversation w/ internal+customer notes, status, links, SLA timer.
- **Unit Tests:** [ ] note post; [ ] status update.

### TICK-10 · Task · Seed/fixtures
- **Points:** 1 **Depends on:** TICK-1
- **AC:** [ ] realistic tickets seeded.
- **Unit Tests:** [ ] idempotent.

### TICK-11 · Check · Ticketing module-wide check
- **Points:** 2 **Depends on:** TICK-1…10
- **AC:** [ ] multi-channel create→notes→resolve E2E; ≥80% coverage; TK-001 satisfied.
- **Unit Tests:** [ ] integration covering create→note→close.
