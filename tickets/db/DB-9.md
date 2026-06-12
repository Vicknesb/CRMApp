> **Epic context:** EPIC-DB · Database & Schema (Foundational Data Layer)

### DB-9 · Story · Contract & Invoicing tables
- **Points:** 3 **SRS:** §3.7, §3.8 **Depends on:** DB-4, DB-5 · **Covers:** CONTR-1, INV-1
- **Description:** `Contract` (dates, value, terms, autoRenew, status), `Amendment`, `Signature`; `Invoice` (number, status, currency, totals, dueDate, account/contract/deal FKs), `InvoiceLineItem`, `Payment`.
- **Acceptance Criteria:** [ ] tables + FKs; invoice→contract/deal; line-item & payment cascade.
- **Unit Tests:** [ ] invoice FK integrity; [ ] line-item cascade delete; [ ] contract amendment link.
- **DoD:** Global DoD + AC.