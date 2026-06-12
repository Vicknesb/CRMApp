# Auto-commit hook: fires on PostToolUse(Edit|Write).
# When PROGRESS.md gains a newly checked task ([x] with a TICKET-ID), commit the repo
# with a proper message. Reads the hook JSON payload from stdin.
#
# Git remote/push is intentionally NOT done here (commits are local). Once you provide
# git remote details, uncomment the `git push` line near the bottom to push automatically.

$ErrorActionPreference = 'Stop'
# Repo path — auto-detected, portable across machines/paths:
#   1) CRM_HOOK_REPO env (testing override)
#   2) CLAUDE_PROJECT_DIR (set by Claude Code for hooks)
#   3) derived from this script's location: <repo>\.claude\hooks\thisfile -> up two levels
$repo = if ($env:CRM_HOOK_REPO) { $env:CRM_HOOK_REPO }
        elseif ($env:CLAUDE_PROJECT_DIR) { $env:CLAUDE_PROJECT_DIR }
        else { Split-Path (Split-Path $PSScriptRoot -Parent) -Parent }

function Emit($msg) { Write-Output (@{ systemMessage = $msg } | ConvertTo-Json -Compress) }

try {
    $raw = [Console]::In.ReadToEnd()
    if ([string]::IsNullOrWhiteSpace($raw)) { exit 0 }

    $payload = $raw | ConvertFrom-Json
    $fp = $payload.tool_input.file_path
    if (-not $fp) { exit 0 }
    # Only act when PROGRESS.md was the file edited/written
    if ($fp -notmatch 'PROGRESS\.md$') { exit 0 }

    Set-Location $repo

    # Must be a git repo
    git rev-parse --is-inside-work-tree *> $null
    if ($LASTEXITCODE -ne 0) { exit 0 }

    # Ensure a commit identity exists (fallback only if unset; won't override yours)
    if (-not (git config user.name))  { git config user.name  "CRM Auto Commit" }
    if (-not (git config user.email)) { git config user.email "crm-autocommit@local" }

    # Get the diff of PROGRESS.md vs last commit (or whole file if no commits yet)
    git rev-parse --verify HEAD *> $null
    if ($LASTEXITCODE -eq 0) {
        $diff = (git diff HEAD -- PROGRESS.md | Out-String)
    } else {
        $diff = ((Get-Content (Join-Path $repo 'PROGRESS.md') -Raw) -split "`n" | ForEach-Object { "+$_" }) -join "`n"
    }

    # Find newly-added checked lines: "+ ... [x] ... TICKET-ID · Title"
    $ids = New-Object System.Collections.ArrayList
    $titles = @{}
    foreach ($line in ($diff -split "`n")) {
        if ($line -notmatch '^\+') { continue }
        if ($line -notmatch '\[x\]') { continue }
        if ($line -match '([A-Z]{2,8}-\d+)') {
            $id = $matches[1]
            if (-not $ids.Contains($id)) {
                [void]$ids.Add($id)
                if ($line -match '([A-Z]{2,8}-\d+)\s*[·•\-:]\s*(.+?)\s*$') {
                    $titles[$id] = $matches[2].Trim()
                } else {
                    $titles[$id] = ''
                }
            }
        }
    }

    if ($ids.Count -eq 0) { exit 0 }   # PROGRESS.md changed but no task newly checked

    # Build commit subject
    if ($ids.Count -eq 1) {
        $t = $titles[$ids[0]]
        $subject = if ($t) { "$($ids[0]): $t [auto]" } else { "$($ids[0]): task completed [auto]" }
    } else {
        $subject = "$([string]::Join(', ', $ids)): tasks completed [auto]"
    }

    # Stage everything and commit only if there is something to commit
    git add -A
    git diff --cached --quiet
    if ($LASTEXITCODE -eq 0) { exit 0 }   # nothing staged

    git commit -m $subject -m "Auto-committed on task completion via PostToolUse hook." -m "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>" *> $null

    # --- PUSH (enable once you provide git remote details) ---
    # git push
    # ---------------------------------------------------------

    Emit "Auto-committed: $subject"
}
catch {
    Emit "Auto-commit hook error: $($_.Exception.Message)"
    exit 0
}
