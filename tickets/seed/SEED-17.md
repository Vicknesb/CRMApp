> **Epic context:** EPIC-SEED · Dummy / Demo Data Loading (ON-HOLD · opt-in)

### SEED-17 · Check · Dummy-data module-wide check
- **Points:** 2 **Depends on:** SEED-1…16
- **Description:** Verify a full dummy load across all modules.
- **Acceptance Criteria:**
  - [ ] `seed_dummy.py --module all` populates every module on a migrated DB.
  - [ ] Re-running is idempotent (no duplicates); all key screens have data.
- **Unit Tests:** [ ] integration: migrate → dummy-load → expected counts per module; [ ] idempotency.
- **DoD:** Global DoD + all SEED tickets closed.