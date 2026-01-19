#!/bin/bash -e

# Convenience script to sync latest .ctt configuration files with the top-level template

cp .ctt/default/.editorconfig go_template/.editorconfig
cp .ctt/default/.cz.toml .cz.toml

echo 'FYI: Occasionally sync the pre-commit config, but requires manual review:'
echo '  cp .ctt/default/.pre-commit-config.yaml .pre-commit-config.yaml'
echo 'and sync updated versions in reverse:'
echo '  cp .pre-commit-config.yaml go_template/.pre-commit-config.yaml.jinja'
