"""Check my_go_template's pinned GitHub Action versions for drift.

Action-pin convention: `uses: owner/repo@<40-char sha> # v<tag>` in workflow files. The same
action is pinned identically across the root repo's own workflows and the jinja-templated
workflows shipped to generated projects (go_template/.github/workflows/*.jinja); a drifted
pin is patched in every file where it's found.

doneram (.doneram.pkl) now owns every mise-backed tool pin, including hk's five-way patch and
golangci-lint's cross-file agreement; this script only covers the SHA+tag action pins doneram's
locator can't yet express, since patching them means resolving a tag and then looking up that
tag's commit SHA rather than reading one version literal.
"""

import logging
import re
import sys
from pathlib import Path

from freshness.checkers import (
    CheckResult,
    fetch_github_commit,
    fetch_github_release,
    is_outdated,
    render_report,
)

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent

ACTION_FILES = [
    REPO_ROOT / ".github" / "workflows" / "ci.yml",
    REPO_ROOT / ".github" / "workflows" / "bump_version.yml",
    REPO_ROOT / "go_template" / ".github" / "workflows" / "ci.yml.jinja",
    REPO_ROOT / "go_template" / ".github" / "workflows" / "bump_version.yml.jinja",
]

ACTION_PIN_PATTERN = re.compile(r"uses:\s*([\w.\-]+/[\w.\-]+)@([0-9a-f]{40})\s*#\s*v([\w.\-]+)")


def check_action_pins() -> list[CheckResult]:
    """Check every `uses: owner/repo@sha # vtag` pin across root and templated workflows.

    Uses each action's first occurrence across ACTION_FILES as the "current" pin, then patches
    that literal `action@sha # vtag` string everywhere it appears if a newer release exists.

    Returns:
        One CheckResult per unique action found.

    """
    pins: dict[str, tuple[str, str]] = {}
    for file_path in ACTION_FILES:
        if not file_path.exists():
            continue
        for match in ACTION_PIN_PATTERN.finditer(file_path.read_text(encoding="utf-8")):
            action, sha, tag = match.groups()
            pins.setdefault(action, (sha, tag))

    results = []
    for action, (sha, tag) in pins.items():
        owner, repo = action.split("/", 1)
        latest_tag = fetch_github_release(owner, repo)
        if not latest_tag:
            logger.warning("Could not fetch latest release for %s", action)
            continue
        drifted = is_outdated(tag, latest_tag)
        if drifted:
            latest_sha = fetch_github_commit(owner, repo, f"v{latest_tag}")
            if latest_sha:
                old = f"{action}@{sha} # v{tag}"
                new = f"{action}@{latest_sha} # v{latest_tag}"
                for file_path in ACTION_FILES:
                    if file_path.exists() and old in file_path.read_text(encoding="utf-8"):
                        file_path.write_text(
                            file_path.read_text(encoding="utf-8").replace(old, new), encoding="utf-8"
                        )
        results.append(CheckResult(action, "workflows", tag, latest_tag, drifted))
    return results


def main() -> int:
    """Run the action-pin freshness check and return a process exit code.

    Returns:
        0 if nothing drifted, 1 if any check found drift (files are patched in place regardless).

    """
    results = check_action_pins()
    logger.info(render_report(results))
    return 1 if any(result.drifted for result in results) else 0


if __name__ == "__main__":
    sys.exit(main())
