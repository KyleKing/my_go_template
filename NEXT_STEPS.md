# Next Steps

Follow-up work after the 2026-07-03 audit and fixes (context in TEMPLATE_IMPROVEMENT_PLAN.md).

## Template

- Replace the empty-file heuristics in `_copier_post_generation.py` with a rendered `remove-if-found.txt` manifest, following calcipy_template, so `copier update` can prune obsolete files
- Add answer validation to the post-generation script (for example, verify `module_path` ends with `project_name`) and exit nonzero on mismatch, which would have caught the gh-star-search typo
- Upstream `testdata/` plus `internal/testutil/` scaffolding and a binary-build integration test stub, modeled on djot-fmt
- Add `test:integration` and `bench:*` task naming conventions from gh-lazydispatch to `mise.template.toml.jinja` or document them as the expected project-local extension pattern
- Consider an opt-in copier question for a composite `action.yml` (doner's GitHub Action distribution pattern)
- Tag a new release once the Unreleased changelog entries land, so projects can pin past v0.2.2

## Project migrations (ordered by payoff)

1. gh-repo-dashboard: adopt the template wholesale (currently has no mise, hooks, lint config, or goreleaser). Move root `main.go` to `cmd/gh-repo-dashboard/`, replace the manual release matrix with goreleaser, and remove the committed binary
2. djot-fmt: run `copier copy` to retrofit, drop the redundant Makefile, move root `main.go` to `cmd/djot-fmt/`, add CI and releases, and remove the committed binary
3. gh-sweep: adopt the template, fix the stale go 1.21 mise pin, move root `main.go` to `cmd/gh-sweep/`, and revisit the disabled errcheck/unused linters
4. doner: adopt hooks and the strict golangci v2 config incrementally (expect many new findings), keep `action.yml` and the 80 percent coverage gate project-local
5. gh-star-search: run `copier update`, fix the `gh-start-search` answer typo (rename `cmd/gh-start-search/` and the Formula), delete the orphaned `ci.yaml`, and stop hand-editing `mise.template.toml`
6. gh-lazydispatch: bump the template pin once a new release is tagged

## Out of scope

recipes keeps its own tooling. If desired, copy only the golangci config and hk builtins baseline manually.
