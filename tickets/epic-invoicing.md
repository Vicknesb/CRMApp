# EPIC-INV · Invoicing & Revenue Tracking

> **Epic goal:** Invoices from deals/contracts, payment status, accounting sync, revenue + multi-currency. **SRS:** §3.8 (IN-001/002).
> **Mockups:** `09-invoicing.html`, `form-08-invoice.html`. **Depends on:** EPIC-AUTH, EPIC-PIPE, EPIC-CONTR, EPIC-INTG(accounting).

---

### INV-1 · Story · Invoice schema (Invoice, LineItem, Payment)
- **Points:** 3 **SRS:** IN-001 **Depends on:** AUTH-1, ACCT-1
- **Description:** Invoice (number, links, status, currency, subtotal, tax, total, dueDate), LineItem, Payment. Seed across statuses.
- **AC:** [ ] migration + seed.
- **Unit Tests:** [ ] repo CRUD.

### INV-2 · Task · Schemas (Pydantic/Zod)
- **Points:** 1 **Depends on:** INV-1
- **AC:** [ ] invoice/lineitem/payment schemas.
- **Unit Tests:** [ ] parse.

### INV-3 · Story · Invoice generation from deals/contracts
- **Points:** 3 **SRS:** IN-001 **Depends on:** INV-2, AUTH-7
- **Description:** build line items, compute GST/tax + total; CRUD + RBAC(Finance/Admin) + audit.
- **AC:** [ ] invoice generated w/ correct totals.
- **Unit Tests:** [ ] tax/total calc; [ ] generation from deal + from contract.

### INV-4 · Story · Payment status tracking
- **Points:** 2 **SRS:** §3.8 **Depends on:** INV-3
- **AC:** [ ] transitions Draft→Sent→Paid/Overdue/Cancelled; overdue scheduler auto-flags.
- **Unit Tests:** [ ] transition validation; [ ] overdue detection (frozen clock).

### INV-5 · Story · Revenue recognition + multi-currency
- **Points:** 3 **SRS:** §3.8 (AN-001) **Depends on:** INV-3
- **AC:** [ ] revenue by month/quarter/year; currency conversion w/ rates.
- **Unit Tests:** [ ] revenue grouping; [ ] FX conversion.

### INV-6 · Story · Accounting integration (Zoho/QuickBooks)
- **Points:** 3 **SRS:** IN-002 (§6) **Depends on:** INV-3, INTG-5(accounting)
- **AC:** [ ] invoice syncs; payment status reflected.
- **Unit Tests:** [ ] sync payload; [ ] status callback (mock).

### INV-7 · Task · Frontend hooks
- **Points:** 2 **Depends on:** INV-3
- **AC:** [ ] `useInvoices/useInvoice/useCreateInvoice/useRecordPayment`.
- **Unit Tests:** [ ] fetch + invalidation.

### INV-8 · Story · UI: Invoice list
- **Points:** 2 **SRS:** §7.2 **Depends on:** INV-7
- **AC:** [ ] mirror `09-invoicing.html` (table, status).
- **Unit Tests:** [ ] render; [ ] filter.

### INV-9 · Story · UI: Invoice form (line items + GST)
- **Points:** 3 **SRS:** IN-001 **Depends on:** INV-7
- **Description:** mirror `form-08-invoice.html` (header, line items table, GST 18%, totals); Cancel→list.
- **AC:** [ ] live totals compute.
- **Unit Tests:** [ ] line item math; [ ] GST; [ ] submit.

### INV-10 · Story · UI: Invoice detail / PDF + record payment
- **Points:** 3 **SRS:** AN-002 **Depends on:** INV-7, INV-4
- **AC:** [ ] view + export PDF; record payment.
- **Unit Tests:** [ ] PDF output; [ ] payment record.

### INV-11 · Task · UI: Invoice aging report
- **Points:** 2 **SRS:** §9 (Invoice Aging) **Depends on:** INV-7
- **AC:** [ ] outstanding by age bucket.
- **Unit Tests:** [ ] bucket calc.

### INV-12 · Task · Seed/fixtures
- **Points:** 1 **Depends on:** INV-1
- **AC:** [ ] invoices seeded across statuses.
- **Unit Tests:** [ ] idempotent.

### INV-13 · Check · Invoicing module-wide check
- **Points:** 2 **Depends on:** INV-1…12
- **AC:** [ ] generate→pay→sync→revenue E2E; ≥80% coverage; IN-001/002 satisfied.
- **Unit Tests:** [ ] integration covering generate→pay→aging.
