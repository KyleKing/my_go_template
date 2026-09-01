## v0.15.0 (2026-09-01)

### Feat

- **mise**: count subprocess tests toward the coverage floor

### Fix

- **typos**: read an abbreviated commit hash as a hash

## v0.14.2 (2026-09-01)

### Fix

- guard the PR step on a string so an empty output cannot throw

## v0.14.1 (2026-09-01)

### Fix

- run ctt through uvx so the freshness job can regenerate renders

## v0.14.0 (2026-09-01)

### Feat

- **doneram**: install the pinned release and drop Dependabot

### Fix

- **doneram**: install pkl so the freshness job can read the config

## v0.13.1 (2026-09-01)

### Fix

- **ci**: stop Dependabot resolving untagged charmbracelet/x submodules
- **scripts**: generate the tap deploy key inside 1Password

## v0.13.0 (2026-08-31)

### Feat

- **doneram**: track GitHub Action pins with the github-action resolver

### Fix

- **ci**: skip verify-released in the hooks job, which duplicates the ci job
- **copier**: restore .cz.toml version after an update resets it to 0.0.0

### Refactor

- **scripts**: drop pins doneram now owns

## v0.12.1 (2026-08-29)

### Fix

- **ci**: serialize Bump Version so duplicate runs cannot race on the tag

### Refactor

- **template**: drop the render's pre-commit config now that hk owns the hooks

## v0.12.0 (2026-08-27)

### Feat

- **ci**: run a project's own ci:project task so a local gate needs no workflow edit
- guard pushes against an unpublished sibling module

### Fix

- **lint**: stop gocritic demanding the named returns nonamedreturns forbids
- order pyproject.toml the way tombi's schema does
- give TOML arrays the trailing comma tombi needs

### Refactor

- express the doneram pin config in pkl
- hand tool version pins to doneram

## v0.11.4 (2026-08-16)

### Fix

- define every tool version once in copier.yml

## v0.11.3 (2026-08-05)

### Fix

- use portable arithmetic in the PyPI wait loop for Git Bash

## v0.11.2 (2026-08-05)

### Fix

- probe PyPI availability with a command uv actually has

## v0.11.1 (2026-08-05)

### Fix

- dispatch publish.yml so PyPI attestations validate, and tag with semver

## v0.11.0 (2026-08-05)

### Feat

- allow bump_version to cut a prerelease on manual dispatch

## v0.10.2 (2026-08-05)

### Fix

- publish Go binaries and the Python package from one called workflow

## v0.10.1 (2026-08-05)

### Fix

- build wheels on manylinux containers and windows arm64

## v0.10.0 (2026-08-05)

### Feat

- add an optional publish_python flag for shipping Go code to PyPI
- template-owned AGENTS.md with AGENTS.local.md for project guidance

## v0.9.2 (2026-08-01)

### Fix

- **hk**: skip the commitizen branch check on an empty rev-range

## v0.9.1 (2026-07-31)

### Fix

- **scripts**: refuse to delete renders outside the template root

## v0.9.0 (2026-07-30)

### Feat

- **ci**: run the hk gate suite in child CI
- validate copier answers at generation time

## v0.8.0 (2026-07-30)

### Feat

- prune the Formula stub from children via a remove-if-found manifest
- **hooks**: backfill the prek hooks hk.pkl was missing

### Fix

- **hooks**: stop newlines from stripping copier's trailing blank line

## v0.7.0 (2026-07-30)

### Feat

- **release**: publish a Homebrew cask from goreleaser

### Fix

- **hooks**: drop toml-sort so tombi is the only TOML formatter
- **scripts**: document GH_TOKEN

## v0.6.5 (2026-07-30)

### Fix

- **scripts**: archive tap deploy key via 1Password template and dedupe on re-run

## v0.6.4 (2026-07-27)

### Fix

- **release**: build each target into its own dist path

## v0.6.3 (2026-07-27)

### Fix

- stop shipping the copier-template-tester hook to children
- replace the goreleaser keys deprecated in v2
- restore YAML parse checking lost in the hk migration
- exclude golden fixtures from the hk whitespace fixers
- run goreleaser inside the bump job and drop the unreachable release.yml

## v0.6.2 (2026-07-27)

### Fix

- regenerate the .ctt renders from scratch on every sync
- drop the TODO marker from the generated CLI stub
- generate the root bump workflow from the template render
- activate Dependabot on the template repo itself

## v0.6.1 (2026-07-27)

### Fix

- skip the release step when commitizen makes no version bump
- skip go.mod and cmd/{{ project_name }}/main.go on update, document conf.d load order
- enforce snake_case for Go filenames instead of camelCase

## v0.6.0 (2026-07-27)

### Feat

- **tasks**: forward raw args on lint and test tasks

## v0.5.1 (2026-07-26)

### Fix

- move template-managed tool pins into conf.d so copier updates propagate them

## v0.5.0 (2026-07-26)

### Feat

- **tasks**: rename the run task to dev so the mise shorthand works

### Fix

- **lint**: drop the deprecated gomodguard linter, whose blocked list was empty
- **format**: pin golines and wrap at 120 to match the lll limit

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
