#!/bin/bash -e

# Sync latest .ctt configuration files with the top-level template
# and verify the generated template works correctly

CTT_DIR=".ctt/default"

echo "==> Syncing configuration files..."
cp "$CTT_DIR/.editorconfig" go_template/.editorconfig

echo "==> Installing tools in $CTT_DIR..."
(cd "$CTT_DIR" && mise install)

echo "==> Running CI checks in $CTT_DIR..."
(cd "$CTT_DIR" && mise run ci)

echo "==> Running linter in $CTT_DIR..."
(cd "$CTT_DIR" && mise run lint)

echo ""
echo "All checks passed!"
echo ""
echo "FYI: Occasionally sync the pre-commit config, but requires manual review:"
echo "  cp $CTT_DIR/.pre-commit-config.yaml .pre-commit-config.yaml"
echo "and sync updated versions in reverse:"
echo "  cp .pre-commit-config.yaml go_template/.pre-commit-config.yaml.jinja"
