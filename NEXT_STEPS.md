# Next Steps

Open work for my_go_template and its children. Everything here was verified
against the repo on 2026-08-29, and anything that turned out to be done was
removed rather than marked done. Settled design choices live in
[docs/DECISIONS.md](docs/DECISIONS.md), and the per-change history lives in the
git log.

Template is at v0.12.1. Every child (`aragonite`, `djot-fmt`, `gh-lazydispatch`,
`gh-repo-dashboard`, `gh-star-search`, `gh-sweep`, `jj-diff`) is pinned at
v0.12.0, so one `copier update` per child picks up the concurrency guard on Bump
Version and the `.pre-commit-config.yaml` removal.

## Template repo

- The render no longer ships `.pre-commit-config.yaml`; `hk` owns the hooks and
  CI runs `hk check --all`. Children generated before v0.12.1 still have the
  file on disk, because `copier update` adds and patches files but never
  deletes them. Remove it by hand in each child
- Nothing formats TOML in this repo (this repo has no `hk.pkl` of its own), so
  the `.toml.jinja` sources and the committed `.ctt/` renders stay tombi-clean
  only by hand. The check is `tombi format --check` over `.ctt/**/*.toml` after a
  render; a local hk config here would automate it
- No `_migrations` exist in `copier.yml`. Every breaking layout change so far
  (the `.config/mise.toml` `[tools]` move at v0.5.0) needed a hand-sync in each
  child. This is the mechanism to reach for on the next one, and the
  `.pre-commit-config.yaml` removal above is the first case that could have
  used it
- `_skip_if_exists` silently swallows template changes to `README.md`,
  `DESIGN.md`, `.config/mise.toml`, `go.mod`, and `cmd/*/main.go`. Children
  never receive updates to any of them. Want a CI check or post-update note
  that diffs each against the `.ctt/default` render so the drift is visible
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

## Remaining project migrations

Every Go project that is going to adopt the template has, except one:

1. doner: adopt hooks and the strict golangci v2 config incrementally (expect
   many new findings), keep `action.yml` and the 80 percent coverage gate
   project-local

recipes stays out of scope: it is a mixed-language website with its own tooling.
The applicable subset is the golangci config and the hk builtins baseline, copied
by hand if wanted.
