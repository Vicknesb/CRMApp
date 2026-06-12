# PreToolUse guard: blocks any Edit or Write to schema.prisma outside of EPIC-DB.
#
# Only DB-* tickets are permitted to touch prisma/schema.prisma.
# All other agents/epics must use migration files under prisma/migrations/ instead.
#
# Reads the Claude Code hook JSON payload from stdin.
# Outputs {"decision":"block","reason":"..."} to block, or exits 0 silently to allow.

$ErrorActionPreference = 'Stop'

try {
    $raw = [Console]::In.ReadToEnd()
    if ([string]::IsNullOrWhiteSpace($raw)) { exit 0 }

    $payload = $raw | ConvertFrom-Json
    $fp = $payload.tool_input.file_path

    # Only care about schema.prisma edits
    if (-not $fp) { exit 0 }
    if ($fp -notmatch 'schema\.prisma$') { exit 0 }

    # Allow if the file is a migration snapshot (prisma/migrations/**/migration.prisma)
    # — those are auto-generated, not hand-edited
    if ($fp -match 'migrations[/\\]') { exit 0 }

    # At this point: agent is trying to edit schema.prisma directly.
    # Check PROGRESS.md to see if EPIC-DB is currently in progress.
    $repo = if ($env:CRM_HOOK_REPO) { $env:CRM_HOOK_REPO }
            elseif ($env:CLAUDE_PROJECT_DIR) { $env:CLAUDE_PROJECT_DIR }
            else { Split-Path (Split-Path $PSScriptRoot -Parent) -Parent }

    $progressPath = Join-Path $repo 'PROGRESS.md'
    $epicDbInProgress = $false

    if (Test-Path $progressPath) {
        $content = Get-Content $progressPath -Raw
        # EPIC-DB is "in progress" if its heading exists and it is NOT yet fully checked (☑)
        # i.e. the epic heading line contains ☐ (not yet complete)
        if ($content -match '(?m)^.*☐.*EPIC-DB') {
            $epicDbInProgress = $true
        }
        # Also allow if any DB-* ticket is explicitly marked in-progress via an open checkbox
        # (covers the case where the heading uses a different marker)
        if ($content -match '\[ \].*DB-\d+') {
            $epicDbInProgress = $true
        }
    }

    if ($epicDbInProgress) {
        # EPIC-DB is active — allow the edit
        exit 0
    }

    # Block the edit
    $reason = "schema.prisma is protected. Direct edits are only allowed during EPIC-DB (when DB-* tickets are in progress). To change the schema: (1) switch to EPIC-DB, (2) edit schema.prisma, (3) run 'prisma migrate dev --name <change>'. Never hand-edit schema.prisma outside EPIC-DB — it will desync migrations."

    @{ decision = "block"; reason = $reason } | ConvertTo-Json -Compress
    exit 0
}
catch {
    # On any hook error, fail open (allow the edit) so a hook bug never silently blocks work
    exit 0
}
