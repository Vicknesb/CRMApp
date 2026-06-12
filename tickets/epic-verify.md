# EPIC-VERIFY · UAT, Go-Live & SRS Verification

> **Epic goal:** Prove 100% SRS coverage, pass acceptance criteria, and sign off. **SRS:** §11.
> **Depends on:** ALL other epics' `*-CHECK` tickets closed.

---

### VERIFY-1 · Check · SRS coverage matrix
- **Points:** 5 **SRS:** ALL **Depends on:** every epic `*-CHECK`
- **Description:** Build `COVERAGE_MATRIX.md` mapping every SRS item → epic/ticket → code path → test, with ✅/⚠️/❌ + evidence.
- **Acceptance Criteria:**
  - [ ] Every §3 functional bullet mapped + ✅.
  - [ ] All 23 §4 Req IDs ✅ with file + test evidence.
  - [ ] §5 NFRs, §6 integrations (Must/Should ✅; Nice ⚠️ allowed w/ note), §8 data, §9 reports (all 10 + builder + exports) ✅.
  - [ ] §7.2 key screens all exist.
  - [ ] Zero ❌ rows.
- **Unit Tests:** [ ] automated check that every Req ID appears in the matrix as ✅.

### VERIFY-2 · Check · Full regression + coverage gate
- **Points:** 2 **SRS:** §11.1 **Depends on:** VERIFY-1
- **AC:** [ ] `pytest` + `vitest` green; repo coverage ≥80%; 0 Critical/High bugs.
- **Unit Tests:** [ ] CI run archived as evidence.

### VERIFY-3 · Check · Performance acceptance
- **Points:** 2 **SRS:** §11.2 **Depends on:** NFR-1
- **AC:** [ ] 200 concurrent, page <2s, API P95 <500ms (k6 evidence).
- **Unit Tests:** [ ] load-test report attached.

### VERIFY-4 · Check · Security acceptance
- **Points:** 2 **SRS:** §11.3 **Depends on:** NFR-2
- **AC:** [ ] pen-test no Critical/High; 2FA+RBAC+audit functional; encryption verified.
- **Unit Tests:** [ ] security scan report attached.

### VERIFY-5 · Story · UAT sign-off + documentation
- **Points:** 3 **SRS:** §11.4 **Depends on:** VERIFY-1…4
- **AC:** [ ] signed UAT (Sales/Support/IT leads); training docs + video walkthroughs; helpdesk/runbook handover.
- **Unit Tests:** [ ] UAT checklist completed (all Must-Have demoed).

### VERIFY-6 · Check · Go-Live readiness
- **Points:** 2 **SRS:** §11 **Depends on:** VERIFY-1…5
- **AC:** [ ] all integrations verified end-to-end; migration <0.1% error; backups/DR ready; master tracker all epics ✅.
- **Unit Tests:** [ ] go-live checklist signed.
