# Claude Code Features — CRM Project

> Last updated: 2026-06-11

---

## ✅ Implemented Features

### CLAUDE.md
**Where:** `CLAUDE.md`
Auto-loaded rulebook every session — stack, conventions, scope, Definition of Done.

### Subagents
**Where:** `.claude/agents/`
4 agents: `epic-implementer`, `epic-implementer-auth`, `epic-implementer-nfr`, `crm-reviewer`.

### Per-agent model
**Where:** Agent frontmatter
`claude-sonnet-4-6` for implementation agents, `claude-haiku-4-5` for the reviewer.

### `effort: high`
**Where:** `epic-implementer-auth.md`, `epic-implementer-nfr.md`
Deep API-level reasoning for security-critical (AUTH) and compliance (NFR) tickets.

### `maxTurns: 80`
**Where:** All 3 implementer agents
Caps each epic run at 80 tool calls — prevents runaway token spend on stuck epics.

### `isolation: worktree`
**Where:** All 3 implementer agents
Each epic runs in a throwaway git branch — main stays clean until all tests pass.

### `background: true`
**Where:** `crm-reviewer.md`
Reviewer runs non-blocking — implementer continues to next ticket immediately after commit.

### `permissionMode: acceptEdits`
**Where:** `crm-reviewer.md`
Reviewer appends to review log without prompting for approval on every write.

### `disallowedTools: [Edit, MultiEdit]`
**Where:** `crm-reviewer.md`
Permanently blocks the reviewer from making in-place edits to any source file.

### `initialPrompt`
**Where:** All 3 implementer agents
Auto-loads `AGENT-CONTEXT.md` + `PROGRESS.md` before every agent run — no manual priming needed.

### `permissions.allow`
**Where:** `.claude/settings.json`
Bash restricted to: `pytest`, `vitest`, and read-only git commands only.

### `permissions.deny`
**Where:** `.claude/settings.json`
Blocks: `rm`, `rmdir`, `del`, `git reset --hard`, force push, `git clean`, `git rebase`,
`prisma migrate reset`, raw SQL drops (`DROP TABLE`, `TRUNCATE`, `DELETE FROM`).

### PreToolUse hook — schema.prisma guard
**Where:** `.claude/settings.json` + `.claude/hooks/guard-schema-prisma.ps1`
Blocks `Edit`/`Write`/`MultiEdit` on `schema.prisma` outside EPIC-DB.
Fails open on hook error so a bug never silently blocks work.

### PostToolUse hook — auto-commit
**Where:** `.claude/settings.json` + `.claude/hooks/commit-on-task-complete.ps1`
Auto-commits the repo when `PROGRESS.md` is saved with a newly checked `[x]` ticket.

### PostToolUse hook — inline reviewer agent
**Where:** `.claude/settings.json`
Fires `crm-reviewer` (Haiku) automatically after every `PROGRESS.md` save.
Uses `"if": "Edit(**/PROGRESS.md)"` so it only triggers on that one file, not every write.

### MCP servers
**Where:** `.mcp.json`
PostgreSQL + GitHub MCP configured with `${ENV_VAR}` placeholders.
Activate by setting env vars and running `/mcp` to approve.

### UI mockup reading — step 2b
**Where:** `epic-implementer.md` Phase B
Agent reads the relevant HTML mockup before building any React UI.
Enforces brand green `#507d2a`, DaisyUI lemonade theme, sidebar layout, table styles, field labels.

### Deep reasoning step — step 3b
**Where:** `epic-implementer.md` Phase B
Extended internal reasoning triggered for `LEAD-6`, `SLA-5`, `ANLY-4`, and any ticket
whose title contains: engine, builder, scheduler, rule, algorithm.

### Slim context file
**Where:** `AGENT-CONTEXT.md`, loaded via `initialPrompt`
80-line context loaded instead of the full `CLAUDE.md` — ~83% token saving per ticket.

### Per-ticket files
**Where:** `tickets/<prefix>/<TICKET-ID>.md`
Agent loads only the one ticket being implemented — not the entire epic file.

---

## 🔲 Available — Not Yet Used

### Custom slash commands
**How:** Add `.claude/commands/<name>.md`
`/crm:next` — find next unblocked ticket, `/crm:status` — PROGRESS summary,
`/crm:unblock` — list blocked tickets and their missing dependencies.

### Stop hooks
**How:** Add `"Stop"` hook in `.claude/settings.json`
Fires when an agent finishes its run — use for desktop notifications or auto-open coverage report.

### `skills` frontmatter
**How:** Add `skills: [claude-api]` to an agent
Preload the `claude-api` skill into `epic-implementer-auth` for INTG tickets calling external APIs.

### `mcpServers` frontmatter
**How:** Add `mcpServers: [postgres]` to an agent
Scope MCP servers per agent — give implementer live DB access, keep reviewer read-only.

### `memory` frontmatter
**How:** Add `memory:` scope to agent frontmatter
Restrict implementer agents to project memory files only.

### `color` frontmatter
**How:** Add `color: green` / `color: orange` to agent frontmatter
Visual distinction in the Claude Code UI — implementer green, reviewer orange.

