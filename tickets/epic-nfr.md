# EPIC-NFR · Non-Functional & Hardening

> **Epic goal:** Meet all SRS §5 NFRs + §7.3 mobile/push. Cross-cutting; run alongside/after module epics.
> **SRS:** §5, §7.3. **Depends on:** broad app surface.

---

### NFR-1 · Story · Performance (§5.1)
- **Points:** 5 **SRS:** §5.1, §11.2 **Depends on:** core modules
- **Description:** pagination, DB indexes, caching, query tuning; k6 load test (200 users, page <2s, API P95 <500ms, bulk 10k <5min).
- **AC:** [ ] load test meets all §5.1 targets.
- **Unit Tests:** [ ] pagination correctness; [ ] cache hit; **Perf:** [ ] k6 report archived.

### NFR-2 · Story · Security (§5.2)
- **Points:** 5 **SRS:** §5.2, §11.3 **Depends on:** AUTH epic
- **Description:** AES-256 at rest, TLS 1.3, OWASP Top 10 mitigations, session timeout, audit coverage; dependency + pen-test scan.
- **AC:** [ ] scan no High/Critical; encryption + timeout verified.
- **Unit Tests:** [ ] input sanitization; [ ] authz on each module route; **Sec:** [ ] OWASP checklist evidence.

### NFR-3 · Story · Reliability & availability (§5.3)
- **Points:** 3 **SRS:** §5.3 **Depends on:** PLAT-9
- **Description:** daily backups (30d), DR runbook (RTO 4h/RPO 1h), health monitoring + alerts.
- **AC:** [ ] backup+restore tested; health alerts fire.
- **Unit Tests:** [ ] health endpoint; [ ] backup job invocation.

### NFR-4 · Story · Scalability (§5.4)
- **Points:** 3 **SRS:** §5.4 **Depends on:** core modules
- **Description:** stateless API, connection pooling, indexing for 10M rows, LB-ready.
- **AC:** [ ] stateless horizontal scale; acceptable 10M-row query plans.
- **Unit Tests:** [ ] no server-side session state; **Perf:** [ ] EXPLAIN on hot queries.

### NFR-5 · Story · Usability & accessibility (§5.5, §7)
- **Points:** 3 **SRS:** §5.5, §7.3 **Depends on:** UI epics
- **Description:** responsive 375px+, WCAG 2.1 AA, onboarding wizard + tooltips, ≤3-click rule.
- **AC:** [ ] axe passes AA; onboarding works; 3-click verified.
- **Unit Tests:** [ ] a11y test (axe) on key pages; [ ] responsive snapshot at 375/768/1024.

### NFR-6 · Story · Maintainability (§5.6)
- **Points:** 2 **SRS:** §5.6 **Depends on:** PLAT-8, PLAT-11
- **Description:** ≥80% coverage gate, current Swagger, feature flags, centralized logging.
- **AC:** [ ] repo coverage ≥80%; flags toggle features; `/docs` current.
- **Unit Tests:** [ ] feature flag on/off path.

### NFR-7 · Story · Mobile responsive pass (§7.3)
- **Points:** 3 **SRS:** §7.3 **Depends on:** UI epics
- **AC:** [ ] all pages usable ≥375px; core actions (create/view, log activity, update ticket) on mobile.
- **Unit Tests:** [ ] viewport render tests.

### NFR-8 · Story · Browser push notifications (§7.3)
- **Points:** 3 **SRS:** §7.3 **Depends on:** COMM-4
- **AC:** [ ] push for task reminders + SLA alerts.
- **Unit Tests:** [ ] push trigger on reminder/SLA event (mock).

### NFR-9 · Task · Feature flag system
- **Points:** 2 **SRS:** §5.6 **Depends on:** PLAT-2
- **AC:** [ ] runtime flags gate features.
- **Unit Tests:** [ ] flag eval.

### NFR-10 · Check · NFR module-wide check
- **Points:** 2 **Depends on:** NFR-1…9
- **AC:** [ ] all §5 targets evidenced (load/sec/reliability/scale/usability/maintainability) + §7.3 mobile/push; §11.2/11.3 acceptance met.
- **Unit Tests:** [ ] consolidated NFR evidence report compiled.
