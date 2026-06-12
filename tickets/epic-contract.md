# EPIC-CONTR · Contract & Renewal Management

> **Epic goal:** Contracts with renewals, versioning, eSignature, amendments. **SRS:** §3.7 (CT-001).
> **Mockups:** `08-contracts.html`, `form-07-contract.html`. **Depends on:** EPIC-AUTH, EPIC-ACCT, EPIC-INTG(eSign).

---

### CONTR-1 · Story · Contract schema (Contract, Amendment, Signature)
- **Points:** 3 **SRS:** CT-001 **Depends on:** AUTH-1, ACCT-1
- **Description:** Contract (dates, value, terms, autoRenew, status), Amendment, Signature (signer, provider, status). Seed varied expiries.
- **AC:** [ ] migration + seed.
- **Unit Tests:** [ ] repo CRUD.

### CONTR-2 · Task · Schemas (Pydantic/Zod)
- **Points:** 1 **Depends on:** CONTR-1
- **AC:** [ ] contract/amendment/signature schemas.
- **Unit Tests:** [ ] parse.

### CONTR-3 · Story · Contract CRUD API (+auto-renew flag)
- **Points:** 3 **SRS:** CT-001 **Depends on:** CONTR-2, AUTH-7
- **AC:** [ ] CRUD + link account/deal + RBAC(AccountMgr/Finance/Admin) + audit.
- **Unit Tests:** [ ] endpoints; [ ] RBAC.

### CONTR-4 · Story · Renewal reminders (90/60/30)
- **Points:** 3 **SRS:** CT-001 **Depends on:** CONTR-3
- **Description:** scheduler emits reminders + notifications at thresholds.
- **AC:** [ ] reminders fire at 90/60/30 days.
- **Unit Tests:** [ ] threshold detection (frozen clock); [ ] no duplicate reminder.

### CONTR-5 · Story · Version history + eSignature
- **Points:** 3 **SRS:** CT-001 (§6) **Depends on:** CONTR-3, INTG-6(eSign)
- **Description:** version snapshots; DocuSign/Zoho Sign workflow + status callback.
- **AC:** [ ] signing request created; callback updates contract.
- **Unit Tests:** [ ] version snapshot; [ ] callback status apply (mock).

### CONTR-6 · Task · Amendments / change orders
- **Points:** 2 **SRS:** §3.7 **Depends on:** CONTR-3
- **AC:** [ ] track amendments/change orders w/ history.
- **Unit Tests:** [ ] ordered history.

### CONTR-7 · Task · Frontend hooks
- **Points:** 2 **Depends on:** CONTR-3
- **AC:** [ ] `useContracts/useContract/useRenewals/useSignContract`.
- **Unit Tests:** [ ] fetch + invalidation.

### CONTR-8 · Story · UI: Contracts table
- **Points:** 2 **SRS:** §7.2 **Depends on:** CONTR-7
- **AC:** [ ] mirror `08-contracts.html`.
- **Unit Tests:** [ ] render; [ ] filter.

### CONTR-9 · Story · UI: Contract form
- **Points:** 3 **SRS:** CT-001 **Depends on:** CONTR-7
- **Description:** mirror `form-07-contract.html` (terms, dates, services checklist, signatories, eSign, renewal alert preview); Cancel→list.
- **AC:** [ ] persists.
- **Unit Tests:** [ ] validation; [ ] submit.

### CONTR-10 · Story · UI: Contract detail + renewal timeline
- **Points:** 3 **Depends on:** CONTR-7, CONTR-5
- **AC:** [ ] version history, amendments, renewal countdown, sign button.
- **Unit Tests:** [ ] timeline render; [ ] sign trigger.

### CONTR-11 · Task · Seed/fixtures
- **Points:** 1 **Depends on:** CONTR-1
- **AC:** [ ] contracts seeded w/ near-expiry samples.
- **Unit Tests:** [ ] idempotent.

### CONTR-12 · Task · UI: Renewal pipeline widget
- **Points:** 2 **SRS:** §9 (Contract Renewal Pipeline) **Depends on:** CONTR-7
- **AC:** [ ] contracts expiring 30/60/90 grouped.
- **Unit Tests:** [ ] bucket grouping.

### CONTR-13 · Check · Contract module-wide check
- **Points:** 2 **Depends on:** CONTR-1…12
- **AC:** [ ] contract→reminder→eSign→amendment E2E; ≥80% coverage; CT-001 satisfied.
- **Unit Tests:** [ ] integration covering create→reminder→sign.
