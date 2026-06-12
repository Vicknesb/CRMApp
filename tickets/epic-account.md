# EPIC-ACCT · Account Management

> **Epic goal:** Company records, hierarchy, tier, health score, Account 360. **SRS:** §3.2.2 (AC-001/002).
> **Mockups:** `04-accounts.html`, `form-03-account.html`. **Depends on:** EPIC-AUTH.

---

### ACCT-1 · Story · Account schema (+hierarchy, tier, healthScore)
- **Points:** 3 **SRS:** AC-001/002 **Depends on:** AUTH-1
- **Description:** Account (industry, size, location, website, annualRevenue, tier, healthScore, parentId self-relation) + relations to contact/deal/ticket/contract/document. Seed.
- **AC:** [ ] migration + self-relation + seed.
- **Unit Tests:** [ ] repo CRUD; [ ] parent link.

### ACCT-2 · Task · Account schemas (Pydantic/Zod)
- **Points:** 1 **Depends on:** ACCT-1
- **AC:** [ ] create/update/tier/hierarchy schemas.
- **Unit Tests:** [ ] parse valid/invalid.

### ACCT-3 · Story · Account CRUD API
- **Points:** 3 **SRS:** AC-001 **Depends on:** ACCT-2, AUTH-7
- **AC:** [ ] CRUD + filter + RBAC + audit.
- **Unit Tests:** [ ] endpoints; [ ] RBAC.

### ACCT-4 · Task · Tier management
- **Points:** 1 **SRS:** §3.2.2 **Depends on:** ACCT-3
- **AC:** [ ] set tier (Strategic/Enterprise/MidMarket/SMB).
- **Unit Tests:** [ ] invalid tier → 422.

### ACCT-5 · Story · Parent-child hierarchy
- **Points:** 3 **SRS:** AC-001 **Depends on:** ACCT-3
- **Description:** set parent, fetch tree, cycle prevention.
- **AC:** [ ] tree endpoint nested; cycles rejected.
- **Unit Tests:** [ ] tree build; [ ] cycle rejection.

### ACCT-6 · Story · Health score calculation
- **Points:** 3 **SRS:** AC-002 **Depends on:** ACCT-3
- **Description:** score from activity/engagement + open tickets + renewals; scheduled recompute.
- **AC:** [ ] deterministic score.
- **Unit Tests:** [ ] scoring inputs→output; [ ] no-activity edge.

### ACCT-7 · Story · Account 360 aggregation
- **Points:** 3 **SRS:** §7.2 **Depends on:** ACCT-3 (+CONT/PIPE/TICK/CONTR when present)
- **Description:** `/accounts/:id/360` → contacts, deals, tickets, contracts, activities.
- **AC:** [ ] single payload powers 360.
- **Unit Tests:** [ ] aggregation shape.

### ACCT-8 · Task · Frontend hooks
- **Points:** 2 **Depends on:** ACCT-3
- **AC:** [ ] `useAccounts/useAccount/useAccount360/useCreate/useUpdate`.
- **Unit Tests:** [ ] fetch + invalidation.

### ACCT-9 · Story · UI: Account list/cards
- **Points:** 3 **SRS:** AC-001 **Depends on:** ACCT-8
- **Description:** mirror `04-accounts.html` (cards, tier, health).
- **AC:** [ ] renders cards.
- **Unit Tests:** [ ] card render; [ ] filter.

### ACCT-10 · Story · UI: Account form
- **Points:** 3 **SRS:** AC-001 **Depends on:** ACCT-8
- **Description:** mirror `form-03-account.html` (profile, tier radio cards, financials, health); Cancel→list.
- **AC:** [ ] persists.
- **Unit Tests:** [ ] validation; [ ] submit.

### ACCT-11 · Story · UI: Account 360 view
- **Points:** 3 **SRS:** §7.2 **Depends on:** ACCT-8, ACCT-7
- **Description:** full profile w/ contacts/deals/tickets/contracts tabs.
- **AC:** [ ] all relations visible.
- **Unit Tests:** [ ] tab render; [ ] data binding.

### ACCT-12 · Check · Account module-wide check
- **Points:** 2 **Depends on:** ACCT-1…11
- **AC:** [ ] CRUD + hierarchy + health + 360 E2E; ≥80% coverage; AC-001/002 satisfied.
- **Unit Tests:** [ ] integration create→hierarchy→360.