### Task budget
**How:** `output_config: {task_budget: {type: "tokens", total: N}}` — Opus 4.7+ only
Hard token ceiling per epic run. Requires upgrading model from `claude-sonnet-4-6` to Opus 4.7+.

---

## Agents

### `epic-implementer`
**File:** `.claude/agents/epic-implementer.md`
**Model:** `claude-sonnet-4-6` · **maxTurns:** 80 · **isolation:** worktree
**Tools:** Read, Write, Edit, Glob, Grep, Bash
**Invoked by:** `Implement EPIC-<KEY>` (full epic) or `Implement <TICKET-ID>` (single ticket)
Implements all CRM epics except AUTH and NFR. Runs in a throwaway git worktree so main stays
clean until all tests pass. Auto-loads `AGENT-CONTEXT.md` + `PROGRESS.md` via `initialPrompt`.
Reads HTML mockups before building React UI (step 2b). Deep reasoning for complex tickets (step 3b).

### `epic-implementer-auth`
**File:** `.claude/agents/epic-implementer-auth.md`
**Model:** `claude-sonnet-4-6` · **effort:** high · **maxTurns:** 80 · **isolation:** worktree
**Tools:** Read, Write, Edit, Glob, Grep, Bash
**Invoked by:** `Implement EPIC-AUTH` or `Implement AUTH-<N>`
Handles EPIC-AUTH only. `effort: high` enables deep API-level reasoning for security-critical code.
Enforces non-negotiable AUTH rules: JWT in httpOnly cookies, bcrypt ≥ 12, TOTP on every login,
RBAC deny tests, audit log assertions. Deep reasoning gate fires on every AUTH ticket.

### `epic-implementer-nfr`
**File:** `.claude/agents/epic-implementer-nfr.md`
**Model:** `claude-sonnet-4-6` · **effort:** high · **maxTurns:** 80 · **isolation:** worktree
**Tools:** Read, Write, Edit, Glob, Grep, Bash
**Invoked by:** `Implement EPIC-NFR` or `Implement NFR-<N>`
Handles EPIC-NFR only. `effort: high` for deep reasoning on performance, scalability, accessibility.
Enforces: p95 < 200 ms API, FCP < 3 s, `EXPLAIN ANALYZE` on large queries, axe-core WCAG 2.1 AA,
PII encryption verified, pagination on all list endpoints > 100 rows.

### `crm-reviewer`
**File:** `.claude/agents/crm-reviewer.md`
**Model:** `claude-haiku-4-5` · **background:** true · **permissionMode:** acceptEdits
**disallowedTools:** Edit, MultiEdit
**Tools:** Read, Write, Grep, Glob, Bash
**Invoked by:** auto-fires via PostToolUse hook on every `PROGRESS.md` save, or manually via `review the last commit`
Reviews the HEAD diff for: correctness, security (Pydantic, RBAC, audit log), API envelope,
conventions, test coverage ≥ 80%, SRS traceability. Appends verdict to `reports/review-findings.md`.
Runs in background so the implementer never waits for it. Cannot edit source files (disallowedTools).

---

## Hooks

### PreToolUse — schema.prisma guard
**File:** `.claude/hooks/guard-schema-prisma.ps1`
**Matcher:** `Edit | Write | MultiEdit` on any file
**What it does:** Intercepts every file write attempt. If the target is `schema.prisma` (outside
`prisma/migrations/`), checks whether EPIC-DB is currently in progress via `PROGRESS.md`.
Blocks the edit with a clear message if not in EPIC-DB. Fails open on hook error.

### PostToolUse — auto-commit
**File:** `.claude/hooks/commit-on-task-complete.ps1`
**Matcher:** `Edit | Write` on any file
**What it does:** After every file write, checks if `PROGRESS.md` has a newly ticked `[x]` task.
If yes, runs `git add -A` and commits as `<TICKET-ID>: <title> [auto]`. One commit per ticket,
produced automatically — the agent never runs `git commit` manually.

### PostToolUse — inline reviewer
**Config:** `.claude/settings.json` (type: agent, model: haiku)
**Matcher:** `Edit | Write` · **Condition:** `Edit(**/PROGRESS.md)` only
**What it does:** Spins up `crm-reviewer` as an inline agent immediately after the auto-commit lands.
Checks git state, reads the HEAD diff + ticket AC, produces a PASS / CHANGES-NEEDED verdict,
and appends it to `reports/review-findings.md`. Runs in background — never blocks the implementer.

---

## Invocation Reference

### Full epic
```
Implement EPIC-LEAD      →  epic-implementer        (all LEAD-* tickets in order)
Implement EPIC-AUTH      →  epic-implementer-auth   (effort: high)
Implement EPIC-NFR       →  epic-implementer-nfr    (effort: high)
```

### Single ticket
```
Implement LEAD-6         →  epic-implementer
Implement AUTH-3         →  epic-implementer-auth   (effort: high)
Implement NFR-2          →  epic-implementer-nfr    (effort: high)
```

### Manual review
```
review the last commit   →  crm-reviewer            (also auto-fires via hook)
```
