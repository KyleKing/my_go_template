# Next Steps

Follow-up work after the 2026-07-03 audit and fixes (context in TEMPLATE_IMPROVEMENT_PLAN.md).

## Follow-ups from the 2026-07-30 freshening

- The new CI `hooks` job turns four children red on their next update, each on a real finding: gh-sweep (1 typo in `ROADMAP.md`), gh-repo-dashboard (2 typos in `doing.txt` and `ROADMAP.md`), gh-star-search (1 typo in `internal/python/scripts/evaluate_embeddings.py`), gh-lazydispatch (shellcheck SC2044 in `scripts/check-test-safety.sh`). Fix each in the child, not by relaxing the template
- jj-diff additionally fails `check-merge-conflict` on `.jj-diff-roadmap.md`, which documents conflict markers as content. It needs a project-local `exclude` on that step, which is the first case of a child legitimately overriding a template hook
- typos flags deliberate fixture strings in jj-diff's `internal/fuzzy/fuzzy_test.go`. A project-local `[default.extend-words]` in its `.typos.toml` is the fix; the template file is the base and children extend it
- The child render still ships both `hk.pkl` and a full `.pre-commit-config.yaml`. Now that CI runs `hk check --all`, the pre-commit config is the odd one out and should go
- `mise run demo` needs vhs, which is not pinned in `[tools]` because it would be installed on every CI run of the new hooks job. Documented as a manual prerequisite instead
- Dependabot cannot read the action pins inside `go_template/**/*.jinja`, so the SHAs this template ships are still bumped by hand (deferred deliberately)

## Follow-ups from the 2026-07-29 freshening

- Run `scripts/provision-tap-deploy-key.sh` in each goreleaser child that should publish to the tap. Only gh-repo-dashboard has it today; the rest release fine without the secret (the cask push skips with a warning) but ship no cask
- gh-repo-dashboard carries the `homebrew_casks` block and the `TAP_DEPLOY_KEY` env line locally. Its next `copier update` will conflict on both, and the template version is now authoritative: take the template hunk and delete the local one
- gh-star-search excludes `.golangci.toml` from `toml-sort-fix` to protect the gci `sections` order. tombi does not sort arrays, so that exclusion (and the whole toml-sort block) is dead config in every child on its next update
- gh-star-search and gh-lazydispatch have prek installed as their `.git/hooks/pre-commit` while gh-sweep has hk. With toml-sort gone, a prek-only child formats no TOML at all until it runs `hk install --mise`
- Nothing formats TOML in this repo now, so the `.toml.jinja` sources and the committed `.ctt/` renders stay tombi-clean only by hand. `tombi format --check` over `.ctt/**/*.toml` after a render is the check; a local hk config here would automate it
- The hand-written `Formula/{{ project_name }}.rb` stub still ships with `REPLACE_WITH_SHA256_*` placeholders and a `release:homebrew` mise task that tells you to fill them in. goreleaser now generates the cask, so both are redundant; removing them needs the `remove-if-found.txt` manifest below

## Follow-ups from the 2026-07-27 freshening

All three items raised earlier in this pass are fixed. What remains:

