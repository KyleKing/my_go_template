## v0.4.3 (2026-07-26)

### Fix

- **ci**: stop mise run from auto-installing unused tools in the ci job

## v0.4.2 (2026-07-26)

### Fix

- ignore the commitizen body.md so goreleaser's dirty check passes in children

## v0.4.1 (2026-07-26)

### Fix

- repair golangci config for the v2 schema and pin the lint action version
- drop MISE_ENV gating for hk tool pins
- point local dev at go run instead of build-and-install loops

## v0.4.0 (2026-07-26)

### Feat

- explore freshness tool

### Fix

- add script for provisioning a deploy key for my private tap
- **hk**: Pin version literally so generated configs evaluate
- correct demo command

## v0.3.2 (2026-07-04)

### Refactor

- add TUI testing guidance

## v0.3.1 (2026-07-04)

### Refactor

- condense AGENTS.md guidance and document upstreaming workflow

## v0.3.0 (2026-07-04)

### Feat

- fix template breakage found in cross-project audit

### Fix

- drop mise-managed gsa tool pin
- load shared mise tasks via .config/mise/conf.d

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
