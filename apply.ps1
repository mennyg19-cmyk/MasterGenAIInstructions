# === What's in this file ===
# Applies MasterGenAIInstructions rules to an existing project.
# Copies .cursor/rules/, AGENTS.md, and supporting files without overwriting
# existing README.md, .gitignore, or any project code.
#
# Main flow:
#   1. Take a target directory as input
#   2. Copy .cursor/rules/ (overwrites old rules if they exist)
#   3. Copy AGENTS.md (overwrites -- it's generated from the rules)
#   4. Copy DECISION-LOG.md, TESTING-STRATEGY.md, HANDOFF.md only if they don't already exist
#   5. Leave README.md, .gitignore, and all other project files untouched
#   6. Copy CI guardrails workflow (unless -NoGuardrails)
#   7. Ensure CodeGraph MCP (machine) + init/sync index (project) when CLI is on PATH
#   -NoGuardrails   Skip copying .github/workflows/agent-guardrails.yml

param(
    [string]$TargetDir,
    [switch]$NoGuardrails
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TemplateDir = Join-Path $ScriptDir "template"
. (Join-Path $ScriptDir "lib\project-setup.ps1")

if (-not (Test-Path $TemplateDir)) {
    Write-Error "Template directory not found at $TemplateDir"
    exit 1
}

if (-not $TargetDir) {
    $TargetDir = Read-Host "Path to existing project"
}

if (-not (Test-Path $TargetDir)) {
    Write-Error "Directory does not exist: $TargetDir"
    exit 1
}

Write-Host ""
Write-Host "Applying MasterGenAIInstructions to: $TargetDir"
Write-Host ""

$RulesSource = Join-Path $TemplateDir ".cursor\rules"
$RulesDest = Join-Path $TargetDir ".cursor\rules"

New-Item -ItemType Directory -Path $RulesDest -Force | Out-Null
Copy-Item -Path "$RulesSource\*" -Destination $RulesDest -Force
Write-Host "  [copied]   .cursor/rules/ (all rule files)"

$AgentsSource = Join-Path $TemplateDir "AGENTS.md"
Copy-Item -Path $AgentsSource -Destination $TargetDir -Force
Write-Host "  [copied]   AGENTS.md"

$supportingFiles = @("DECISION-LOG.md", "TESTING-STRATEGY.md", "HANDOFF.md")
foreach ($file in $supportingFiles) {
    $dest = Join-Path $TargetDir $file
    if (-not (Test-Path $dest)) {
        Copy-Item -Path (Join-Path $TemplateDir $file) -Destination $dest
        Write-Host "  [created]  $file"
    } else {
        Write-Host "  [skipped]  $file (already exists)"
    }
}

$skippedFiles = @("README.md", ".gitignore")
foreach ($file in $skippedFiles) {
    Write-Host "  [skipped]  $file (not overwriting existing project file)"
}

# Register the project for future updates
$RegistryFile = Join-Path $ScriptDir "registry.json"
$registry = @()
if (Test-Path $RegistryFile) {
    $registry = Get-Content $RegistryFile -Raw | ConvertFrom-Json
}
$fullPath = (Resolve-Path $TargetDir).Path
if ($registry -notcontains $fullPath) {
    $registry += $fullPath
    $registry | ConvertTo-Json | Set-Content $RegistryFile
    Write-Host "  [registered] Project added to registry for future rule updates."
}

if (-not $NoGuardrails) {
    Copy-ProjectGuardrails -ProjectPath $TargetDir -TemplateDir $TemplateDir
}

Ensure-CodeGraphMcp | Out-Null
Sync-ProjectCodeGraph -ProjectPath $TargetDir

Write-Host ""
Write-Host "Done! Rules applied to: $TargetDir"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Fill in .cursor/rules/deploy-awareness.mdc with your deploy targets"
Write-Host "  2. Review AGENTS.md to make sure it fits this project"
if (-not $NoGuardrails) {
    Write-Host "  3. Review .github/workflows/agent-guardrails.yml -- tune or remove jobs as needed"
    Write-Host "  4. Commit the new files"
} else {
    Write-Host "  3. Commit the new files"
}
