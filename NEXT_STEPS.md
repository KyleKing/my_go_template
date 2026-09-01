# Next Steps

Open work for my_go_template and its children. Everything here was verified
against the repo on 2026-09-01, and anything that turned out to be done was
removed rather than marked done. Settled design choices live in
[docs/DECISIONS.md](docs/DECISIONS.md), and the per-change history lives in the
git log.

Every child is behind the current release. `wavez` is the closest at v0.14.1.
`gh-lazydispatch`, `gh-repo-dashboard`, and `gh-sweep` sit at v0.13.1, and
`aragonite`, `djot-fmt`, `gh-star-search`, `jj-diff`, and `second-look` at
v0.13.0. One `copier update` per child picks up the doneram tool bumps and the
Dependabot ignore for the untagged `charmbracelet/x` submodules. Expect a
`hk fix --all` in the same commit, per the golines note below. `what-did-ai-do`
records `_src_path` as this template but pins `v0.3.2`, which is not a tag in
this series and needs a look.

## Template repo

- golangci-lint 2.13.2 deprecates the gofumpt `extra-rules` key that
  `.golangci.toml.jinja` sets, so every child prints a warning on every format
  run. `extra.group-params` is the named replacement and silences it, but the
  two are not equivalent: measured against wavez, `extra-rules` differs from
  plain gofumpt by 31 diff lines and `group-params` by 12, so the swap relaxes a
  rule and reformats multiline call sites. Taking it means a deliberate
  reformat commit in every child, which is why it is not done yet
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
- The commitizen-action step in `bump_version.yml.jinja` builds a Docker image on
  every Bump Version run and failed once on a Docker Hub timeout. A pipx install
  would remove the registry dependency
- `mise run demo` needs vhs, deliberately not pinned in `[tools]` because the CI
  `hooks` job would then install it on every run. Recorded as a manual
  prerequisite in `CONTRIBUTING.md.jinja`
- A golangci-lint bump reformats a whole child, because golines' wrapping moves
  with it. 2.12.2 to 2.13.2 rewrapped 18 files in wavez. Run `hk fix --all`
  in the same commit as the `copier update` rather than leaving the churn to
  surface in the next unrelated change
- `docs/troubleshooting.md` is template-owned, so a project-specific entry
  appended to it conflicts on the next update. The render now carries a
  `docs/troubleshooting.local.md` pointer for that; wavez was the first child to
  hit the conflict and move its entry across

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
