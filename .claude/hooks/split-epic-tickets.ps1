# Splits every tickets/epic-*.md into per-ticket files at tickets/<prefix>/<TICKET-ID>.md
# Run once before starting implementation. Safe to re-run (overwrites existing splits).

$ErrorActionPreference = 'Stop'
$repo = if ($env:CLAUDE_PROJECT_DIR) { $env:CLAUDE_PROJECT_DIR } else { Split-Path (Split-Path $PSScriptRoot -Parent) -Parent }
$ticketsDir = Join-Path $repo 'tickets'

# ticket-ID prefix → subfolder name
$prefixMap = @{
    'PLAT'  = 'plat';  'DB'    = 'db';    'AUTH'  = 'auth';  'LEAD'  = 'lead'
    'CONT'  = 'cont';  'ACCT'  = 'acct';  'PIPE'  = 'pipe';  'ACTV'  = 'actv'
    'TICK'  = 'tick';  'SLA'   = 'sla';   'KB'    = 'kb';    'PROJ'  = 'proj'
    'CONTR' = 'contr'; 'INV'   = 'inv';   'CAMP'  = 'camp';  'ANLY'  = 'anly'
    'COMM'  = 'comm';  'ADMN'  = 'admn';  'INTG'  = 'intg';  'DATA'  = 'data'
    'NFR'   = 'nfr';   'VERIFY'= 'verify';'SEED'  = 'seed'
}

$epicFiles = Get-ChildItem (Join-Path $ticketsDir 'epic-*.md') -File
$totalWritten = 0

foreach ($epicFile in $epicFiles) {
    $raw = Get-Content $epicFile.FullName -Raw -Encoding UTF8

    # Extract epic header block (everything before the first ### ticket heading)
    $headerMatch = [regex]::Match($raw, '^(.*?)(?=\n###\s)', [System.Text.RegularExpressions.RegexOptions]::Singleline)
    $epicHeader = if ($headerMatch.Success) { $headerMatch.Value.Trim() } else { '' }

    # Split on ticket headings: "### TICKET-ID · ..."
    $ticketBlocks = [regex]::Split($raw, '(?m)^(?=###\s+[A-Z]+-\d+)')

    foreach ($block in $ticketBlocks) {
        $block = $block.Trim()
        if (-not $block) { continue }

        # Must start with ### TICKET-ID
        $idMatch = [regex]::Match($block, '^###\s+([A-Z]+-\d+)\b')
        if (-not $idMatch.Success) { continue }

        $ticketId = $idMatch.Groups[1].Value        # e.g. LEAD-6
        $prefix   = [regex]::Match($ticketId, '^([A-Z]+)').Groups[1].Value  # e.g. LEAD

        if (-not $prefixMap.ContainsKey($prefix)) {
            Write-Warning "Unknown prefix '$prefix' in $($epicFile.Name) — skipping $ticketId"
            continue
        }

        $subDir = Join-Path $ticketsDir $prefixMap[$prefix]
        if (-not (Test-Path $subDir)) { New-Item -ItemType Directory -Path $subDir | Out-Null }

        # Build per-ticket file: epic context banner + ticket body
        $epicLine = if ($epicHeader) {
            # Pull the first non-empty line of the epic header as a 1-liner
            $firstLine = ($epicHeader -split "`n" | Where-Object { $_.Trim() -and $_ -notmatch '^#\s*$' } | Select-Object -First 1).Trim('# ').Trim()
            "> **Epic context:** $firstLine`n`n"
        } else { '' }

        $fileContent = $epicLine + $block
        $outPath = Join-Path $subDir "$ticketId.md"
        [System.IO.File]::WriteAllText($outPath, $fileContent, [System.Text.Encoding]::UTF8)
        $totalWritten++
    }
}

Write-Host ('Done. ' + $totalWritten + ' ticket files written under tickets/PREFIX/')
