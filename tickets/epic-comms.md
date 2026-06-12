# EPIC-COMM · Communication & Collaboration

> **Epic goal:** Unified comms log, notifications + @mentions, Slack/Teams alerts, templates, comment threads. **SRS:** §3.10.
> **Depends on:** EPIC-AUTH, EPIC-INTG(Slack/Teams).

---

### COMM-1 · Story · Schema (Notification, Mention, Comment)
- **Points:** 2 **SRS:** §3.10 **Depends on:** AUTH-1
- **Description:** Notification (user, type, payload, readAt), Mention, Comment (polymorphic entity, body, author). Seed.
- **AC:** [ ] migration + seed.
- **Unit Tests:** [ ] repo CRUD.

### COMM-2 · Task · Schemas (Pydantic/Zod)
- **Points:** 1 **Depends on:** COMM-1
- **AC:** [ ] notification/comment schemas.
- **Unit Tests:** [ ] parse.

### COMM-3 · Story · Unified communication log
- **Points:** 3 **SRS:** §3.10 **Depends on:** COMM-2, ACTV-3
- **AC:** [ ] aggregate email/call/chat/meeting per contact/account.
- **Unit Tests:** [ ] aggregation ordering.

### COMM-4 · Story · In-app notifications + @mention
- **Points:** 3 **SRS:** §3.10 **Depends on:** COMM-2
- **AC:** [ ] notification center; @mention parse → notify.
- **Unit Tests:** [ ] mention parse; [ ] notification create; [ ] mark read.

### COMM-5 · Story · Slack/Teams integration
- **Points:** 3 **SRS:** §6 **Depends on:** COMM-2, INTG-3(Slack/Teams)
- **AC:** [ ] deal/ticket events post to channel; @mentions.
- **Unit Tests:** [ ] event→message payload (mock).

### COMM-6 · Story · Email templates
- **Points:** 2 **SRS:** §3.10 **Depends on:** COMM-2
- **AC:** [ ] sales/support/onboarding templates w/ variable rendering.
- **Unit Tests:** [ ] template var substitution.

### COMM-7 · Story · Comment threads on records
- **Points:** 3 **SRS:** §3.10 **Depends on:** COMM-2
- **AC:** [ ] threaded comments on any record.
- **Unit Tests:** [ ] nested thread; [ ] reply.

### COMM-8 · Task · Frontend hooks
- **Points:** 2 **Depends on:** COMM-3, COMM-4, COMM-7
- **AC:** [ ] `useNotifications/useComments/useMarkRead`.
- **Unit Tests:** [ ] fetch + invalidation.

### COMM-9 · Story · UI: Notification center
- **Points:** 2 **SRS:** §7.1 **Depends on:** COMM-8
- **AC:** [ ] header bell dropdown + unread state.
- **Unit Tests:** [ ] list; [ ] mark read.

### COMM-10 · Story · UI: Comment threads component
- **Points:** 3 **Depends on:** COMM-8, COMM-7
- **AC:** [ ] embeddable threads w/ @mention autocomplete.
- **Unit Tests:** [ ] post/reply; [ ] mention autocomplete.

### COMM-11 · Task · UI: Email template manager
- **Points:** 2 **Depends on:** COMM-8, COMM-6
- **AC:** [ ] CRUD templates w/ preview.
- **Unit Tests:** [ ] preview render.

### COMM-12 · Check · Comms module-wide check
- **Points:** 2 **Depends on:** COMM-1…11
- **AC:** [ ] mention→notify→Slack + comment thread E2E; ≥80% coverage; §3.10 satisfied.
- **Unit Tests:** [ ] integration covering mention→notification→channel post.
