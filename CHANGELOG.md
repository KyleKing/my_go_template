## Unreleased

### Feat

- generate go.mod from module_path so projects build without a manual go mod init
- generate .cz.toml and bump_version.yml so commitizen hooks in generated projects are fully wired
- add test:coverage-min mise task with a 70 percent threshold
- add ctt fixtures for library and cli-without-goreleaser variants
- add template CI that generates each variant and runs go vet and go build

### Fix

- remove the unsupported workspace project type from README and dead branches from ci.yml.jinja
- fix sync_with_ctt.sh aborting on a nonexistent .cz.toml copy
- migrate .golangci.toml to golangci-lint v2: drop removed linters (execinquery, exportloopref, gomnd, gosimple, stylecheck, typecheck, tenv), add usetesting, move gci/gofmt/gofumpt/goimports to the formatters section
- document all copier questions in the README variable table
- centralize the hk version pin in a copier variable referenced by hk.pkl and mise.hk.toml

## v0.2.2 (2026-02-01)

### Fix

- split out into project-specific files to minimize clobbering

## v0.2.1 (2026-01-31)

### Fix

- adapt to gh-lazydispatch

## v0.2.0 (2026-01-31)

### Feat

- update to work on real projects like jj-diff

## v0.1.0 (2026-01-30)

### Feat

- add ldflags
- restore strict linting rules
- simplify and improve documentation
- switch to mise from makefile
- add homebrew tap
- extend go template
- init my_go_template

### Fix

- finish migrating to v2 format of golang-ci
