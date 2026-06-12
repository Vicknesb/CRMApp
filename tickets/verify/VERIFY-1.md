> **Epic context:** EPIC-VERIFY · UAT, Go-Live & SRS Verification

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