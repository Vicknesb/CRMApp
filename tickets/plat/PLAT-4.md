> **Epic context:** EPIC-PLAT · Platform & Infrastructure

### PLAT-4 · Task · React SPA scaffold (Vite + Tailwind + DaisyUI)
- **Points:** 3 **SRS:** §7.1 **Depends on:** PLAT-1
- **Description:** Vite React+TS, Tailwind+DaisyUI lemonade, React Router, TanStack Query, axios apiClient (credentials + envelope unwrap).
- **Acceptance Criteria:**
  - [ ] Themed shell page renders; apiClient unwraps `{data,error}` and normalizes errors.
- **Unit Tests:** [ ] `apiClient` unwraps data + throws normalized error on `error` payload.
- **DoD:** Global DoD + AC.