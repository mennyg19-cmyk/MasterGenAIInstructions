# === What's in this file ===
# Pushes updated rules to all registered projects.
# Reads registry.json for the list of projects, copies .cursor/rules/ and AGENTS.md
# to each one (PRESERVING each project's own deploy-awareness.mdc), then commits.
#
# Usage:
#   .\update-all.ps1              # prompts whether to commit in each project
#   .\update-all.ps1 -AutoCommit  # commits + pushes in each project without prompting
#   .\update-all.ps1 -NoCommit    # copies only, never commits

param(
    [switch]$AutoCommit,
    [switch]$NoCommit
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TemplateDir = Join-Path $ScriptDir "template"
$RegistryFile = Join-Path $ScriptDir "registry.json"

if (-not (Test-Path $RegistryFile)) {
    Write-Host "No registry.json found. No projects to update."
    exit 0
}

$registry = Get-Content $RegistryFile -Raw | ConvertFrom-Json

if ($registry.Count -eq 0) {
    Write-Host "Registry is empty. Bootstrap or apply to a project first."
    exit 0
}

Write-Host ""
Write-Host "Updating rules in $($registry.Count) registered project(s)..."
Write-Host ""

$RulesSource = Join-Path $TemplateDir ".cursor\rules"
$AgentsSource = Join-Path $TemplateDir "AGENTS.md"
$updated = @()
$skipped = @()

# Files OWNED BY EACH PROJECT -- never overwritten by an update.
# deploy-awareness.mdc holds per-project deploy config (Vercel project, env vars, branch
# strategy); clobbering it with the generic template would wipe real configuration.
$ProjectOwnedFiles = @("deploy-awareness.mdc")

foreach ($projectPath in $registry) {
    if (-not (Test-Path $projectPath)) {
        Write-Host "  [missing]  $projectPath -- directory not found, skipping"
        $skipped += $projectPath
        continue
    }

    $rulesDest = Join-Path $projectPath ".cursor\rules"
    New-Item -ItemType Directory -Path $rulesDest -Force | Out-Null
    Copy-Item -Path "$RulesSource\*" -Destination $rulesDest -Force -Exclude $ProjectOwnedFiles
    Copy-Item -Path $AgentsSource -Destination $projectPath -Force

    Write-Host "  [updated]  $projectPath  (preserved: $($ProjectOwnedFiles -join ', '))"
    $updated += $projectPath
}

# Clean missing projects from registry
if ($skipped.Count -gt 0) {
    $cleanRegistry = $registry | Where-Object { $skipped -notcontains $_ }
    $cleanRegistry | ConvertTo-Json | Set-Content $RegistryFile
    Write-Host ""
    Write-Host "  Removed $($skipped.Count) missing project(s) from registry."
}

Write-Host ""
Write-Host "Updated $($updated.Count) project(s)."

if ($updated.Count -gt 0) {
    $doCommit = $false
    if ($AutoCommit) {
        $doCommit = $true
    } elseif (-not $NoCommit) {
        Write-Host ""
        $commitChoice = Read-Host "Commit the updated rules in each project? (y/n, default: n)"
        $doCommit = ($commitChoice -eq "y")
    }

    if ($doCommit) {
        foreach ($projectPath in $updated) {
            Push-Location $projectPath
            # Scope status/add to rules + AGENTS only -- never touch a project's in-flight work.
            $hasChanges = git status --porcelain -- .cursor/rules/ AGENTS.md
            if ($hasChanges) {
                git add .cursor/rules/ AGENTS.md
                git commit -m "Update rules from MasterGenAIInstructions" | Out-Null
                git push 2>$null
                Write-Host "  [committed] $projectPath"
            } else {
                Write-Host "  [no changes] $projectPath"
            }
            Pop-Location
        }
    }
}

Write-Host ""
Write-Host "Done."
