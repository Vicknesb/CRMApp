> **Epic context:** EPIC-PLAT · Platform & Infrastructure

### PLAT-2 · Task · FastAPI scaffold (layered)
- **Points:** 3 **SRS:** §2.3 **Depends on:** PLAT-1
- **Description:** FastAPI app with `core/`, `db/`, `middleware/`, `modules/` layout, config via Pydantic Settings, `/health`, and **CORS** configured for the SPA origin with credentials.
- **Acceptance Criteria:**
  - [ ] `app/main.py` boots; `GET /health` → `{data:{status:"ok"},error:null}`.
  - [ ] Response-envelope helpers; settings loaded + validated from env.
  - [ ] **CORS middleware** enabled: allowed origin = the SPA URL (env `WEB_ORIGIN`, e.g. `http://localhost:5173`), `allow_credentials=True`, sensible allowed methods/headers — so the browser sends/accepts the httpOnly auth cookie cross-origin.
- **Unit Tests:** [ ] `test_health_ok`; [ ] envelope helper shapes `data/error/meta`; [ ] **CORS preflight (`OPTIONS`) returns the SPA origin in `Access-Control-Allow-Origin` with `Access-Control-Allow-Credentials: true`; a disallowed origin is rejected.**
- **DoD:** Global DoD + AC.