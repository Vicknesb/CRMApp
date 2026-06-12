# Parallel Agents — Complete Guide

> This document covers everything about how parallel agents work in the CRM project:
> what they are, how they are grouped, how to run them, token usage, context windows,
> merging, pros, cons, and real timelines.

---

## 1. What Are Parallel Agents?

In Claude Code, every agent invocation is a **completely separate Claude API call** with its own:
- Context window
- Tool call budget (maxTurns)
- Git worktree (because `isolation: worktree` is set)
- Memory — agents share nothing at runtime

When you run agents **in parallel**, you open multiple Claude Code sessions simultaneously
and invoke one agent in each. They all run at the same time, each unaware of the others,
each writing code into their own isolated git branch.

The result: **wall-clock time = the slowest agent in the group**, not the sum of all agents.

---

## 2. Build Order and Dependency Map

```
PLAT → DB → AUTH → [Group 4] → [Group 5] → INTG → [Group 7] → [Group 8] → ADMN → DATA → NFR → VERIFY
```

Epics inside `[ ]` brackets are **independent of each other** and can run in parallel.
Epics outside brackets must run **sequentially** — each depends on the previous completing first.

### Full dependency chain

```
PLAT          (no deps — run first)
  └─► DB      (needs PLAT ☑)
        └─► AUTH         (needs DB ☑)
               └─► LEAD  ─┐
                   CONT  ─┤  GROUP 4 — all need AUTH ☑ — run simultaneously
                   ACCT  ─┤
                   PIPE  ─┤
                   ACTV  ─┘
                        └─► TICK ─┐
                            SLA  ─┤  GROUP 5 — all need Group 4 ☑ — run simultaneously
                            KB   ─┘
                                 └─► INTG     (needs Group 5 ☑)
                                          └─► PROJ  ─┐
                                              CONTR ─┤  GROUP 7 — all need INTG ☑ — run simultaneously
                                              INV   ─┘
                                                   └─► CAMP ─┐
                                                       ANLY ─┤  GROUP 8 — all need Group 7 ☑ — run simultaneously
                                                       COMM ─┘
                                                            └─► ADMN     (needs Group 8 ☑)
                                                                     └─► DATA   (needs ADMN ☑)
                                                                               └─► NFR    (needs DATA ☑)
                                                                                        └─► VERIFY (needs NFR ☑)
```

---

## 3. The Four Parallel Groups

### Group 4 — after AUTH completes
| Agent | Epic | Tickets | Prerequisite |
|-------|------|---------|-------------|
| `epic-implementer-lead` | EPIC-LEAD | LEAD-* | AUTH ☑ |
| `epic-implementer-cont` | EPIC-CONT | CONT-* | AUTH ☑ |
| `epic-implementer-acct` | EPIC-ACCT | ACCT-* | AUTH ☑ |
| `epic-implementer-pipe` | EPIC-PIPE | PIPE-* | AUTH ☑ |
| `epic-implementer-actv` | EPIC-ACTV | ACTV-* | AUTH ☑ |

### Group 5 — after Group 4 completes
| Agent | Epic | Tickets | Prerequisite |
|-------|------|---------|-------------|
| `epic-implementer-tick` | EPIC-TICK | TICK-* | LEAD ☑ CONT ☑ ACCT ☑ PIPE ☑ ACTV ☑ |
| `epic-implementer-sla`  | EPIC-SLA  | SLA-*  | LEAD ☑ CONT ☑ ACCT ☑ PIPE ☑ ACTV ☑ |
| `epic-implementer-kb`   | EPIC-KB   | KB-*   | LEAD ☑ CONT ☑ ACCT ☑ PIPE ☑ ACTV ☑ |

### Group 7 — after INTG completes
| Agent | Epic | Tickets | Prerequisite |
|-------|------|---------|-------------|
| `epic-implementer-proj`  | EPIC-PROJ  | PROJ-*  | INTG ☑ |
| `epic-implementer-contr` | EPIC-CONTR | CONTR-* | INTG ☑ |
| `epic-implementer-inv`   | EPIC-INV   | INV-*   | INTG ☑ |

