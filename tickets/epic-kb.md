# EPIC-KB · Knowledge Base

> **Epic goal:** KB articles, ticket-time suggestions, usage/helpfulness tracking. **SRS:** §3.5.3 (TK-003).
> **Mockup:** `15-knowledge-base.html`. **Depends on:** EPIC-AUTH (suggestions consumed by EPIC-TICK).

---

### KB-1 · Story · KB schema (Article, KbCategory, ArticleRating)
- **Points:** 2 **SRS:** TK-003 **Depends on:** AUTH-1
- **Description:** Article (title, body, category, tags, status, views, helpfulYes/No), category, rating. Seed.
- **AC:** [ ] migration + seed.
- **Unit Tests:** [ ] repo CRUD.

### KB-2 · Task · Schemas (Pydantic/Zod)
- **Points:** 1 **Depends on:** KB-1
- **AC:** [ ] article/rating schemas.
- **Unit Tests:** [ ] parse.

### KB-3 · Story · Article CRUD + search API
- **Points:** 3 **SRS:** TK-003 **Depends on:** KB-2, AUTH-7
- **AC:** [ ] CRUD + full-text search + category filter + RBAC.
- **Unit Tests:** [ ] CRUD; [ ] search match.

### KB-4 · Story · Suggestion engine
- **Points:** 3 **SRS:** TK-003 **Depends on:** KB-3
- **Description:** `/kb/suggest?subject=&category=` ranked suggestions (consumed by ticket form).
- **AC:** [ ] returns ranked suggestions.
- **Unit Tests:** [ ] ranking order; [ ] no-match empty.

### KB-5 · Task · Usage + helpfulness tracking
- **Points:** 2 **SRS:** §3.5.3 **Depends on:** KB-3
- **AC:** [ ] increment views; record helpful yes/no.
- **Unit Tests:** [ ] counters; [ ] rating store.

### KB-6 · Task · Frontend hooks
- **Points:** 1 **Depends on:** KB-3
- **AC:** [ ] `useArticles/useArticle/useKbSuggest/useRateArticle`.
- **Unit Tests:** [ ] fetch.

### KB-7 · Story · UI: KB list + category filters
- **Points:** 3 **SRS:** §7.2 **Depends on:** KB-6
- **AC:** [ ] mirror `15-knowledge-base.html` (filters, ratings, suggested).
- **Unit Tests:** [ ] filter; [ ] render.

### KB-8 · Story · UI: Article editor
- **Points:** 2 **Depends on:** KB-6
- **AC:** [ ] create/edit (rich text); persists.
- **Unit Tests:** [ ] validation; [ ] submit.

### KB-9 · Story · UI: Article view + rating
- **Points:** 2 **Depends on:** KB-6, KB-5
- **AC:** [ ] read view w/ helpful Yes/No + view counter.
- **Unit Tests:** [ ] rating click; [ ] view increment.

### KB-10 · Task · Seed/fixtures
- **Points:** 1 **Depends on:** KB-1
- **AC:** [ ] sample articles seeded.
- **Unit Tests:** [ ] idempotent.

### KB-11 · Check · KB module-wide check
- **Points:** 2 **Depends on:** KB-1…10
- **AC:** [ ] article→suggest-on-ticket→rate E2E; ≥80% coverage; TK-003 satisfied.
- **Unit Tests:** [ ] integration covering create→suggest→rate.
