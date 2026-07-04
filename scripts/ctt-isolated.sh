#!/usr/bin/env bash
set -euo pipefail

# Runs `ctt` against a clean, isolated git worktree instead of the live
# working tree, then copies the rendered `.ctt/*` output back.
#
# Why: copier's Worker uses vcs_ref="HEAD", and copier._vcs.clone() special-cases
# a dirty repo by staging the live work tree (--work-tree=<repo>) into a *different*
# throwaway git-dir and committing there. Running that against the real repo mid
# pre-commit (when the index is mid-write) has caused index/object-store corruption.
# A worktree checked out from a synthetic commit of the current index is always
# clean, so copier never takes that code path.

# pre-commit/prek export GIT_DIR, GIT_INDEX_FILE, GIT_WORK_TREE, etc. into the hook
# environment. Those leak into git commands run inside the linked worktree below,
# whose `.git` is a *file* (not a directory), producing
# `fatal: .git/index: index file open failed: Not a directory`. Clear them so every
# git invocation rediscovers the correct repo from its working directory.
unset GIT_DIR GIT_INDEX_FILE GIT_WORK_TREE GIT_OBJECT_DIRECTORY \
  GIT_COMMON_DIR GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_PREFIX GIT_CONFIG_PARAMETERS

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

tree="$(git write-tree)"
commit="$(git commit-tree "$tree" -p HEAD -m "ctt: isolated snapshot")"

worktree_dir="$(mktemp -d "${TMPDIR:-/tmp}/ctt-worktree.XXXXXX")"
cleanup() {
  git worktree remove --force "$worktree_dir" >/dev/null 2>&1 || rm -rf "$worktree_dir"
}
trap cleanup EXIT

git worktree add --detach --quiet "$worktree_dir" "$commit"

mapfile -t output_dirs < <(grep -oE '^\[output\."[^"]+"\]' ctt.toml | sed -E 's/^\[output\."([^"]+)"\]$/\1/')

set +e
(cd "$worktree_dir" && ctt --check-untracked "$@")
status=$?
set -e

for output_dir in "${output_dirs[@]}"; do
  mkdir -p "$repo_root/$output_dir"
  rsync -a --delete "$worktree_dir/$output_dir/" "$repo_root/$output_dir/"
done

# The worktree's `.git` is a file (linked worktree), not a directory, so copier's
# is_git_repo_root() check fails and it can't detect VCS info from within it.
# Normalize the resulting `_commit`/`_src_path` fields to match the deterministic
# values previously produced when ctt ran against the real repo directly.
python3 - "$repo_root" "${output_dirs[@]}" <<'PYEOF'
import os
import sys
from pathlib import Path

repo_root = Path(sys.argv[1])
for output_dir in sys.argv[2:]:
    answers = repo_root / output_dir / ".copier-answers.yml"
    if not answers.is_file():
        continue
    count_rel = len(answers.parent.relative_to(repo_root).parts)
    rel = "/".join([*([".."] * count_rel), repo_root.name])
    lines = [l for l in answers.read_text().splitlines(keepends=True)
             if not l.startswith("_commit:") and not l.startswith("_src_path:")]
    out = [lines[0], f"_commit: HEAD\n", f"_src_path: {rel}\n", *lines[1:]]
    answers.write_text("".join(out))
PYEOF

exit "$status"