### Group 8 — after Group 7 completes
| Agent | Epic | Tickets | Prerequisite |
|-------|------|---------|-------------|
| `epic-implementer-camp` | EPIC-CAMP | CAMP-* | PROJ ☑ CONTR ☑ INV ☑ |
| `epic-implementer-anly` | EPIC-ANLY | ANLY-* | PROJ ☑ CONTR ☑ INV ☑ |
| `epic-implementer-comm` | EPIC-COMM | COMM-* | PROJ ☑ CONTR ☑ INV ☑ |

### Sequential epics (not parallelisable)
| Agent | Epic | Reason |
|-------|------|--------|
| `epic-implementer` | EPIC-PLAT | First epic — nothing to parallel with |
| `epic-implementer` | EPIC-DB | Depends on PLAT only |
| `epic-implementer-auth` | EPIC-AUTH | Depends on DB only |
| `epic-implementer` | EPIC-INTG | Depends on all of Group 5 |
| `epic-implementer` | EPIC-ADMN | Depends on all of Group 8 |
| `epic-implementer` | EPIC-DATA | Depends on ADMN only |
| `epic-implementer-nfr` | EPIC-NFR | Depends on DATA only |
| `epic-implementer` | EPIC-VERIFY | Depends on NFR only |

---

## 4. How to Run Parallel Agents

### Step 1 — Verify prerequisites
Before starting a group, confirm all prerequisite epics are ☑ in `PROGRESS.md`.
Each agent's `initialPrompt` does this automatically — if prerequisites are not met,
the agent reports BLOCKED and stops before writing any code.

### Step 2 — Open one Claude Code session per agent
Open N separate Claude Code windows/terminals for the group you want to run.
Each session is completely independent.

### Step 3 — Invoke one agent per session

**Group 4 — 5 sessions:**
```
Session 1:  Implement EPIC-LEAD
Session 2:  Implement EPIC-CONT
Session 3:  Implement EPIC-ACCT
Session 4:  Implement EPIC-PIPE
Session 5:  Implement EPIC-ACTV
```

**Group 5 — 3 sessions:**
```
Session 1:  Implement EPIC-TICK
Session 2:  Implement EPIC-SLA
Session 3:  Implement EPIC-KB
```

**Group 7 — 3 sessions:**
```
Session 1:  Implement EPIC-PROJ
Session 2:  Implement EPIC-CONTR
Session 3:  Implement EPIC-INV
```

**Group 8 — 3 sessions:**
```
Session 1:  Implement EPIC-CAMP
Session 2:  Implement EPIC-ANLY
Session 3:  Implement EPIC-COMM
```

### Step 4 — Wait for all agents in the group to finish
All agents must complete (green tests) before you move to the next group.
Do NOT start Group 5 until every agent in Group 4 reports completion.

### Step 5 — Merge the worktrees
Each agent worked in its own git worktree (separate branch). Merge them into main:

```bash
# Example for Group 4
git merge worktree/epic-lead
git merge worktree/epic-cont    # resolve PROGRESS.md conflict here if any
git merge worktree/epic-acct
git merge worktree/epic-pipe
git merge worktree/epic-actv
```

Conflicts will almost always be in `PROGRESS.md` only (each agent ticked its own tickets).
Resolve by accepting all checked lines from both sides — no code conflicts expected since
each agent touched different module folders (`features/lead/`, `features/cont/`, etc.).

### Step 6 — Start the next group
Once all worktrees are merged and `PROGRESS.md` shows all Group 4 epics ☑, open sessions
for Group 5 and repeat from Step 2.

---

## 5. Context Window — Per Agent

Each agent gets its own **fresh 200K token context window**. They share nothing.

### What fills one agent's context window during an epic run

```
initialPrompt loads:
  AGENT-CONTEXT.md            ~  1,000 tokens
  PROGRESS.md                 ~  3,000 tokens

Per ticket (repeated N times):
  ticket file (15 lines)      ~    200 tokens each
  mockup HTML (UI tickets)    ~  2,500 tokens each
  grep/glob results           ~    500 tokens each
  files read for context      ~  1,500 tokens each
  code written (echoed back)  ~  2,000 tokens each
  test output (pytest/vitest) ~    800 tokens each
  ─────────────────────────────────────────────────
  Per ticket total            ~  7,500 tokens

For a 12-ticket epic:
  Bootstrap                   ~  4,000 tokens
  12 tickets × 7,500          ~ 90,000 tokens
  ─────────────────────────────────────────────────
  Total per agent             ~ 94,000 tokens   (well within 200K limit)
```

