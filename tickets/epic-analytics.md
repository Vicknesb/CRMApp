# EPIC-ANLY · Analytics & Reporting

> **Epic goal:** Role dashboards, all 10 pre-built reports, custom report builder, scheduling, exports. **SRS:** §9 (AN-001/002), §7.2.
> **Mockups:** `11-analytics.html`, `01-dashboard.html`. **Depends on:** most module epics (reads their data).

---

### ANLY-1 · Story · Reporting data model / DB views
- **Points:** 3 **SRS:** AN-001 **Depends on:** module schemas
- **AC:** [ ] read-optimized views/materialized aggregates.
- **Unit Tests:** [ ] view returns expected shape.

### ANLY-2 · Story · Role-based dashboard aggregation API
- **Points:** 3 **SRS:** AN-001 (§7.2) **Depends on:** ANLY-1, AUTH-7
- **Description:** `/dashboard?role=` returns role widgets (pipeline summary, my tasks, KPIs).
- **AC:** [ ] each role gets correct widget set.
- **Unit Tests:** [ ] per-role widget composition.

### ANLY-3 · Story · Pre-built reports (all 10 §9.1)
- **Points:** 5 **SRS:** AN-001 **Depends on:** ANLY-1
- **Description:** Pipeline Summary, Lead Conversion Funnel, Revenue Forecast, Rep Performance, Account Health, SLA Compliance, Ticket Volume, Campaign ROI, Contract Renewal Pipeline, Invoice Aging.
- **AC:** [ ] all 10 return correct aggregates.
- **Unit Tests:** [ ] one aggregation test per report (10).

### ANLY-4 · Story · Custom report builder API
- **Points:** 5 **SRS:** §9.2 (AN-001) **Depends on:** ANLY-1
- **Description:** `/reports/run` w/ definition (fields, filters, grouping, sum/avg/count/min/max); field allowlist (no injection).
- **AC:** [ ] arbitrary safe definitions execute.
- **Unit Tests:** [ ] aggregation funcs; [ ] disallowed field rejected; [ ] injection attempt blocked.

### ANLY-5 · Story · Scheduled report delivery
- **Points:** 3 **SRS:** §9.2 **Depends on:** ANLY-3, INTG-2(email)
- **AC:** [ ] schedule daily/weekly/monthly email delivery.
- **Unit Tests:** [ ] schedule fire (frozen clock); [ ] email payload.

### ANLY-6 · Story · Export PDF/Excel/CSV
- **Points:** 3 **SRS:** AN-002 **Depends on:** ANLY-3
- **AC:** [ ] export any report to all three formats.
- **Unit Tests:** [ ] CSV rows; [ ] Excel sheet; [ ] PDF bytes.

### ANLY-7 · Task · Frontend hooks
- **Points:** 2 **Depends on:** ANLY-2, ANLY-3, ANLY-4
- **AC:** [ ] `useDashboard/useReport/useRunReport/useExportReport`.
- **Unit Tests:** [ ] fetch.

### ANLY-8 · Story · UI: Analytics dashboard
- **Points:** 3 **SRS:** AN-001 **Depends on:** ANLY-7
- **AC:** [ ] mirror `11-analytics.html` (4+ charts, filters, drill-down).
- **Unit Tests:** [ ] chart render; [ ] filter; [ ] drill-down.

### ANLY-9 · Story · UI: Role dashboards (home)
- **Points:** 3 **SRS:** §7.2 **Depends on:** ANLY-7, ANLY-2
- **AC:** [ ] mirror `01-dashboard.html`; widgets vary by role.
- **Unit Tests:** [ ] role widget switch.

### ANLY-10 · Story · UI: Custom report builder
- **Points:** 5 **SRS:** §9.2 **Depends on:** ANLY-7, ANLY-4
- **AC:** [ ] drag-drop fields, filters, grouping, run + export.
- **Unit Tests:** [ ] build definition; [ ] run; [ ] export.

### ANLY-11 · Task · Report scheduling UI
- **Points:** 2 **SRS:** §9.2 **Depends on:** ANLY-7, ANLY-5
- **AC:** [ ] schedule config UI.
- **Unit Tests:** [ ] schedule form submit.

### ANLY-12 · Task · Drill-down navigation
- **Points:** 2 **Depends on:** ANLY-8
- **AC:** [ ] chart element → filtered record list.
- **Unit Tests:** [ ] drill route params.

### ANLY-13 · Task · Performance: cache/materialize heavy reports
- **Points:** 2 **SRS:** §5.1 **Depends on:** ANLY-3
- **AC:** [ ] heavy reports cached/materialized; <2s.
- **Unit Tests:** [ ] cache hit path.

### ANLY-14 · Check · Analytics module-wide check
- **Points:** 2 **Depends on:** ANLY-1…13
- **AC:** [ ] dashboards + 10 reports + builder + exports E2E; ≥80% coverage; AN-001/002 satisfied.
- **Unit Tests:** [ ] integration covering dashboard→report→export.
