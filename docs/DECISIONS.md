# Design Decisions

Choices that would otherwise be re-litigated, and the evidence that settled them.
Decisions whose rationale already sits next to the code it governs are listed at
the bottom rather than repeated here.

## No `uses_cgo` copier question

A project with a cgo-only dependency needs a different goreleaser build matrix
from the pure-Go default, so a boolean answer looks tempting. It cannot express
the answer: the right matrix is per-project. `gh-star-search` dropped windows,
freebsd, 386, and linux-arm64 because duckdb cannot cross-compile, and a
different cgo dependency would drop a different set.

A boolean would also branch two files (`.goreleaser.yml.jinja` and
`bump_version.yml.jinja`) for one child out of five, so the template keeps
`CGO_ENABLED=0` as the unconditional default and documents the rework instead.
The recipe is in the README under "Releasing a project that needs cgo", worked
from `gh-star-search` commits `f64b1c1` and `20a2597`.

## Decisions recorded next to their code

- The two-GOROOT failure from pairing `actions/setup-go` with `jdx/mise-action`
  in one job: `go_template/.github/workflows/ci.yml.jinja`
- Why the render ships no TOML formatter of its own beyond hk's `tombi-format`:
  `.pre-commit-config.yaml`
- Why the Homebrew cask publishes unconditionally rather than behind a
  `use_homebrew_tap` question: `go_template/.goreleaser.yml.jinja`
- Why Go filenames stay `snake_case`: `go_template/.ls-lint.yml`
- Why `sync_with_ctt.sh` clears `.ctt/*/` before rendering: `sync_with_ctt.sh`