### Context window safety margin

| Epic size | Estimated tokens | 200K limit | Headroom |
|-----------|-----------------|------------|---------|
| Small (5 tickets) | ~40K | 200K | 160K ✅ |
| Medium (12 tickets) | ~94K | 200K | 106K ✅ |
| Large (20 tickets) | ~154K | 200K | 46K ✅ |
| Very large (25+ tickets) | ~190K | 200K | 10K ⚠️ |

`maxTurns: 80` acts as a safety cap — it limits how many tool results can accumulate
in context, preventing runaway context growth on very large epics.

---

## 6. Token Cost — Parallel vs Sequential

### Key truth: parallel agents do NOT save tokens. They save time.

The total token bill is identical whether you run sequentially or in parallel.
You are running the same work — just simultaneously instead of one after another.

### Sequential (old approach)
```
LEAD runs:  70K tokens   40 min
CONT runs:  65K tokens   35 min   (after LEAD finishes)
ACCT runs:  60K tokens   30 min   (after CONT finishes)
PIPE runs:  55K tokens   30 min   (after ACCT finishes)
ACTV runs:  50K tokens   25 min   (after PIPE finishes)
─────────────────────────────────────────────────────
Total:     300K tokens   160 min wall-clock time
```

### Parallel (new approach)
```
LEAD runs:  70K tokens  ─┐
CONT runs:  65K tokens  ─┤  all running simultaneously
ACCT runs:  60K tokens  ─┤
PIPE runs:  55K tokens  ─┤
ACTV runs:  50K tokens  ─┘
─────────────────────────────────────────────────────
Total:     300K tokens   40 min wall-clock time  (only the slowest agent)
```

**Same token cost. 4× faster.**

### Where parallel is slightly MORE expensive

Shared files get loaded once per agent instead of once total:

```
Sequential:
  PROGRESS.md loaded  1 time = 3,000 tokens

Parallel (5 agents):
  PROGRESS.md loaded  5 times = 15,000 tokens  (+12,000 tokens overhead)
  AGENT-CONTEXT.md loaded 5 times = 5,000 tokens  (+4,000 tokens overhead)
```

Total overhead per parallel group: ~16,000 extra tokens — roughly 5% more than sequential.
This is the price of the time saving. Completely worth it.

---

## 7. Time Savings — Real Numbers

Assuming each epic takes ~30 minutes on average:

### Sequential approach (no parallel)
```
PLAT(30) + DB(30) + AUTH(45) +
LEAD(40) + CONT(35) + ACCT(30) + PIPE(30) + ACTV(25) +   ← 160 min sequential
TICK(35) + SLA(30) + KB(25) +                              ←  90 min sequential
INTG(30) +
PROJ(40) + CONTR(35) + INV(30) +                           ← 105 min sequential
CAMP(30) + ANLY(45) + COMM(25) +                           ← 100 min sequential
ADMN(30) + DATA(25) + NFR(45) + VERIFY(30)
─────────────────────────────────────────────────────────────
Total: ~895 minutes (~15 hours) wall-clock
```

### Parallel approach (with group agents)
```
PLAT(30) + DB(30) + AUTH(45) +
max(LEAD40, CONT35, ACCT30, PIPE30, ACTV25) = 40 min +    ← was 160 min
max(TICK35, SLA30, KB25) = 35 min +                        ← was  90 min
INTG(30) +
max(PROJ40, CONTR35, INV30) = 40 min +                     ← was 105 min
max(CAMP30, ANLY45, COMM25) = 45 min +                     ← was 100 min
ADMN(30) + DATA(25) + NFR(45) + VERIFY(30)
─────────────────────────────────────────────────────────────
Total: ~425 minutes (~7 hours) wall-clock
```

**Savings: ~470 minutes (~8 hours) — roughly 53% faster.**

---

## 8. Isolation — How Worktrees Work

Each agent has `isolation: worktree` in its frontmatter. This means:

1. Claude Code creates a new git branch (e.g. `worktree/epic-lead`)
2. A separate directory checkout of that branch is created
3. The agent works entirely inside that directory
4. Your main working tree is **never touched** during the run
5. If the agent fails or goes wrong — you discard the worktree, main is clean
6. If tests pass — you merge the worktree branch into main

