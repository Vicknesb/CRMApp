> **Epic context:** EPIC-SEED · Dummy / Demo Data Loading (ON-HOLD · opt-in)

### SEED-1 · Task · Dummy-data framework & runner
- **Points:** 2 **Depends on:** DB-13
- **Description:** Idempotent loader (`seed_dummy.py`) with a Faker (en_IN locale) helper, deterministic seed,
  per-module toggles, and a single `--module <name>|all` entry point. Safe to re-run (upsert by natural key).
- **Acceptance Criteria:** [ ] runner loads/clears per module; re-run produces no duplicates.
- **Unit Tests:** [ ] idempotency (second run = same row counts); [ ] `--module` selector works.
- **DoD:** Global DoD + AC.