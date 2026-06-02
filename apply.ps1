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

param(
    [string]$TargetDir
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TemplateDir = Join-Path $ScriptDir "template"

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
Write-Host "  [copied]   .cursor/rules/ (13 rule files)"

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

Write-Host ""
Write-Host "Done! Rules applied to: $TargetDir"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Fill in .cursor/rules/deploy-awareness.mdc with your deploy targets"
Write-Host "  2. Review AGENTS.md to make sure it fits this project"
Write-Host "  3. Commit the new files"