```
main branch          worktree/epic-lead    worktree/epic-cont
     │                      │                     │
     │               agent writes here     agent writes here
     │               (features/lead/)      (features/cont/)
     │                      │                     │
     └──── merge ───────────┴─────────────────────┘
           (after all green)
```

### Why worktrees prevent code conflicts

Each epic's agent writes to a different module folder:
```
epic-implementer-lead  →  apps/web/src/features/lead/
epic-implementer-cont  →  apps/web/src/features/cont/
epic-implementer-acct  →  apps/web/src/features/acct/
```

These folders don't overlap. The **only** file all agents write to is `PROGRESS.md`
(when ticking tickets done). That's the only merge conflict you'll ever see.

---

## 9. PROGRESS.md Merge Conflicts — How to Handle

When merging 5 worktrees, `PROGRESS.md` will have conflicts because each agent ticked
different lines. The conflict looks like:

```
<<<<<<< HEAD
- [ ] LEAD-6 · Scoring engine
=======
- [x] LEAD-6 · Scoring engine
>>>>>>> worktree/epic-lead
```

**Resolution rule: always accept the `[x]` version** — the checked version is the truth.
Never accept `[ ]` over `[x]`. A quick find-and-replace resolves all conflicts in under
a minute:

```bash
# After git merge conflict on PROGRESS.md:
# Open the file, search for <<<<<<< and accept [x] lines over [ ] lines
# Then:
git add PROGRESS.md
git commit -m "Merge Group 4 parallel worktrees"
```

---

## 10. Prerequisite Guard — How It Works

Every parallel agent's `initialPrompt` checks prerequisites automatically:

```
Agent starts
    │
    ▼
Reads PROGRESS.md
    │
    ▼
Checks required epics for ☑
    │
    ├── NOT all ☑ → reports "BLOCKED: <prerequisite> must complete first" → STOPS
    │
    └── All ☑ → proceeds with task instruction
```

This means you can safely invoke all 5 Group 4 agents **before** AUTH finishes —
they will each report BLOCKED and not write a single line of code. Once AUTH completes,
re-invoke them and they proceed.

---

## 11. Pros and Cons

### Pros

**Speed**
- 53% faster total wall-clock time across the full 22-epic build
- Group 4 alone: 160 min → 40 min (saves 2+ hours in one group)
- Run overnight — wake up with 5 epics done instead of 1

**Safety**
- `isolation: worktree` means nothing lands on main until you merge manually
- Prerequisite guard prevents out-of-order implementation
- Scope guard prevents each agent from accidentally implementing the wrong epic
- If one agent fails, the other 4 are unaffected

**Clarity**
- Each agent is scoped to one epic — easy to see which session is doing what
- Completion reports are per-epic — clear audit trail
- Merge conflicts are predictable (PROGRESS.md only)

**Cost neutrality**
- Same total token spend as sequential — no extra API cost for the speed gain
- Only ~5% overhead from shared file re-loads

---

### Cons

**Merge overhead**
- After each group you must manually merge N worktrees
- PROGRESS.md conflicts are minor but require attention
- More git history noise (N merge commits per group)

**Resource usage**
- 5 parallel agents = 5 simultaneous model API calls
- Your machine runs 5 Claude Code processes at once — CPU/memory overhead
- API rate limits: if your Anthropic account has concurrency limits, you may get throttled

**Monitoring complexity**
- You need to watch 5 terminal windows simultaneously
- If one agent gets stuck, you must notice and intervene manually
- No single "is everything done?" view — you check each session

**PROGRESS.md race condition (edge case)**
- If two agents finish a ticket at the exact same second and both try to write PROGRESS.md,
  the auto-commit hook may fire twice simultaneously — potential git lock error
- In practice this is extremely rare (agents finish at different moments)
- Workaround: each agent has its own PROGRESS.md copy in its worktree — no actual race

**Context duplication**
- Shared files (PROGRESS.md, AGENT-CONTEXT.md) loaded N times total
- ~16K extra tokens per group — minor but worth knowing

---

## 12. Complete Agent Inventory

