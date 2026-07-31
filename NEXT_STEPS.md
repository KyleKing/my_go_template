# Next Steps

Open work for my_go_template and its children. Everything here was verified
against the repo on 2026-07-27; anything that turned out to be done was removed
rather than marked done. The append-only pass log lives in `.freshen.md`.

Template is at v0.9.0. All five children (`gh-sweep`, `gh-repo-dashboard`,
`gh-star-search`, `gh-lazydispatch`, `jj-diff`) are pinned at v0.7.0, so the
v0.8.0/v0.9.0 hook and validation work has not reached any of them yet.

## Template repo

- The child render still ships both `hk.pkl` and a full `.pre-commit-config.yaml`.
  CI now runs `hk check --all`, so the pre-commit config is the odd one out and
  should be dropped from `go_template/`. Verify with
  `ls go_template/.pre-commit-config.yaml.jinja go_template/hk.pkl.jinja`
- Nothing formats TOML in this repo (this repo has no `hk.pkl` of its own), so
  the `.toml.jinja` sources and the committed `.ctt/` renders stay tombi-clean
  only by hand. The check is `tombi format --check` over `.ctt/**/*.toml` after a
  render; a local hk config here would automate it
- No `_migrations` exist in `copier.yml`. Every breaking layout change so far
  (the `.config/mise.toml` `[tools]` move at v0.5.0) needed a hand-sync in each
  child. This is the mechanism to reach for on the next one
- `_skip_if_exists` silently swallows template changes to `README.md`,
  `AGENTS.md`, `DESIGN.md`, `.config/mise.toml`, `go.mod`, and `cmd/*/main.go`.
  Children never receive updates to any of them. Want a CI check or post-update
  note that diffs each against the `.ctt/default` render so the drift is visible
- `ctt` renders in place. `sync_with_ctt.sh` clears `.ctt/*/` first, but the
  `copier-template-tester` pre-commit hook still renders in place and reports a
  stale tree as current. The real fix is upstream in copier-template-tester
- Dependabot cannot read the action pins inside `go_template/**/*.jinja`, so the
  SHAs this template ships are bumped by hand. Deferred deliberately: pointing
  Dependabot at `.ctt/default` would open PRs against generated output that the
  next `ctt` run reverts. A real fix is a script that rewrites the jinja sources
  from a child's merged bump
- The commitizen-action step in `bump_version.yml.jinja` builds a Docker image on
  every Bump Version run and failed once on a Docker Hub timeout. A pipx install
  would remove the registry dependency
- `mise run demo` needs vhs, deliberately not pinned in `[tools]` because the CI
  `hooks` job would then install it on every run. Recorded as a manual
  prerequisite in `CONTRIBUTING.md.jinja`

### Upstream from projects

- `testdata/` plus `internal/testutil/` scaffolding and a binary-build
  integration test stub, modeled on djot-fmt. Neither exists in the render today
- `test:integration` task naming from gh-lazydispatch. `bench`, `test`, and
  `test:coverage-min` are in `conf.d/template.toml.jinja`; `test:integration` is
  not. Either add it or document it as the expected project-local extension
- Consider an opt-in copier question for a composite `action.yml` (doner's
  GitHub Action distribution pattern)

## Child fallout, pending their v0.7.0 → v0.9.0 update

The new CI `hooks` job turns four children red on their first update, each on a
real finding. Fix each in the child, not by relaxing the template.

- gh-lazydispatch: shellcheck SC2044 in `scripts/check-test-safety.sh`
- jj-diff: `check-merge-conflict` fails on `.jj-diff-roadmap.md`, which documents
  conflict markers as content. Needs a project-local `exclude` on that step, the
  first case of a child legitimately overriding a template hook
- jj-diff: `typos` flags deliberate fixture strings in
  `internal/fuzzy/fuzzy_test.go`. The fix is a project-local
  `[default.extend-words]` in its `.typos.toml`; the template file is the base
  and children extend it
- gh-star-search: 1 typo in `internal/python/scripts/evaluate_embeddings.py`
- gh-sweep and gh-repo-dashboard had their notes-file typos fixed on 2026-07-27
  and should now be clean, but neither has been re-measured against the v0.9.0
  hook set
- `AGENTS.md` is in `_skip_if_exists`, so no child picks up the v0.9.0+ rewrite.
  Bring the five toward it by hand, keeping each one's real local content (the
  package tree, and jj-diff's TUI section). `CLAUDE.md` is not skipped, so
  gh-star-search and jj-diff get the `@AGENTS.md` bridge automatically; without
  it Claude Code was never loading their `AGENTS.md` at all
- gh-star-search and gh-lazydispatch still carry the pre-v0.6 `AGENTS.md` shape
  (`### Package Guidelines`, `### File Organization`), so their diff against the
  new seed is the largest

## Remaining project migrations

gh-sweep, gh-repo-dashboard, gh-star-search, gh-lazydispatch, and jj-diff have
all adopted the template. What is left:

1. djot-fmt: run `copier copy` to retrofit, drop the redundant Makefile, move
   root `main.go` to `cmd/djot-fmt/`, add CI and releases, remove the committed
   binary
2. doner: adopt hooks and the strict golangci v2 config incrementally (expect
   many new findings), keep `action.yml` and the 80 percent coverage gate
   project-local

recipes stays out of scope: it is a mixed-language website with its own tooling.
The applicable subset is the golangci config and the hk builtins baseline, copied
by hand if wanted.
