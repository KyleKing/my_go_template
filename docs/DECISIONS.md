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
`sys-guardian` found the second per-project matrix divergence — a single-OS
project, rather than a cgo matrix — which lands in the same place: a recipe in
the README ("Releasing a project for one OS"), not a question.
The recipe is in the README under "Releasing a project that needs cgo", worked
from `gh-star-search` commits `f64b1c1` and `20a2597`.

## `_skip_if_exists` stays reserved for files the template stops maintaining

Scaffolding a project then implements conflicts on every `copier update`, because
the template keeps rendering its starting version. The `bindings/` cgo shim showed
this the first time `publish_python` reached a real project: djot-fmt's hand-written
binding was replaced by the generic stub and its content landed in `.rej` files.

Adding those paths to `_skip_if_exists` would stop the conflict, and it would also
stop every later template fix from reaching them, without ever reporting that it
had. A conflict is visible and usually a few lines to re-apply, so the template
takes the loud failure over the quiet one. `_skip_if_exists` holds only files the
template has nothing further to say about after the first render: `README.md`,
`DESIGN.md`, `go.mod`, `.config/mise.toml`, and `cmd/{{ project_name }}/main.go`.

The resolution procedure lives in `go_template/AGENTS.md.jinja` so it reaches every
generated project.

## Golden snapshot tasks stay in the project

gh-repo-dashboard keeps `test:golden`, `test:golden-update`, and a `ci` that runs the
golden-tagged tests, and they conflicted on every `copier update`. Each one hard-codes
a package (`./internal/app/`), a test name (`TestGolden`), and a build tag, and none
of those exist in a project without that layout. A template version would need three
questions or an empty default that does nothing, so the tasks stay local.

The generic part is the orphan check, which takes `GOLDEN_TAGS` for goldens behind a
build tag. Projects add their own tasks in a sibling `conf.d` file and override `ci`
there.

## `major_version_zero` is rendered, and a migration drops it past 0.x

jj-diff and jojo each added `major_version_zero = true` by hand so a `feat!` on 0.x
cuts a minor rather than 1.0.0, and every `copier update` would have dropped it.
The right value depends on the project's version, which is not a copier answer,
and a question for it would default wrong for a 1.x child updated with
`--defaults`. So `.cz.toml` renders the key, and an every-update migration in
`copier.yml` deletes it once the version is 1.0.0 or later.

Leaving it in a 1.x project is not refused as expected: commitizen 4.18 and 4.20
refuse the `--major-version-zero` flag past 0.x but honor the config key silently,
bumping a breaking change from 1.3.0 to 1.4.0 (verified with `cz bump --dry-run`).
Without it a 1.x Go module's `feat!` tags v2.0.0, which the module proxy rejects
until the module path ends in `/v2`. That move is deliberate work either way, so
the template keeps commitizen's honest answer and leaves the path change to the
project.

The migration runs after every update rather than once at the version that
introduced the key, because a conflict elsewhere in `.cz.toml` rejects the whole
hunk, deletion included.

## The version is restored after an update's diff, not before

copier renders the new template over the project, runs `_tasks`, and only then
applies the project's own diff. `restore_version` used to run in `_tasks`, so the
version was already real when the diff's `0.0.0 -> <real>` hunk arrived, and that
hunk was rejected on every update in every child. `_copier_post_generation.py` now
skips the restore when `_copier_operation` is `update`, the diff carries the
version, and the after-stage migration in `copier.yml` reads it back from `HEAD`
only when a conflict left the placeholder.

## Test hermeticity is guidance, not a generated `TestMain`

jj-diff, jojo, and second-look leaked into the runner's `~/.config` from their tests
(jj 0.47 records every repository it opens under `$XDG_CONFIG_HOME/jj/repos`) and
fixed it with aragonite's `hermetic` package. The generated `AGENTS.md` carries the
rule and names the package, and the template renders no `TestMain`. The stub project
has no test that starts a process, so a `TestMain` would guard nothing; importing
aragonite would make it a dependency of every project, including the ones with no
use for it; and a stdlib copy of `hermetic` would drift from the one the tools use.

## The stub ships its own test, rendered on copy only

A fresh render failed its own `test:coverage-min`: the stub `main.go` had no test, so
coverage read 0%, and the library render had no package at all, so `mise run ci`
stopped at "no packages to test". The stub now routes through `run(args, stdout)` and
`report(err, stderr)`, `main_internal_test.go` covers them (92%), and the library
render gets a `doc.go`; `test:coverage-min` passes a project with no statements yet.

Both files are scaffolding the project replaces, like `main.go`, but `_skip_if_exists`
alone is not enough for them: it skips a file only when it exists, so an update would
add a test of a `run()` jojo and second-look no longer have, and a root package to
aragonite. `_exclude` drops them when `_copier_operation` is `update`, and
`_skip_if_exists` keeps `copier recopy` off them.

## `check-added-large-files` checks only what the change adds

hk 2.13 selects every tracked file under `hk check --all`, and its
`check_added_large_files` builtin sets `allow_binary = true`, so a demo gif
committed long ago failed every whole-tree check: CI's `hk check --all` and the
hand-run check jj users rely on. Under hk 1
the step never saw it: binaries were filtered out, and the name promises files
*added*.

The step wraps the builtin and drops each file whose content is byte-identical to
the same path at the base: where HEAD meets `origin/HEAD`, or HEAD when that ref is
missing. A new or modified oversized file is still refused, by pre-commit (the
staged files), by pre-push (whatever the unpushed commits add), and by
`hk check --all` while the commit adding it is unpushed. Verified on a scratch repo
with a 1.5 MB gif in the base commit: the stock builtin fails `hk check --all`, the
wrapper passes it, and the wrapper still fails `git commit` of a new 1.5 MB file,
of a modified one, and `git push` of an unpushed commit adding one.

Removing the step from the `check` and `fix` hooks was the other option, and it
would leave jj users with no guard at all, since `jj git push` runs no git hooks.
CI checks out the commit being tested with no `origin/HEAD`, so there the base is
HEAD and the step checks nothing; the guard is local, as it was under hk 1.

## Decisions recorded next to their code

- The two-GOROOT failure from pairing `actions/setup-go` with `jdx/mise-action`
  in one job: `go_template/.github/workflows/ci.yml.jinja`
- Why `tombi-format` is the render's only TOML formatter, and what else hk does
  not cover: `go_template/hk.pkl.jinja`
- Why the Homebrew cask publishes unconditionally rather than behind a
  `use_homebrew_tap` question: `go_template/.goreleaser.yml.jinja`
- Why Go filenames stay `snake_case`: `go_template/.ls-lint.yml`
- Why `sync_with_ctt.sh` clears `.ctt/*/` before rendering: `sync_with_ctt.sh`
