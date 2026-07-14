# Refresh Cursor model catalog and diff against Job assignments.
# Usage:
#   .\check-models.ps1              # fetch + report (needs CURSOR_API_KEY env or cursor-agent)
#   .\check-models.ps1 -SyncOnly    # sync tables from model-roster.json
#   .\check-models.ps1 -PushApps    # after a successful sync: run update-all -AutoCommit

param(
    [switch]$SyncOnly,
    [switch]$PushApps,
    [string]$CatalogFile = ""
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $py) {
    Write-Error "python/python3 not on PATH"
    exit 1
}

if ($SyncOnly) {
    & $py.Source "lib\model-roster.py" sync
    $code = $LASTEXITCODE
    if ($code -ne 0) { exit $code }
    if ($PushApps) {
        Write-Host ""
        Write-Host "Pushing updated rules to registered apps..."
        & (Join-Path $ScriptDir "update-all.ps1") -AutoCommit
    }
    exit 0
}

$reportArgs = @("lib\model-roster.py", "report", "--out", ".scratch\model-roster-report.md")
if ($CatalogFile) {
    $reportArgs += @("--catalog-file", $CatalogFile)
}

& $py.Source @reportArgs
$code = $LASTEXITCODE

Write-Host ""
if (Test-Path ".scratch\model-roster-report.md") {
    Write-Host "Report: .scratch\model-roster-report.md"
    Get-Content ".scratch\model-roster-report.md" | Select-Object -First 40
}

if ($code -eq 2) {
    Write-Host ""
    Write-Host "ACTION NEEDED: edit _meta\model-roster.json, then:"
    Write-Host "  .\check-models.ps1 -SyncOnly -PushApps"
} elseif ($code -eq 0) {
    Write-Host ""
    Write-Host "Roster OK against current catalog."
}

exit $code
