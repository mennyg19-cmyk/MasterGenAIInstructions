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
echo "  [copied]   .cursor/rules/ (13 rule files)"

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

echo ""
echo "Done! Rules applied to: $TARGET_DIR"
echo ""
echo "Next steps:"
echo "  1. Fill in .cursor/rules/deploy-awareness.mdc with your deploy targets"
echo "  2. Review AGENTS.md to make sure it fits this project"
echo "  3. Commit the new files"
