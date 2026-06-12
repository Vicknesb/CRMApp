# MCP Setup — Feasibility & Activation (PostgreSQL + GitHub)

> Scaffolding is ready in **`.mcp.json`** (project-scoped). It uses `${ENV_VAR}` placeholders so **no secrets
> are committed**. You provide the actual values later as environment variables, then approve the servers.
> This doc states exactly what's needed, why it's feasible, and how to turn each on.

---

## 1. PostgreSQL MCP

**Purpose:** read-only access to your CRM database so Claude can inspect tables, columns, relations, indexes,
and run `SELECT` queries — directly in-session. Biggest payoff during **EPIC-DB** (verify migrations, seed
data, FK integrity) and later debugging.

**Server:** `@modelcontextprotocol/server-postgres` (run via `npx`, no install).
**Access:** **read-only** (it executes queries; safe for a dev/local DB). Point it at a **dev** database, not prod.

**Prerequisites**
- Node.js + npx available on PATH.
- A running PostgreSQL instance (local Docker is fine — comes from PLAT-9 / DB-1).

**What I need from you later**
- `POSTGRES_CONNECTION_STRING` — e.g. `postgresql://USER:PASSWORD@localhost:5432/crm_dev`
  - Prefer a **read-only DB role** for this MCP (least privilege).

**Feasibility:** ✅ High. Standard server, local DB, read-only — minimal risk. Works once the DB exists (DB-1).

---

## 2. GitHub MCP

**Purpose:** interact with GitHub — repos, issues, PRs, commits — to support the commit-per-ticket workflow,
optionally mirror epics/tickets as GitHub issues, and manage PRs/CI.

**Server:** `@modelcontextprotocol/server-github` (run via `npx`).
**Access:** scoped to whatever the PAT allows — keep it **least-privilege**.

**Prerequisites**
- Node.js + npx.
- A GitHub repository for the CRM (you'll create/connect it).

**What I need from you later**
- `GITHUB_PERSONAL_ACCESS_TOKEN` — a **fine-grained PAT** limited to the CRM repo, with only:
  - **Contents** (read/write — for commits/branches),
  - **Pull requests** (read/write),
  - **Issues** (read/write, only if you want ticket↔issue mirroring),
  - Metadata (read, default).
- The repo target: `OWNER/REPO` (e.g. `your-org/crm`).

**Feasibility:** ✅ High. npx server + a scoped PAT. The only sensitivity is the token — never commit it.

---

## 3. How to provide the details (later)

Set the values as **environment variables** (Claude Code expands `${VAR}` in `.mcp.json` from the environment):

**Option A — `.env` file (recommended; keep it untracked)**
```
# C:\AI_I2I\CRM\.env   (add ".env" to .gitignore — DO NOT COMMIT)
POSTGRES_CONNECTION_STRING=postgresql://crm_ro:PASSWORD@localhost:5432/crm_dev
GITHUB_PERSONAL_ACCESS_TOKEN=github_pat_xxxxxxxxxxxxxxxxx
```

**Option B — Windows session env vars (PowerShell)**
```powershell
$env:POSTGRES_CONNECTION_STRING = "postgresql://crm_ro:PASSWORD@localhost:5432/crm_dev"
$env:GITHUB_PERSONAL_ACCESS_TOKEN = "github_pat_xxxx"
```

> ⚠️ **Security:** add `.env` to `.gitignore` before creating it. Never put real secrets in `.mcp.json`
> (it's committed). Use a read-only DB role and a fine-grained, repo-scoped PAT.

---

## 4. Activation (after values are set)

1. Restart Claude Code (so it loads `.mcp.json` + the new env vars).
2. Run `/mcp` to review and **approve** the `postgres` and `github` servers (project MCP servers require approval).
   - To auto-approve all project servers instead, set `"enableAllProjectMcpServers": true` in `.claude/settings.json`.
3. Verify: ask Claude to "list database tables" (postgres) and "show open issues" (github).

---

## 5. Status checklist

- [x] `.mcp.json` scaffolded with both servers (placeholders, no secrets).
- [x] This feasibility/setup doc written.
- [ ] You provide `POSTGRES_CONNECTION_STRING` (dev DB, read-only role).
- [ ] You provide `GITHUB_PERSONAL_ACCESS_TOKEN` (fine-grained, repo-scoped) + `OWNER/REPO`.
- [ ] `.env` created and added to `.gitignore`.
- [ ] Servers approved via `/mcp`; connectivity verified.

> Tell me when you have the details and I'll finish wiring + verify both connections.
