#!/usr/bin/env python3
"""Post-generation tasks for go_template."""

import shutil
import sys
from pathlib import Path


def _read_answers(answers_file):
    """Parse the flat scalar answers copier just wrote.

    Deliberately not PyYAML: copier runs this with whatever python is on PATH.
    """
    answers = {}
    for line in answers_file.read_text().splitlines():
        if line.startswith(("#", " ", "-")) or ":" not in line:
            continue
        key, _, value = line.partition(":")
        answers[key.strip()] = value.strip().strip("'\"")
    return answers


def validate_answers():
    """Reject answers that contradict each other before they reach a real project.

    A project_name typo renders cleanly and stays wrong for months, because every
    later `copier update` reverts the hand-fixes it forces.
    """
    root = Path(__file__).parent
    answers = _read_answers(root / ".copier-answers.yml")
    project_name = answers.get("project_name", "")
    module_path = answers.get("module_path", "")
    namespace = answers.get("repository_namespace", "")

    errors = []
    if not module_path.endswith("/" + project_name):
        errors.append(
            f"module_path '{module_path}' must end with '/{project_name}'. "
            f"Fix whichever answer is misspelled: the two names drive cmd/, the "
            f"binary, the module import path, and the release artifacts separately, "
            f"so a mismatch leaves the project half-renamed.",
        )
    if namespace and "/" + namespace + "/" not in module_path:
        errors.append(
            f"module_path '{module_path}' does not contain repository_namespace "
            f"'{namespace}'. Set module_path to '<host>/{namespace}/{project_name}', "
            f"or correct repository_namespace so it matches where the repo lives.",
        )

    if errors:
        print("\nCopier answers are inconsistent:\n")
        for error in errors:
            print(f"  - {error}\n")
        sys.exit(1)


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

    for name in ("pyproject.toml", ".github/workflows/publish.yml"):
        path = root / name
        if path.exists() and not path.read_text().strip():
            path.unlink()
            print(f"Removed empty {name}")


def cleanup_removed_files():
    """Prune paths the template no longer renders.

    copier leaves a file in place once the template stops rendering it, so the
    manifest is the only way a `copier update` sheds one.
    """
    root = Path(__file__).parent
    manifest = root / "remove-if-found.txt"
    if not manifest.is_file():
        return
    for line in manifest.read_text().splitlines():
        target = root / line.strip()
        if not line.strip():
            continue
        if target.is_file():
            target.unlink()
            print(f"Removed {line.strip()}")
        elif target.is_dir():
            shutil.rmtree(target)
            print(f"Removed {line.strip()}/")
    manifest.unlink()


def cleanup_legacy_files():
    """Remove files superseded by the conf.d layout on copier update."""
    root = Path(__file__).parent
    legacy_tasks = root / ".config" / "mise.template.toml"
    if legacy_tasks.exists():
        legacy_tasks.unlink()
        print("Removed legacy .config/mise.template.toml (tasks now in .config/mise/conf.d/)")


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
    validate_answers()
    cleanup_conditional_files()
    cleanup_legacy_files()
    cleanup_removed_files()
    cleanup_cmd_directory()
    delete_myself()


if __name__ == "__main__":
    main()
