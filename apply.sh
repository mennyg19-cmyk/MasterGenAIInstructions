#!/usr/bin/env bash
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

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/template"
# shellcheck source=lib/project-setup.sh
source "$SCRIPT_DIR/lib/project-setup.sh"

if [ ! -d "$TEMPLATE_DIR" ]; then
    echo "Error: Template directory not found at $TEMPLATE_DIR" >&2
    exit 1
fi

TARGET_DIR="${1:-}"
if [ -z "$TARGET_DIR" ]; then
    read -rp "Path to existing project: " TARGET_DIR
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory does not exist: $TARGET_DIR" >&2
    exit 1
fi

echo ""
echo "Applying MasterGenAIInstructions to: $TARGET_DIR"
echo ""

mkdir -p "$TARGET_DIR/.cursor/rules"
cp "$TEMPLATE_DIR/.cursor/rules/"* "$TARGET_DIR/.cursor/rules/"
prune_orphan_project_rules "$TARGET_DIR" "$TEMPLATE_DIR"
echo "  [copied]   .cursor/rules/ (all rule files)"

cp "$TEMPLATE_DIR/AGENTS.md" "$TARGET_DIR/AGENTS.md"
echo "  [copied]   AGENTS.md"

for file in DECISION-LOG.md TESTING-STRATEGY.md HANDOFF.md; do
    if [ ! -f "$TARGET_DIR/$file" ]; then
        cp "$TEMPLATE_DIR/$file" "$TARGET_DIR/$file"
        echo "  [created]  $file"
    else
        echo "  [skipped]  $file (already exists)"
    fi
done

echo "  [skipped]  README.md (not overwriting existing project file)"
echo "  [skipped]  .gitignore (not overwriting existing project file)"

# Register the project for future updates
REGISTRY_FILE="$SCRIPT_DIR/registry.json"
FULL_PATH="$(cd "$TARGET_DIR" && pwd)"
if command -v python3 &>/dev/null; then
    REGISTERED=$(python3 - "$REGISTRY_FILE" "$FULL_PATH" <<'PY'
import json, sys
from pathlib import Path
registry_file, full_path = Path(sys.argv[1]), sys.argv[2]
registry = json.loads(registry_file.read_text()) if registry_file.exists() else []
if full_path not in registry:
    registry.append(full_path)
    registry_file.write_text(json.dumps(registry, indent=2))
    print("yes")
PY
)
    if [ "$REGISTERED" = "yes" ]; then
        echo "  [registered] Project added to registry for future rule updates."
    fi
fi

NO_GUARDRAILS="${NO_GUARDRAILS:-0}"
if [ "$NO_GUARDRAILS" != "1" ]; then
    copy_project_guardrails "$TARGET_DIR" "$TEMPLATE_DIR"
fi

ensure_codegraph_mcp || true
sync_project_codegraph "$TARGET_DIR"

echo ""
echo "Done! Rules applied to: $TARGET_DIR"
echo ""
echo "Next steps:"
echo "  1. Fill in .cursor/rules/deploy-awareness.mdc with your deploy targets"
echo "  2. Review AGENTS.md to make sure it fits this project"
if [ "$NO_GUARDRAILS" != "1" ]; then
    echo "  3. Review .github/workflows/agent-guardrails.yml -- tune or remove jobs as needed"
    echo "  4. Commit the new files"
else
    echo "  3. Commit the new files"
fi
