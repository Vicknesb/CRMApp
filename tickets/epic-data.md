# EPIC-DATA · Data Management & Compliance

> **Epic goal:** Migration wizard, retention/archiving/recycle bin, GDPR/PDPB compliance. **SRS:** §8.
> **Depends on:** module schemas (EPIC-CONT/ACCT/PIPE at minimum), EPIC-AUTH.

---

### DATA-1 · Story · CSV/Excel import engine
- **Points:** 5 **SRS:** §8.1 **Depends on:** CONT-1, ACCT-1, PIPE-1
- **Description:** parse CSV/Excel; field mapping; validation; error report; chunked for 10k+ rows.
- **AC:** [ ] import 10k rows; error report <0.1% (§11).
- **Unit Tests:** [ ] mapping; [ ] row validation; [ ] error aggregation; [ ] large-batch chunking.

### DATA-2 · Story · Legacy API migration (Salesforce/Zoho/HubSpot)
- **Points:** 3 **SRS:** §8.1 **Depends on:** DATA-1, INTG-1
- **AC:** [ ] one-time API import w/ mapping.
- **Unit Tests:** [ ] source→model mapping (mock).

### DATA-3 · Story · UI: Migration wizard
- **Points:** 3 **SRS:** §8.1 **Depends on:** DATA-1
- **AC:** [ ] upload → map fields → validate → import → error report.
- **Unit Tests:** [ ] mapping step; [ ] error display.

### DATA-4 · Story · Soft-delete + recycle bin (30-day)
- **Points:** 3 **SRS:** §8.2 **Depends on:** module schemas
- **AC:** [ ] deleted recoverable 30 days; restore endpoint.
- **Unit Tests:** [ ] soft-delete; [ ] restore; [ ] purge after 30d (frozen clock).

### DATA-5 · Story · Archiving (7-year retention, auto-archive >5yr)
- **Points:** 3 **SRS:** §8.2 **Depends on:** DATA-4
- **AC:** [ ] archive job moves >5yr records; 7yr retention.
- **Unit Tests:** [ ] archive selection (frozen clock).

### DATA-6 · Story · GDPR/PDPB: data export (portability)
- **Points:** 2 **SRS:** §8.3 **Depends on:** AUTH-7
- **AC:** [ ] export all data for a subject on request.
- **Unit Tests:** [ ] export completeness.

### DATA-7 · Story · GDPR/PDPB: erasure / anonymization
- **Points:** 3 **SRS:** §8.3 **Depends on:** AUTH-7, AUTH-8
- **AC:** [ ] anonymize/delete individual records; audit retained.
- **Unit Tests:** [ ] anonymization scrubs PII; [ ] referential integrity.

### DATA-8 · Story · Consent management (marketing opt-in)
- **Points:** 2 **SRS:** §8.3 **Depends on:** CONT-1
- **AC:** [ ] consent flags; opt-in/out tracked; gate marketing sends.
- **Unit Tests:** [ ] consent gate blocks send.

### DATA-9 · Check · Data module-wide check
- **Points:** 2 **Depends on:** DATA-1…8
- **AC:** [ ] migrate→retain→export→erase E2E; ≥80% coverage; §8 satisfied.
- **Unit Tests:** [ ] integration covering import→soft-delete→restore→export→erase.
