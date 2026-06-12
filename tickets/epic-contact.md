# EPIC-CONT · Contact Management

> **Epic goal:** Contact records, multi-account links, interaction history. **SRS:** §3.2.1 (CO-001/002).
> **Mockups:** `03-contacts.html`, `form-02-contact.html`. **Depends on:** EPIC-AUTH.

---

### CONT-1 · Story · Contact schema (Contact, ContactRole, Interaction)
- **Points:** 3 **SRS:** CO-001/002 **Depends on:** AUTH-1
- **Description:** Contact (name, designation, email, phone, linkedin, timezone), role tags (DecisionMaker/Influencer/EndUser/TechnicalPOC), Interaction; M2M Contact↔Account. Seed.
- **AC:** [ ] migration + seed; M2M works.
- **Unit Tests:** [ ] repo CRUD; [ ] M2M attach.

### CONT-2 · Task · Contact schemas (Pydantic/Zod)
- **Points:** 1 **Depends on:** CONT-1
- **AC:** [ ] create/update/role-tag/interaction schemas used by router+form.
- **Unit Tests:** [ ] valid/invalid parse.

### CONT-3 · Story · Contact CRUD API
- **Points:** 3 **SRS:** CO-001 **Depends on:** CONT-2, AUTH-7
- **AC:** [ ] CRUD + filter/paginate + RBAC + audit + 422.
- **Unit Tests:** [ ] endpoints; [ ] RBAC deny.

### CONT-4 · Story · Multi-account association
- **Points:** 2 **SRS:** CO-002 **Depends on:** CONT-3, ACCT-1
- **Description:** attach/detach accounts; primary flag.
- **AC:** [ ] contact lists across accounts.
- **Unit Tests:** [ ] attach/detach; [ ] primary uniqueness.

### CONT-5 · Task · Interaction/history logging
- **Points:** 2 **SRS:** §3.2.1 **Depends on:** CONT-3
- **AC:** [ ] log calls/emails/notes; `/contacts/:id/interactions` chronological.
- **Unit Tests:** [ ] ordering; [ ] create.

### CONT-6 · Task · Frontend hooks
- **Points:** 2 **Depends on:** CONT-3
- **AC:** [ ] `useContacts/useContact/useCreate/useUpdate/useContactInteractions` + invalidation.
- **Unit Tests:** [ ] fetch + invalidation.

### CONT-7 · Story · UI: Contact list + detail panel
- **Points:** 3 **SRS:** CO-001 **Depends on:** CONT-6
- **Description:** mirror `03-contacts.html` (list + detail, role tags, interaction log).
- **AC:** [ ] list+detail render real data.
- **Unit Tests:** [ ] row render; [ ] detail open.

### CONT-8 · Story · UI: Contact form
- **Points:** 3 **SRS:** CO-001 **Depends on:** CONT-6
- **Description:** mirror `form-02-contact.html` (personal/work/role tags/comm prefs/linked account/completeness %); Cancel→list.
- **AC:** [ ] create/edit persists.
- **Unit Tests:** [ ] validation; [ ] submit mutation.

### CONT-9 · Task · UI: Interaction timeline component
- **Points:** 2 **Depends on:** CONT-6, CONT-5
- **AC:** [ ] timeline renders chronological interactions.
- **Unit Tests:** [ ] renders ordered items.

### CONT-10 · Task · Seed/fixtures
- **Points:** 1 **Depends on:** CONT-1
- **AC:** [ ] realistic contacts seeded.
- **Unit Tests:** [ ] idempotent.

### CONT-11 · Check · Contact module-wide check
- **Points:** 2 **Depends on:** CONT-1…10
- **AC:** [ ] CRUD + multi-account + interactions E2E; ≥80% coverage; CO-001/002 satisfied.
- **Unit Tests:** [ ] integration covering create→associate→log.
