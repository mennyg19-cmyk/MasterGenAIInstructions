# Commit with a multi-line message from PowerShell (no bash heredoc, no temp file).
# Usage:
#   .\lib\git-commit.ps1 -Subject "Fix login redirect" -Body "Return URL was dropped on OAuth callback."
#   .\lib\git-commit.ps1 -Subject "One-line only"

param(
    [Parameter(Mandatory)]
    [string]$Subject,
    [string]$Body
)

if ($Body) {
    git commit -m $Subject -m $Body
} else {
    git commit -m $Subject
}

if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
