# Auto-commit hook: works in ALL modes (CLI, desktop, direct Bash call).
# Detects newly-ticked [x] lines in PROGRESS.md and auto-commits.

$repo = if ($env:CRM_HOOK_REPO) { $env:CRM_HOOK_REPO }
        elseif ($env:CLAUDE_PROJECT_DIR) { $env:CLAUDE_PROJECT_DIR }
        else { Split-Path (Split-Path $PSScriptRoot -Parent) -Parent }

function Emit([string]$msg) {
    Write-Output (@{ systemMessage = $msg } | ConvertTo-Json -Compress)
}

Set-Location $repo

$null = git rev-parse --is-inside-work-tree *>&1
if ($LASTEXITCODE -ne 0) { exit 0 }

if (-not (git config user.name))  { git config user.name  "CRM Auto Commit" }
if (-not (git config user.email)) { git config user.email "crm-autocommit@local" }

# Get diff of PROGRESS.md against HEAD
$null = git rev-parse --verify HEAD *>&1
if ($LASTEXITCODE -eq 0) {
    $diff = (git diff HEAD -- PROGRESS.md) -join "`n"
} else {
    $raw = Get-Content (Join-Path $repo "PROGRESS.md") -Raw -ErrorAction SilentlyContinue
    $diff = ($raw -split "`n" | ForEach-Object { "+$_" }) -join "`n"
}

# Find newly-ticked ticket IDs
$ids    = [System.Collections.ArrayList]::new()
$titles = @{}
foreach ($line in ($diff -split "`n")) {
    if ($line -notmatch "^\+") { continue }
    if ($line -notmatch "\[x\]") { continue }
    if ($line -match "([A-Z]{2,8}-\d+)") {
        $id = $Matches[1]
        if (-not $ids.Contains($id)) {
            [void]$ids.Add($id)
            if ($line -match "[A-Z]{2,8}-\d+\s*[^\[]+\[x\]\s*[^\[]+\s+(.+)$") {
                $titles[$id] = ($Matches[1].Trim() -replace "\s+", " ")
            } else {
                $titles[$id] = ""
            }
        }
    }
}

if ($ids.Count -eq 0) {
    Emit "No newly-completed tickets found -- skipping commit."
    exit 0
}

# Build commit subject
if ($ids.Count -eq 1) {
    $t = $titles[$ids[0]].Trim()
    $subject = if ($t) { "$($ids[0]): $t [auto]" } else { "$($ids[0]): task completed [auto]" }
} else {
    $subject = "$([string]::Join(', ', [string[]]$ids)): tasks completed [auto]"
}

# Stage everything (suppress LF warnings by ignoring all output)
git add -A *>&1 | Out-Null

# Check if anything is staged: git status --porcelain shows staged as first char
$porcelain = git status --porcelain *>&1
$hasStagedFiles = $porcelain | Where-Object { $_ -match "^[MADRCU]" }

if (-not $hasStagedFiles) {
    Emit "Nothing staged -- skipping commit."
    exit 0
}

# Commit
git commit -m $subject -m "Auto-committed on task completion." *>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Emit "SUCCESS: Auto-committed -- $subject"
} else {
    Emit "FAILED: git commit returned non-zero."
}