### Parallel agents (created for this project)
| Agent file | Epic | Group | Prerequisite |
|------------|------|-------|-------------|
| `epic-implementer-lead.md` | LEAD | 4 | AUTH ☑ |
| `epic-implementer-cont.md` | CONT | 4 | AUTH ☑ |
| `epic-implementer-acct.md` | ACCT | 4 | AUTH ☑ |
| `epic-implementer-pipe.md` | PIPE | 4 | AUTH ☑ |
| `epic-implementer-actv.md` | ACTV | 4 | AUTH ☑ |
| `epic-implementer-tick.md` | TICK | 5 | Group 4 all ☑ |
| `epic-implementer-sla.md`  | SLA  | 5 | Group 4 all ☑ |
| `epic-implementer-kb.md`   | KB   | 5 | Group 4 all ☑ |
| `epic-implementer-proj.md` | PROJ | 7 | INTG ☑ |
| `epic-implementer-contr.md`| CONTR| 7 | INTG ☑ |
| `epic-implementer-inv.md`  | INV  | 7 | INTG ☑ |
| `epic-implementer-camp.md` | CAMP | 8 | Group 7 all ☑ |
| `epic-implementer-anly.md` | ANLY | 8 | Group 7 all ☑ |
| `epic-implementer-comm.md` | COMM | 8 | Group 7 all ☑ |

### Sequential agents (existing)
| Agent file | Epic | Prerequisite |
|------------|------|-------------|
| `epic-implementer.md` | PLAT, DB, INTG, ADMN, DATA, VERIFY | varies |
| `epic-implementer-auth.md` | AUTH | DB ☑ |
| `epic-implementer-nfr.md`  | NFR  | DATA ☑ |
| `crm-reviewer.md` | all — auto-fires via hook | — |

---

## 13. Recommended Run Order (Full Build)

```
Phase 1 — Sequential bootstrap
  [1 session]  Implement EPIC-PLAT
  [1 session]  Implement EPIC-DB
  [1 session]  Implement EPIC-AUTH    ← uses epic-implementer-auth (effort: high)

Phase 2 — Group 4 parallel  (open 5 sessions simultaneously)
  [Session 1]  Implement EPIC-LEAD
  [Session 2]  Implement EPIC-CONT
  [Session 3]  Implement EPIC-ACCT
  [Session 4]  Implement EPIC-PIPE
  [Session 5]  Implement EPIC-ACTV
  → Wait for all 5 to finish → merge 5 worktrees → resolve PROGRESS.md

Phase 3 — Group 5 parallel  (open 3 sessions simultaneously)
  [Session 1]  Implement EPIC-TICK
  [Session 2]  Implement EPIC-SLA
  [Session 3]  Implement EPIC-KB
  → Wait for all 3 → merge → resolve

Phase 4 — Sequential
  [1 session]  Implement EPIC-INTG

Phase 5 — Group 7 parallel  (open 3 sessions simultaneously)
  [Session 1]  Implement EPIC-PROJ
  [Session 2]  Implement EPIC-CONTR
  [Session 3]  Implement EPIC-INV
  → Wait for all 3 → merge → resolve

Phase 6 — Group 8 parallel  (open 3 sessions simultaneously)
  [Session 1]  Implement EPIC-CAMP
  [Session 2]  Implement EPIC-ANLY
  [Session 3]  Implement EPIC-COMM
  → Wait for all 3 → merge → resolve

Phase 7 — Sequential finish
  [1 session]  Implement EPIC-ADMN
  [1 session]  Implement EPIC-DATA
  [1 session]  Implement EPIC-NFR      ← uses epic-implementer-nfr (effort: high)
  [1 session]  Implement EPIC-VERIFY
```

---

## 14. Quick Reference Card

```
WHEN TO USE PARALLEL:
  ✅ Epics in the same [ ] group in the build order
  ✅ After their shared prerequisite is ☑ in PROGRESS.md
  ✅ When you want faster wall-clock time

WHEN NOT TO USE PARALLEL:
  ❌ Epics that depend on each other (e.g. TICK depends on LEAD)
  ❌ Sequential epics (PLAT, DB, AUTH, INTG, ADMN, DATA, NFR, VERIFY)
  ❌ When your machine/API account can't handle concurrent sessions

TOKEN COST:    Same as sequential + ~5% overhead from shared file re-loads
CONTEXT:       Each agent gets its own fresh 200K window — no sharing
CONFLICTS:     PROGRESS.md only — always accept [x] over [ ]
SAFETY:        isolation: worktree — main branch never touched until you merge
PREREQUISITE:  Each agent self-checks on start — reports BLOCKED if not ready
```
