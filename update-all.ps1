# === What's in this file ===
# Pushes updated rules to all registered projects.
# Reads registry.json for the list of projects, copies .cursor/rules/ and AGENTS.md
# to each one, then offers to commit the changes.

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

foreach ($projectPath in $registry) {
    if (-not (Test-Path $projectPath)) {
        Write-Host "  [missing]  $projectPath -- directory not found, skipping"
        $skipped += $projectPath
        continue
    }

    $rulesDest = Join-Path $projectPath ".cursor\rules"
    New-Item -ItemType Directory -Path $rulesDest -Force | Out-Null
    Copy-Item -Path "$RulesSource\*" -Destination $rulesDest -Force
    Copy-Item -Path $AgentsSource -Destination $projectPath -Force

    Write-Host "  [updated]  $projectPath"
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
    Write-Host ""
    $commitChoice = Read-Host "Commit the updated rules in each project? (y/n, default: n)"
    if ($commitChoice -eq "y") {
        foreach ($projectPath in $updated) {
            Push-Location $projectPath
            $hasChanges = git status --porcelain
            if ($hasChanges) {
                git add .cursor/rules/ AGENTS.md
                git commit -m "Update rules from MasterGenAIInstructions"
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
