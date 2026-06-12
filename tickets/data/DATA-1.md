> **Epic context:** EPIC-DATA · Data Management & Compliance

### DATA-1 · Story · CSV/Excel import engine
- **Points:** 5 **SRS:** §8.1 **Depends on:** CONT-1, ACCT-1, PIPE-1
- **Description:** parse CSV/Excel; field mapping; validation; error report; chunked for 10k+ rows.
- **AC:** [ ] import 10k rows; error report <0.1% (§11).
- **Unit Tests:** [ ] mapping; [ ] row validation; [ ] error aggregation; [ ] large-batch chunking.