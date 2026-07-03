# Go Project Audit and my_go_template Improvement Plan

Date: 2026-07-03. Audit of seven Go projects and the template itself, using calcipy_template as the quality bar.

## Problem

my_go_template is partially adopted (2 of 7 projects), has several broken or contradictory pieces, and lags calcipy_template on self-testing, migrations, and post-generation validation. The Go projects have independently evolved practices worth upstreaming, and several hand-rolled projects could migrate once the template is trustworthy.

## Project status summary

| Project | From template | Maturity | Hooks | mise | CI | Release |
|---|---|---|---|---|---|---|
| gh-lazydispatch | yes (v0.2.2) | mid-dev, strong tests | hk | layered | yes +4 extra | goreleaser+brew |
| gh-star-search | yes (v0.2.2) | mature, 38 test files | hk | layered, drifted | yes (dup ci.yaml) | goreleaser+brew |
| djot-fmt | no | complete, narrow scope | hk + Makefile | single file | none | none |
| doner | no | near-complete | none | single file | yes, 80% cov gate | goreleaser + action.yml |
| gh-repo-dashboard | no | functional WIP | none | none | hand-written | manual matrix |
| gh-sweep | no | MVP complete | none | stale (go 1.21 pin) | yes | none |
| recipes | no (not a fit) | mature website | hk (custom) | rich, domain tasks | deploy only | n/a |

Notes per project:

- gh-lazydispatch is the healthiest template consumer. Drift is additive (extra workflows, demo tooling, bench/integration tasks). Pinned at template v0.2.2
- gh-star-search carries a generation typo (`project_name: gh-start-search`) so `cmd/gh-start-search/`, the Formula, and build targets mismatch the real module path. Also has an orphaned duplicate `ci.yaml` and a hand-edited `mise.template.toml` (which copier should own)
- djot-fmt is hand-rolled but closest in spirit: hk + mise + strict golangci. Redundant Makefile shim, no CI, no release pipeline, committed binary, root main.go
- doner has the best CI discipline (80% coverage floor) and a composite `action.yml` distribution pattern, but no hooks, a minimal v1-style `.golangci.yml`, and none of the template docs (AGENTS.md, CONTRIBUTING.md)
- gh-repo-dashboard has almost no shared tooling (no mise, hooks, lint config, editorconfig) and a manual cross-compile release matrix. Highest-value migration target
- gh-sweep has a self-contained mise config with a stale go pin and deliberately weakened lint config. No hooks, no release tooling
- recipes is a mixed-language website (Go + templ + CGO/spaCy + Python + JS). It should never adopt the template wholesale. The applicable subset is the golangci config, hk builtins baseline, and editorconfig/gitattributes

## Template health (my_go_template itself)

Broken or contradictory today:

- README advertises a `workspace` project type that `copier.yml` does not offer. `ci.yml.jinja` contains dead `project_type == "workspace"` branches that can never run
- `sync_with_ctt.sh` aborts: it copies `.ctt/default/.cz.toml`, which is never generated
- Generated projects get commitizen hooks (hk.pkl, pre-commit) but no `.cz.toml` and no version-bump workflow, so the versioning story is half-wired
- `module_path` is collected but no `go.mod` is generated, so fresh projects do not build until a manual `go mod init`
- `.golangci.toml.jinja` references linters removed or renamed in golangci-lint v2 (gomnd, execinquery, exportloopref, gosimple, stylecheck, typecheck)
- Only one ctt fixture (`cli` + goreleaser). The `library` and `use_goreleaser=false` paths are never exercised
- No CI on the template repo beyond `bump_version.yml`. Nothing generates fixtures and runs `go build`/`go vet` against them
- README variable table is stale (missing five variables, wrong project_type choices)
- Post-generation cleanup relies on detecting empty rendered files, which is fragile compared to calcipy's `remove-if-found.txt` manifest
- Version pins duplicated between `hk.pkl` and `mise.hk.toml`

## What calcipy_template has that this lacks

- Migration machinery run from `_tasks` that upgrades pre-template projects and self-deletes
- A rendered `remove-if-found.txt` manifest so `copier update` can prune obsolete files
- Post-generation validation that cross-checks derived answers and exits nonzero on mismatch
- Programmatic config sync (tomlkit script) instead of shell `cp`
- Multiple ctt fixtures covering conditional branches
- Richer generated scaffolding (tests dir, issue templates, docs)

## Decision: what the template should enforce

The template targets releasable single-binary CLI tools and libraries. It should enforce, not accommodate:

- `cmd/<name>/main.go` layout (djot-fmt, gh-sweep, gh-repo-dashboard would move their root main.go on migration)
- hk + layered mise config, no Makefile
- golangci-lint v2 with the strict curated config
- goreleaser + Formula for CLI projects, nothing manual
- A working versioning loop (commitizen config + bump workflow) in generated projects

recipes stays out of scope. doner's `action.yml` pattern and demo/VHS tooling stay project-local for now (candidates for future opt-in questions).

## Prioritized changes

Items 1 through 11 below were implemented on 2026-07-03 (see CHANGELOG.md Unreleased). Items 12 and 13 and the migration wave remain open. Item 9 was partially done: post-generation cleanup was extended to remove the empty Formula/ directory, but the remove-if-found.txt manifest and answer validation are still open.

Fix-now (broken or misleading):

1. Remove all `workspace` references (README, ci.yml.jinja dead branches)
2. Fix `sync_with_ctt.sh` so it runs cleanly and only syncs files that exist
3. Generate `.cz.toml.jinja` and a `bump_version.yml` workflow for downstream projects to complete the commitizen wiring
4. Generate `go.mod.jinja` from `module_path` so projects build immediately
5. Audit `.golangci.toml.jinja` for golangci-lint v2 (drop removed linters)
6. Correct the README variable table

Robustness (calcipy parity):

7. Add ctt fixtures for `library` and `cli` without goreleaser
8. Add a template CI workflow that generates each fixture and runs `go vet`/`go build`
9. Replace empty-file post-gen cleanup with a `remove-if-found.txt` manifest and add answer validation
10. Centralize duplicated version pins

Upstream from projects:

11. Coverage floor task (`test:coverage-min`, threshold var) and CI gate, from doner/gh-star-search
12. `testdata/` + `internal/testutil/` scaffolding and a binary-build integration test stub, from djot-fmt
13. Integration/bench task naming conventions (`test:integration`, `bench:*`), from gh-lazydispatch

Migration wave (after the above land, roughly in order of payoff):

- gh-repo-dashboard (gets everything: mise, hooks, lint, goreleaser)
- djot-fmt (drop Makefile, gain CI and releases)
- gh-sweep (fix stale pins, gain hooks and releases)
- doner (adopt strict lint incrementally, keep action.yml)
- gh-star-search (run `copier update`, fix the gh-start-search typo, delete orphan ci.yaml)
- gh-lazydispatch (bump template pin when a new tag exists)
