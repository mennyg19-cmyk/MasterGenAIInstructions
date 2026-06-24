# Shared project setup helpers for bootstrap, apply, and update-all.
# Source: source "$SCRIPT_DIR/lib/project-setup.sh"

codegraph_mcp_installed() {
    local mcp_json="${HOME}/.cursor/mcp.json"
    [ -f "$mcp_json" ] && grep -q 'codegraph' "$mcp_json"
}

ensure_codegraph_mcp() {
    if ! command -v codegraph &>/dev/null; then
        echo "  [codegraph] CLI not on PATH -- skip MCP and index (https://github.com/colbymchenry/codegraph)"
        return 1
    fi

    if codegraph_mcp_installed; then
        return 0
    fi

    echo "  [codegraph] Installing Cursor MCP config (global, one-time)..."
    if codegraph install --target=cursor --location=global --yes; then
        echo "  [codegraph] MCP wired in ~/.cursor/mcp.json -- restart Cursor to load"
    else
        echo "  [codegraph] MCP install failed. Run: codegraph install --target=cursor --location=global --yes" >&2
    fi
}

sync_project_codegraph() {
    local project_path="$1"

    if ! command -v codegraph &>/dev/null; then
        echo "  [codegraph] CLI not on PATH -- skip index"
        return
    fi

    if [ -d "$project_path/.codegraph" ]; then
        echo "  [codegraph] Syncing index..."
        if (cd "$project_path" && codegraph sync); then
            echo "  [codegraph] Index synced"
        else
            echo "  [codegraph] sync failed" >&2
        fi
    else
        echo "  [codegraph] Building index..."
        if (cd "$project_path" && codegraph init); then
            echo "  [codegraph] Index built at .codegraph/"
        else
            echo "  [codegraph] init failed" >&2
        fi
    fi
}

prune_orphan_project_rules() {
    local project_path="$1"
    local template_dir="$2"
    local rules_dest="$project_path/.cursor/rules"
    local rules_src="$template_dir/.cursor/rules"
    [ -d "$rules_dest" ] || return
    local removed=""
    for f in "$rules_dest"/*.mdc; do
        [ -f "$f" ] || continue
        base=$(basename "$f")
        [ "$base" = "deploy-awareness.mdc" ] && continue
        if [ ! -f "$rules_src/$base" ]; then
            rm -f "$f"
            removed="$removed $base"
        fi
    done
    if [ -n "$removed" ]; then
        echo "  [pruned]   removed stale rules:$removed"
    fi
}

copy_project_guardrails() {
    local project_path="$1"
    local template_dir="$2"
    local dest="$project_path/.github/workflows/agent-guardrails.yml"

    if [ ! -f "$dest" ]; then
        mkdir -p "$project_path/.github/workflows"
        cp "$template_dir/.github/workflows/agent-guardrails.yml" "$dest"
        echo "  [created]  .github/workflows/agent-guardrails.yml"
    else
        echo "  [skipped]  .github/workflows/agent-guardrails.yml (already exists)"
    fi
}
