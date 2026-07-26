# Next Steps

Follow-up work after the 2026-07-03 audit and fixes (context in TEMPLATE_IMPROVEMENT_PLAN.md).

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
