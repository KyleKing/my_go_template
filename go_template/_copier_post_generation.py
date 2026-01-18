#!/usr/bin/env python3
"""Post-generation tasks for go_template."""

from pathlib import Path
import subprocess
import sys


def cleanup_conditional_files():
    """Remove files that were conditionally excluded."""
    root = Path(".")

    # Remove goreleaser if not a CLI project or use_goreleaser is false
    goreleaser = root / ".goreleaser.yml"
    if goreleaser.exists():
        content = goreleaser.read_text().strip()
        if not content:
            goreleaser.unlink()
            print("Removed empty .goreleaser.yml")

    # Remove release workflow if goreleaser was removed
    release_workflow = root / ".github" / "workflows" / "release.yml"
    if release_workflow.exists() and not goreleaser.exists():
        release_workflow.unlink()
        print("Removed release.yml (no goreleaser)")


def run_go_mod_init():
    """Initialize go.mod if it doesn't exist."""
    go_mod = Path("go.mod")
    if not go_mod.exists():
        print("Note: Run 'go mod init <module_path>' to initialize the module")


def delete_myself():
    """Remove this script after execution."""
    Path(__file__).unlink()


def main():
    cleanup_conditional_files()
    run_go_mod_init()
    delete_myself()


if __name__ == "__main__":
    main()
