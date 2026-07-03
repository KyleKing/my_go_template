#!/usr/bin/env python3
"""Post-generation tasks for go_template."""

import shutil
from pathlib import Path


def cleanup_conditional_files():
    """Remove files that were conditionally excluded."""
    root = Path(__file__).parent

    goreleaser = root / ".goreleaser.yml"
    if goreleaser.exists():
        content = goreleaser.read_text().strip()
        if not content:
            goreleaser.unlink()
            print("Removed empty .goreleaser.yml")

    release_workflow = root / ".github" / "workflows" / "release.yml"
    if release_workflow.exists() and not goreleaser.exists():
        release_workflow.unlink()
        print("Removed release.yml (no goreleaser)")

    formula_dir = root / "Formula"
    if formula_dir.exists() and not goreleaser.exists():
        shutil.rmtree(formula_dir)
        print("Removed Formula/ (no goreleaser)")


def cleanup_cmd_directory():
    """Remove cmd/ directory for library projects."""
    root = Path(__file__).parent
    cmd_dir = root / "cmd"
    if cmd_dir.exists():
        main_files = list(cmd_dir.rglob("main.go"))
        if main_files and not main_files[0].read_text().strip():
            shutil.rmtree(cmd_dir)
            print("Removed empty cmd/ directory (library project)")


def delete_myself():
    """Remove this script after execution."""
    Path(__file__).unlink()


def main():
    cleanup_conditional_files()
    cleanup_cmd_directory()
    delete_myself()


if __name__ == "__main__":
    main()
