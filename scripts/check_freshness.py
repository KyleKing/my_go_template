"""Check my_go_template's pinned GitHub Action versions and standalone tool pins for drift.

Action-pin convention: `uses: owner/repo@<40-char sha> # v<tag>` in workflow files. The same
action is pinned identically across the root repo's own workflows and the jinja-templated
workflows shipped to generated projects (go_template/.github/workflows/*.jinja); a drifted
pin is patched in every file where it's found.

Standalone pins: `hk` is report-only, since its version repeats five times. `golangci-lint` is pinned twice, as a mise
tool version in go_template/.config/mise/conf.d/template.toml.jinja and as a `version:` for
golangci-lint-action in go_template/.github/workflows/ci.yml.jinja, and the two must agree.
"""

import logging
import re
import sys
from pathlib import Path

from freshness.checkers import (
    CheckResult,
    extract_pin,
    fetch_github_commit,
    fetch_github_release,
    is_outdated,
    patch_pin,
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

TEMPLATE_HK_PKL = REPO_ROOT / "go_template" / "hk.pkl.jinja"
TEMPLATE_TASKS_TOML = REPO_ROOT / "go_template" / ".config" / "mise" / "conf.d" / "template.toml.jinja"
TEMPLATE_CI_YML = REPO_ROOT / "go_template" / ".github" / "workflows" / "ci.yml.jinja"


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


def check_standalone_pins() -> list[CheckResult]:
    """Check the hk and golangci-lint version pins against their latest upstream releases.

    Returns:
        One CheckResult per pin, in file order.

    """
    results = []

    current_hk = extract_pin(TEMPLATE_HK_PKL, r'min_hk_version = "([^"]+)"')
    latest_hk = fetch_github_release("jdx", "hk")
    if current_hk and latest_hk:
        results.append(
            CheckResult(
                "hk",
                str(TEMPLATE_HK_PKL.relative_to(REPO_ROOT)),
                current_hk,
                latest_hk,
                is_outdated(current_hk, latest_hk),
                note="report-only: the version repeats five times across hk.pkl.jinja and the mise pins, "
                "which patch_pin cannot rewrite together; doneram patches all five from .doneram.pkl",
            )
        )

    current_lint = extract_pin(TEMPLATE_TASKS_TOML, r'"golangci-lint"\s*=\s*"([^"]+)"')
    ci_lint = extract_pin(TEMPLATE_CI_YML, r"version:\s*v([\w.\-]+)")
    latest_lint = fetch_github_release("golangci", "golangci-lint")
    if current_lint and ci_lint and current_lint != ci_lint:
        results.append(
            CheckResult(
                "golangci-lint",
                str(TEMPLATE_CI_YML.relative_to(REPO_ROOT)),
                ci_lint,
                current_lint,
                drifted=True,
                note="the ci.yml action pin disagrees with the mise tool pin; set both to the same version",
            )
        )
    if current_lint and latest_lint:
        drifted = is_outdated(current_lint, latest_lint)
        if drifted:
            patch_pin(
                TEMPLATE_TASKS_TOML, f'"golangci-lint" = "{current_lint}"', f'"golangci-lint" = "{latest_lint}"'
            )
            patch_pin(TEMPLATE_CI_YML, f"version: v{current_lint}", f"version: v{latest_lint}")
        results.append(
            CheckResult(
                "golangci-lint",
                str(TEMPLATE_TASKS_TOML.relative_to(REPO_ROOT)),
                current_lint,
                latest_lint,
                drifted,
                note=f"also pinned as `version: v{latest_lint}` in {TEMPLATE_CI_YML.relative_to(REPO_ROOT)}",
            )
        )

    return results


def main() -> int:
    """Run both freshness checks and return a process exit code.

    Returns:
        0 if nothing drifted, 1 if any check found drift (files are patched in place regardless).

    """
    results = check_action_pins() + check_standalone_pins()
    logger.info(render_report(results))
    return 1 if any(result.drifted for result in results) else 0


if __name__ == "__main__":
    sys.exit(main())
