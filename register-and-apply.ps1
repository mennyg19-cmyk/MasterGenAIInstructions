# Apply MasterGenAIInstructions rules + CodeGraph init/sync to many repos at once.
# Use when onboarding repos that are not yet in registry.json, or to re-apply the full stack.
#
# Usage:
#   .\register-and-apply.ps1 -Discover          # App + Family + D:\Projects git repos (excludes tool forks)
#   .\register-and-apply.ps1 -Path "D:\Projects\Foo"
#   .\register-and-apply.ps1 -Discover -AutoCommit   # then commit rule updates in each git repo

param(
    [string[]]$Path,
    [switch]$Discover,
    [switch]$NoGuardrails,
    [switch]$AutoCommit
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ApplyScript = Join-Path $ScriptDir "apply.ps1"
$UpdateAllScript = Join-Path $ScriptDir "update-all.ps1"

$ExcludeDirNames = @('node_modules', '.git', '.scratch', 'codegraph', 'ponytail', 'genAITemplate')
$ExcludePathFragments = @('\.scratch\', '\node_modules\')

function Test-RepoPath([string]$p) {
    if (-not (Test-Path $p)) { return $false }
    if (-not (Test-Path (Join-Path $p '.git'))) { return $false }
    foreach ($frag in $ExcludePathFragments) {
        if ($p -like "*$frag*") { return $false }
    }
    $leaf = Split-Path $p -Leaf
    if ($ExcludeDirNames -contains $leaf) { return $false }
    return $true
}

function Get-DiscoveredRepos {
    $roots = @(
        'D:\Projects',
        'C:\Users\Menny\Documents\Personal\Program\App',
        'C:\Users\Menny\Documents\Family'
    )
    $repos = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
    foreach ($root in $roots) {
        if (-not (Test-Path -LiteralPath $root)) { continue }
        $dirs = Get-ChildItem -LiteralPath $root -Directory -Recurse -Depth 4 -ErrorAction SilentlyContinue
        foreach ($d in $dirs) {
            $git = Join-Path $d.FullName '.git'
            if (Test-Path -LiteralPath $git) {
                if (Test-RepoPath $d.FullName) { [void]$repos.Add($d.FullName) }
            }
        }
    }
    return @($repos) | Sort-Object
}

$targets = @()
if ($Discover) { $targets += Get-DiscoveredRepos }
if ($Path) { $targets += $Path }
$targets = $targets | ForEach-Object { (Resolve-Path -LiteralPath $_).Path } | Sort-Object -Unique

if ($targets.Count -eq 0) {
    Write-Host "No targets. Use -Discover and/or -Path."
    exit 1
}

Write-Host ""
Write-Host "Applying stack to $($targets.Count) repo(s)..."
Write-Host ""

$applyArgs = @{}
if ($NoGuardrails) { $applyArgs['NoGuardrails'] = $true }

foreach ($target in $targets) {
    Write-Host "========== $target =========="
    & $ApplyScript -TargetDir $target @applyArgs
    Write-Host ""
}

Write-Host "Running update-all to sync template hash across registry..."
$updateArgs = @{ NoCommit = $true }
if (-not $NoGuardrails) { }
if ($AutoCommit) { $updateArgs = @{ AutoCommit = $true } }
& $UpdateAllScript @updateArgs

Write-Host ""
Write-Host "Done."
exit 0
