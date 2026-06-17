# Shared project setup helpers for bootstrap, apply, and update-all.
# Dot-source: . (Join-Path $ScriptDir "lib\project-setup.ps1")

function Test-CodeGraphMcpInstalled {
    $mcpJson = Join-Path $env:USERPROFILE ".cursor\mcp.json"
    if (-not (Test-Path $mcpJson)) { return $false }
    return (Get-Content $mcpJson -Raw) -match 'codegraph'
}

function Ensure-CodeGraphMcp {
    $cg = Get-Command codegraph -ErrorAction SilentlyContinue
    if (-not $cg) {
        Write-Host "  [codegraph] CLI not on PATH -- skip MCP and index (https://github.com/colbymchenry/codegraph)"
        return $false
    }

    if (Test-CodeGraphMcpInstalled) { return $true }

    Write-Host "  [codegraph] Installing Cursor MCP config (global, one-time)..."
    & codegraph install --target=cursor --location=global --yes 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [codegraph] MCP wired in ~/.cursor/mcp.json -- restart Cursor to load"
        return $true
    }

    Write-Warning "  [codegraph] MCP install failed (exit $LASTEXITCODE). Run: codegraph install --target=cursor --location=global --yes"
    return $true
}

function Sync-ProjectCodeGraph {
    param([Parameter(Mandatory)][string]$ProjectPath)

    if (-not (Get-Command codegraph -ErrorAction SilentlyContinue)) {
        Write-Host "  [codegraph] CLI not on PATH -- skip index"
        return
    }

    $indexPath = Join-Path $ProjectPath ".codegraph"
    Push-Location $ProjectPath
    try {
        if (Test-Path $indexPath) {
            Write-Host "  [codegraph] Syncing index..."
            & codegraph sync 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  [codegraph] Index synced"
            } else {
                Write-Warning "  [codegraph] sync failed (exit $LASTEXITCODE)"
            }
        } else {
            Write-Host "  [codegraph] Building index..."
            & codegraph init 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  [codegraph] Index built at .codegraph/"
            } else {
                Write-Warning "  [codegraph] init failed (exit $LASTEXITCODE)"
            }
        }
    } finally {
        Pop-Location
    }
}

function Copy-ProjectGuardrails {
    param(
        [Parameter(Mandatory)][string]$ProjectPath,
        [Parameter(Mandatory)][string]$TemplateDir
    )

    $WorkflowSrc = Join-Path $TemplateDir ".github\workflows\agent-guardrails.yml"
    $WorkflowDestDir = Join-Path $ProjectPath ".github\workflows"
    $WorkflowDest = Join-Path $WorkflowDestDir "agent-guardrails.yml"
    if (-not (Test-Path $WorkflowDest)) {
        New-Item -ItemType Directory -Path $WorkflowDestDir -Force | Out-Null
        Copy-Item -Path $WorkflowSrc -Destination $WorkflowDest
        Write-Host "  [created]  .github/workflows/agent-guardrails.yml"
    } else {
        Write-Host "  [skipped]  .github/workflows/agent-guardrails.yml (already exists)"
    }
}
