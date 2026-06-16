# === What's in this file ===
# Bootstrap script that creates a new project from the MasterGenAIInstructions template.
#
# Main flow:
#   1. Prompt for project name, description, destination, GitHub preference
#   2. Copy template/ into the destination
#   3. Replace {{PROJECT_NAME}} and {{DESCRIPTION}} placeholders
#   4. Initialize git
#   5. Optionally create a private GitHub repo and push

param(
    [string]$ProjectName,
    [string]$Description,
    [string]$Destination,
    [switch]$NoGitHub
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TemplateDir = Join-Path $ScriptDir "template"

if (-not (Test-Path $TemplateDir)) {
    Write-Error "Template directory not found at $TemplateDir"
    exit 1
}

if (-not $ProjectName) {
    $ProjectName = Read-Host "Project name"
}

if (-not $ProjectName) {
    Write-Error "Project name is required."
    exit 1
}

if (-not $Description) {
    $Description = Read-Host "Description (one line)"
}

if (-not $Destination) {
    $DefaultDest = Join-Path (Get-Location) $ProjectName
    $Destination = Read-Host "Destination directory (default: $DefaultDest)"
    if (-not $Destination) {
        $Destination = $DefaultDest
    }
}

if (Test-Path $Destination) {
    Write-Error "Destination already exists: $Destination"
    exit 1
}

Write-Host ""
Write-Host "Creating project: $ProjectName"
Write-Host "Description:      $Description"
Write-Host "Destination:      $Destination"
Write-Host ""

Copy-Item -Path $TemplateDir -Destination $Destination -Recurse -Force

$mdFiles = Get-ChildItem -Path $Destination -Recurse -Include "*.md","*.mdc" -File
foreach ($file in $mdFiles) {
    $content = Get-Content $file.FullName -Raw
    $content = $content -replace '\{\{PROJECT_NAME\}\}', $ProjectName
    $content = $content -replace '\{\{DESCRIPTION\}\}', $Description
    Set-Content -Path $file.FullName -Value $content -NoNewline
}

Push-Location $Destination

git init -b main
git add -A
git commit -m "Initial project scaffold from MasterGenAIInstructions"

if (-not $NoGitHub) {
    $createRepo = Read-Host "Create private GitHub repo? (y/n, default: y)"
    if ($createRepo -ne "n") {
        $ghAvailable = Get-Command gh -ErrorAction SilentlyContinue
        if ($ghAvailable) {
            gh repo create $ProjectName --private --source . --push
            Write-Host ""
            Write-Host "GitHub repo created and pushed."
        } else {
            Write-Warning "gh CLI not found. Install it to auto-create GitHub repos: https://cli.github.com"
            Write-Host "You can push manually later."
        }
    }
}

Pop-Location

# Register the project for future updates
$RegistryFile = Join-Path $ScriptDir "registry.json"
$registry = @()
if (Test-Path $RegistryFile) {
    $registry = Get-Content $RegistryFile -Raw | ConvertFrom-Json
}
$fullPath = (Resolve-Path $Destination).Path
if ($registry -notcontains $fullPath) {
    $registry += $fullPath
    $registry | ConvertTo-Json | Set-Content $RegistryFile
    Write-Host "  [registered] Project added to registry for future rule updates."
}

Write-Host ""
Write-Host "Done! Your project is ready at: $Destination"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Open $Destination in Cursor"
Write-Host "  2. Fill in .cursor/rules/deploy-awareness.mdc with your deploy targets"
$cgCli = Get-Command codegraph -ErrorAction SilentlyContinue
if ($cgCli) {
    $cgInit = Read-Host "Run codegraph init in this project? (y/n, default: y)"
    if ($cgInit -ne "n") {
        Push-Location $Destination
        codegraph init
        Pop-Location
        Write-Host "  [codegraph] Index built at .codegraph/"
    }
} else {
    Write-Host "  3. Optional: install CodeGraph (https://github.com/colbymchenry/codegraph) then run codegraph install && codegraph init"
}
Write-Host "  4. Start building -- agents already know your workflow"
