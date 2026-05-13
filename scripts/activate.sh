#!/usr/bin/env bash
# activate.sh — Initialize a project to use the agent framework
#
# Usage: bash /path/to/agent-framework/scripts/activate.sh [project-dir]
#
# What it does:
#   1. Creates a .agent/ directory in the project
#   2. Copies CLAUDE.md into the project root (or merges if one exists)
#   3. Creates a starter Architecture Brief for the first project

set -euo pipefail

FRAMEWORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_DIR="${1:-$(pwd)}"

echo "Activating agent framework in: $PROJECT_DIR"
echo "Framework source: $FRAMEWORK_DIR"
echo ""

# Create .agent/ directory for project-level artifacts
mkdir -p "$PROJECT_DIR/.agent"

cat > "$PROJECT_DIR/.agent/README.md" << 'EOF'
# .agent/

Project-level artifacts for the agent orchestration framework.

## Structure
- `briefs/`    — Architecture Briefs (one per project/post)
- `packages/`  — Analyst Review Packages
- `qa/`        — QA Reports
- `close/`     — Close Reports

Artifacts are named by project slug, e.g. `briefs/mtg-legacy-tournament.md`.
EOF

mkdir -p "$PROJECT_DIR/.agent/briefs"
mkdir -p "$PROJECT_DIR/.agent/packages"
mkdir -p "$PROJECT_DIR/.agent/qa"
mkdir -p "$PROJECT_DIR/.agent/close"

# Copy or merge CLAUDE.md
if [ -f "$PROJECT_DIR/CLAUDE.md" ]; then
  echo "CLAUDE.md already exists in project. Appending framework section."
  echo "" >> "$PROJECT_DIR/CLAUDE.md"
  echo "---" >> "$PROJECT_DIR/CLAUDE.md"
  echo "" >> "$PROJECT_DIR/CLAUDE.md"
  cat "$FRAMEWORK_DIR/CLAUDE.md" >> "$PROJECT_DIR/CLAUDE.md"
  echo "Appended to: $PROJECT_DIR/CLAUDE.md"
else
  cp "$FRAMEWORK_DIR/CLAUDE.md" "$PROJECT_DIR/CLAUDE.md"
  echo "Created: $PROJECT_DIR/CLAUDE.md"
fi

echo ""
echo "Done. Next steps:"
echo "  1. Tell Claude: 'New project: [your project name]'"
echo "  2. Claude will activate the Architect role and produce an Architecture Brief"
echo "  3. Confirm the brief, then say 'start working'"