- Dependabot cannot read the action pins inside `go_template/**/*.jinja`, so the SHAs this template ships to children are still bumped by hand. Pointing Dependabot at `.ctt/default` would open PRs against generated output that the next `ctt` run reverts, so it needs a real answer (a script that rewrites the jinja sources from a child's merged bump, or accepting the manual step)
- Children updating past v0.6.3 must confirm copier deleted `.github/workflows/release.yml`. goreleaser now runs inside `bump_version.yml`, and a leftover on-tag workflow would race it on any hand-pushed tag
- gh-sweep has seven camelCase Go filenames (`ghaPerfCache.go`, `actionsErrors.go`, `actionsFlaky.go`, `commentsGraphql.go`, `ghaPerf.go`, `watchGraphql.go`, `watchGraphql_test.go`) that fail the template's `snake_case` rule. Rename them there rather than relaxing the template
- The child render ships both `hk.pkl` and a full `.pre-commit-config.yaml`. Two hook systems in one project will drift apart. Decide whether children still need the pre-commit config now that hk covers the same ground
- `ctt` renders in place, which is what let the committed output freeze against stale recorded answers and `_skip_if_exists` files. `sync_with_ctt.sh` now clears `.ctt/*/` first, but the `copier-template-tester` pre-commit hook still renders in place and reports a stale tree as current. Worth fixing upstream in copier-template-tester
- The `_skip_if_exists` drift item below (2026-07-26) is now sharper: children never receive updates to `README.md`, `AGENTS.md`, `DESIGN.md`, `.config/mise.toml`, `go.mod`, or `cmd/*/main.go`, and until this pass the renders hid that

## Follow-ups from the 2026-07-26 freshening

- Pre-v0.5.0 children need a one-time hand-sync of `.config/mise.toml` when they update (drop the [tools] block; pins now live in the copier-managed `conf.d/template.toml`). A `_migrations` entry keyed to v0.5.0 could automate this; the templates currently use no `_migrations` at all, and this is the recurring class of change that mechanism exists for
- The `_skip_if_exists` list (AGENTS.md, DESIGN.md, README.md, .config/mise.toml) silently swallows template changes; consider a CI check or post-update note that diffs those files against the `.ctt/default` render so drift is visible
- The commitizen-action Docker build hits Docker Hub every Bump Version run and failed once on a registry timeout; consider a non-Docker install (pipx) in the workflow

## Template

- Replace the empty-file heuristics in `_copier_post_generation.py` with a rendered `remove-if-found.txt` manifest, following calcipy_template, so `copier update` can prune obsolete files
- Add answer validation to the post-generation script (for example, verify `module_path` ends with `project_name`) and exit nonzero on mismatch, which would have caught the gh-star-search typo
- Upstream `testdata/` plus `internal/testutil/` scaffolding and a binary-build integration test stub, modeled on djot-fmt
- Add `test:integration` and `bench:*` task naming conventions from gh-lazydispatch to `.config/mise/conf.d/template.toml.jinja` or document them as the expected project-local extension pattern
- Propagate the conf.d migration to each downstream project: mise never loaded `mise.template.toml` (it only loads `mise.toml` plus `mise.$MISE_ENV.toml`), so every task defined there was invisible and `mise run ci` failed with "unknown command: ci" locally and in CI. Tasks now live in `.config/mise/conf.d/template.toml`, which mise loads unconditionally, while env-gated tools stay in `mise.hk.toml`. Projects must delete the old `.config/mise.template.toml` and move any `mise.project.toml` tasks into `.config/mise/conf.d/`
- Consider an opt-in copier question for a composite `action.yml` (doner's GitHub Action distribution pattern)
- Tag a release to ship the pending AGENTS.md guidance and upstreaming-workflow docs so downstream projects can `copier update` past v0.3.0

gh-repo-dashboard adopted the template wholesale at v0.3.0 (config pinned via
`.copier-answers.yml`, root `main.go` moved to `cmd/gh-repo-dashboard/`, goreleaser
replacing the manual release matrix) and is the reference for the remaining migrations.

## Project migrations (ordered by payoff)

1. djot-fmt: run `copier copy` to retrofit, drop the redundant Makefile, move root `main.go` to `cmd/djot-fmt/`, add CI and releases, and remove the committed binary
2. gh-sweep: adopt the template, fix the stale go 1.21 mise pin, move root `main.go` to `cmd/gh-sweep/`, and revisit the disabled errcheck/unused linters
3. doner: adopt hooks and the strict golangci v2 config incrementally (expect many new findings), keep `action.yml` and the 80 percent coverage gate project-local
4. gh-star-search: run `copier update`, fix the `gh-start-search` answer typo (rename `cmd/gh-start-search/` and the Formula), delete the orphaned `ci.yaml`, and stop hand-editing `mise.template.toml`
5. gh-lazydispatch: bump the template pin from v0.2.2 to the latest release

## Cross-project consistency

| Item | Current state | Action |
| --- | --- | --- |
| vhs/gif demo output path | Inconsistent: some go apps write to `.github/assets`, others to `docs/images/demo.gif` | Pick one convention and standardize across projects; impacts https://github.com/kyleking/KyleKing |

## Out of scope

recipes keeps its own tooling. If desired, copy only the golangci config and hk builtins baseline manually.
