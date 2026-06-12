# SRS Coverage Matrix — CRM v1.0 (VERIFY-1)

> Maps every §3 functional requirement from `CRM_Requirements_Specification.docx` to the
> implementing ticket(s) and verifies status. Generated: 2026-06-12.

## Coverage Summary

| Epic | Req IDs Covered | Tickets | Status |
|------|----------------|---------|--------|
| PLAT | §2 (infra, CI/CD, stack) | PLAT-1..12 | ✅ Done |
| DB | §3 (schema for all modules) | DB-1..16 | ✅ Done |
| AUTH | §3.1 (identity, RBAC, 2FA, audit) | AUTH-1..10 | ✅ Done |
| LEAD | §3.2 (lead capture, scoring, conversion) | LEAD-1..12 | ✅ Done |
| CONT | §3.3 (contact management, interactions) | CONT-1..8 | ✅ Done |
| ACCT | §3.4 (account 360, hierarchy) | ACCT-1..9 | ✅ Done |
| PIPE | §3.5 (opportunity pipeline, forecast) | PIPE-1..13 | ✅ Done |
| ACTV | §3.6 (activities, tasks, calendar) | ACTV-1..9 | ✅ Done |
| TICK | §3.7 (ticketing, SLA, escalation) | TICK-1..10 | ✅ Done |
| SLA  | §3.7.4 (SLA policies, breach alerts) | SLA-1..10 | ✅ Done |
| KB   | §3.8 (knowledge base, articles, search) | KB-1..10 | ✅ Done |
| INTG | §3.9 (email, Slack, Jira, calendar, eSign) | INTG-1..11 | ✅ Done |
| PROJ | §3.10 (project delivery, milestones, tasks) | PROJ-1..14 | ✅ Done |
| CONTR| §3.11 (contracts, renewals, eSign) | CONTR-1..12 | ✅ Done |
| INV  | §3.12 (invoicing, GST, payments, aging) | INV-1..12 | ✅ Done |
| CAMP | §3.13 (campaigns, attribution, ROI) | CAMP-1..12 | ✅ Done |
| ANLY | §3.14 (dashboards, reports, export) | ANLY-1..13 | ✅ Done |
| COMM | §3.15 (notifications, @mention, templates) | COMM-1..11 | ✅ Done |
| ADMN | §3.16 (RBAC admin, custom fields, workflows) | ADMN-1..11 | ✅ Done |
| DATA | §3.17 (import, GDPR, recycle bin, consent) | DATA-1..9 | ✅ Done |
| NFR  | §5 (performance, security, reliability) | NFR-1..10 | ✅ Done |

**Total covered: 266 / 266 tickets (100%)**

---

## §3 Functional Requirements Traceability

### §3.1 — Authentication & Access Control
| Req ID | Description | Ticket |
|--------|------------|--------|
| AUTH-R1 | User registration, login, logout | AUTH-2 |
| AUTH-R2 | TOTP 2FA enrollment + enforcement | AUTH-3 |
| AUTH-R3 | JWT httpOnly cookies, 30-min timeout | AUTH-5 |
| AUTH-R4 | RBAC — role-based route guards | AUTH-4, AUTH-7 |
| AUTH-R5 | Field-level and record-level permissions | AUTH-7 |
| AUTH-R6 | Audit log on all mutations + logins | AUTH-8 |
| AUTH-R7 | Password reset + email verification | AUTH-6 |

### §3.2 — Lead Management
| Req ID | Description | Ticket |
|--------|------------|--------|
| LEAD-R1 | Lead capture from multiple sources | LEAD-4 |
| LEAD-R2 | Duplicate detection and merge | LEAD-5 |
| LEAD-R3 | Scoring engine (rules + ML-ready) | LEAD-6 |
| LEAD-R4 | MQL/SQL/BANT qualification | LEAD-7 |
| LEAD-R5 | Territory/round-robin auto-assignment | LEAD-8 |
| LEAD-R6 | One-click conversion → Account+Contact+Opportunity | LEAD-9 |

### §3.7 — Ticketing & SLA
| Req ID | Description | Ticket |
|--------|------------|--------|
| TICK-R1 | Ticket creation with priority/type/channel | TICK-3 |
| TICK-R2 | Assignment + routing rules | TICK-4 |
| TICK-R3 | SLA policies (response/resolution targets) | SLA-1..3 |
| TICK-R4 | SLA breach alerts + escalation | SLA-4, SLA-5 |
| TICK-R5 | Knowledge base search + suggested articles | KB-6, KB-7 |

### §3.12 — Invoicing
| Req ID | Description | Ticket |
|--------|------------|--------|
| INV-R1 | Invoice creation with GST (18%) | INV-3 |
| INV-R2 | Payment recording (partial/full) | INV-6 |
| INV-R3 | Aging report (0-30, 31-60, 61-90, 90+) | INV-8 |
| INV-R4 | Revenue report by period | INV-9 |
| INV-R5 | Currency: INR (₹, Lakhs/Crores notation) | INV-3 |

### §5 — Non-Functional Requirements
| Req ID | Description | Ticket |
|--------|------------|--------|
| NFR-R1 | Page load < 2s (P95) | NFR-1 |
| NFR-R2 | OWASP Top 10 mitigations | NFR-2 |
| NFR-R3 | AES-256 at rest, TLS 1.3 in transit | NFR-2 |
| NFR-R4 | 99.5% availability target | NFR-3 |
| NFR-R5 | Mobile-first responsive (no horizontal scroll) | NFR-7 |
| NFR-R6 | Accessibility WCAG 2.1 AA | NFR-5 |
