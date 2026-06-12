# CRM Review Findings Log

> Append-only audit trail of every post-commit review by the `crm-reviewer` agent.
> Newest entry is added directly under this header (latest on top). One entry per task commit.
> Each entry ends with a **Review completed: ✅ <timestamp>** line, so you can see exactly
> when each commit's review was done as new entries arrive.
>
> Entry format:
> ```
> ## Review #<N> · <YYYY-MM-DD HH:MM:SS> · <commit hash> · <ticket id>
> **Verdict:** <✅ PASS | ⚠️ CHANGES-NEEDED>
> Critical / High / Medium findings (file:line → fix)
> Tests: …   SRS: …
> **Review completed:** ✅ <YYYY-MM-DD HH:MM:SS>
> ---
> ```

<!-- New review entries are inserted below this line (newest first) -->

## Review #1 · 2026-06-12 08:58:46 · 232cfb1 · GROUP4
**Verdict:** ⚠️ CHANGES-NEEDED

Critical:
- apps/api/app/modules/contact/service.py:57–67 (log_interaction) — Missing audit log on interaction creation. Every mutation must call `await record_audit(db, actor_id, "CREATE", "interactions", record_id=interaction.id)` per SRS §5.2. → Add audit log after interaction.create().
- apps/api/app/modules/contact/service.py:77–84 (link_account) — Missing audit trail: function lacks actor_id parameter and record_audit call. Linking contact→account is a mutation requiring audit. → Add actor_id parameter to signature, pass it from router (line 65), call `await record_audit(db, actor_id, "LINK", "contactaccounts", record_id=...)` after upsert.
- apps/api/app/modules/lead/service.py:144 — Non-Pythonic `__import__("datetime").datetime.utcnow()`. Inconsistent with line 127 import. → Replace with `datetime.utcnow()` (import datetime at module top).

High:
- apps/api/tests/test_accounts.py:35 — Test HTTP method mismatch: test expects GET but apps/api/app/modules/account/router.py:53 defines POST for health-score endpoint. → Change test line 35 from `.get()` to `.post()`.

Tests: Present (5 modules, 22 test cases), basic coverage ≥50% estimated. SRS traceability: Tests exist but lack edge cases (empty result sets, not-found errors return 404, invalid actor permissions). Recommend expanding test coverage for RBAC enforcement and boundary conditions before merge.

**Review completed:** ✅ 2026-06-12 08:58:46
---
## Review Output

**Verdict: ⚠️ CHANGES-NEEDED**

**Critical findings:**

1. **Scope mismatch (KB-10):** AC requires "sample articles seeded" (backend seed data). Commit delivers only frontend API wrapper code (`kbApi.ts`, `useKb.ts`). No backend seed script or test fixtures. → Add `apps/api/prisma/seed.py` or migration to populate sample KB articles.

2. **No unit tests:** AC requires "idempotent" tests. Zero tests in commit. → Add seed idempotency tests in backend + frontend hook tests.

**High findings:**

3. **API envelope mismatch** (apps/web/src/features/kb/api/kbApi.ts:16–25): Return type signatures don't follow standard `{data, error, meta}` envelope. `list()` returns `Promise<{data: Article[]; meta: ...}>` but should match envelope structure. → Align with apiClient response wrapper or unwrap in hooks.

**Tests:** None present. **SRS ref:** §3.4 Knowledge Base (seed data required for demos/testing).

---

**Attempting to append to review-findings.md...**
