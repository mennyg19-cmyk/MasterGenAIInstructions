#!/usr/bin/env bash
# === What's in this file ===
# Bootstrap script that creates a new project from the MasterGenAIInstructions template.
#
# Main flow:
#   1. Prompt for project name, description, destination, GitHub preference
#   2. Copy template/ into the destination
#   3. Replace {{PROJECT_NAME}} and {{DESCRIPTION}} placeholders
#   4. Initialize git
#   5. Optionally create a private GitHub repo and push

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/template"

if [ ! -d "$TEMPLATE_DIR" ]; then
    echo "Error: Template directory not found at $TEMPLATE_DIR" >&2
    exit 1
fi

PROJECT_NAME="${1:-}"
if [ -z "$PROJECT_NAME" ]; then
    read -rp "Project name: " PROJECT_NAME
fi

if [ -z "$PROJECT_NAME" ]; then
    echo "Error: Project name is required." >&2
    exit 1
fi

read -rp "Description (one line): " DESCRIPTION

DEFAULT_DEST="$(pwd)/$PROJECT_NAME"
read -rp "Destination directory (default: $DEFAULT_DEST): " DESTINATION
DESTINATION="${DESTINATION:-$DEFAULT_DEST}"

if [ -d "$DESTINATION" ]; then
    echo "Error: Destination already exists: $DESTINATION" >&2
    exit 1
fi

echo ""
echo "Creating project: $PROJECT_NAME"
echo "Description:      $DESCRIPTION"
echo "Destination:      $DESTINATION"
echo ""

cp -r "$TEMPLATE_DIR" "$DESTINATION"

find "$DESTINATION" -type f \( -name "*.md" -o -name "*.mdc" \) -exec sed -i'' \
    -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
    -e "s/{{DESCRIPTION}}/$DESCRIPTION/g" \
    {} +

cd "$DESTINATION"
git init -b main
git add -A
git commit -m "Initial project scaffold from MasterGenAIInstructions"

read -rp "Create private GitHub repo? (y/n, default: y): " CREATE_REPO
if [ "${CREATE_REPO:-y}" != "n" ]; then
    if command -v gh &>/dev/null; then
        gh repo create "$PROJECT_NAME" --private --source . --push
        echo ""
        echo "GitHub repo created and pushed."
    else
        echo "Warning: gh CLI not found. Install it to auto-create GitHub repos: https://cli.github.com"
        echo "You can push manually later."
    fi
fi

echo ""
echo "Done! Your project is ready at: $DESTINATION"
echo ""
echo "Next steps:"
echo "  1. Open $DESTINATION in Cursor"
echo "  2. Fill in .cursor/rules/deploy-awareness.mdc with your deploy targets"
echo "  3. Start building -- agents already know your workflow"
