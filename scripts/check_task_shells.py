#!/usr/bin/env python3
"""Fail on a mise task whose script needs bash but would run under sh.

mise runs an inline `run` script with `sh -o errexit -c` unless the task sets
`shell` or the script starts with a shebang. sh is bash in POSIX mode on macOS,
where `set -o pipefail` and `(( ))` both work, and dash on Ubuntu, where neither
does, so a task written on a Mac passes there and dies in CI and on every Linux
laptop with "Illegal option -o pipefail".

Usage: check_task_shells.py <mise toml>...
"""

import re
import sys
import tomllib
from pathlib import Path

# Syntax dash rejects. Each is anchored loosely on purpose: a false positive costs
# one `shell = "bash -c"`, and a miss costs a broken task in every child.
BASHISMS = {
    "set -o pipefail": re.compile(r"\bpipefail\b"),
    "(( ))": re.compile(r"\(\("),
    "[[ ]]": re.compile(r"\[\["),
    "process substitution": re.compile(r"[<>]\("),
    "$'...' quoting": re.compile(r"\$'"),
}


def _scripts(task):
    run = task.get("run", [])
    for step in [run] if isinstance(run, str) else run:
        if isinstance(step, str):
            yield step


def _runs_bash(shell):
    argv = shell.split()
    return bool(argv) and (Path(argv[0]).name == "bash" or argv[:2] == ["/usr/bin/env", "bash"])


def problems(path):
    tasks = tomllib.loads(Path(path).read_text()).get("tasks", {})
    for name, task in tasks.items():
        if not isinstance(task, dict):
            continue
        if _runs_bash(task.get("shell", "")):
            continue
        for script in _scripts(task):
            if script.lstrip().startswith("#!"):
                continue
            found = [label for label, pattern in BASHISMS.items() if pattern.search(script)]
            if found:
                yield f'{path}: task "{name}" uses {", ".join(found)} without shell = "bash -c"'


def main(paths):
    failures = [problem for path in paths for problem in problems(path)]
    for failure in failures:
        print(failure, file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
