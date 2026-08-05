# AI Agent Guidelines for my_go_template

How to work on this copier template. This file governs the template repository. The
guidance that ships to generated projects lives in `go_template/AGENTS.md.jinja`.

## What this repo is

`go_template/` is the render root (`_subdirectory` in `copier.yml`). Everything outside
it is template tooling and never reaches a generated project. Files ending `.jinja`
are rendered and the suffix is stripped, and files without it are copied verbatim, so
add the suffix only when a copier variable is actually interpolated.

`.ctt/` holds committed renders of every variant, driven by `ctt.toml` and
copier-template-tester. They are generated output. Never hand-edit them, run
`./sync_with_ctt.sh` and commit what it produces.

`copier-template-tester` renders from a clone of git HEAD, so untracked template files
are invisible to it and render as empty. Commit new template files before running the
sync, or the new variant comes out wrong.

## Improvements flow back from children

Generated projects diverge from the template on purpose. When a `copier update`
clobbers real work in a child repo, that is a signal about this template, not only a
chore for the child. Read the `.rej` and decide:

- The child's version generalizes, so backport it here and let every project get it
- The child's version is specific to that project, so leave the template alone
- The template's version was right, so nothing to do

Prefer backporting. A template that keeps overwriting the same thing in the same way
is rendering the wrong starting point, and the child repos are the only place that
shows up. `djot-fmt` commit `1ba8794` reached this template as `8abe04e` by exactly
this route.

Record the decision in `docs/DECISIONS.md` when the answer is "deliberately not".

## `_skip_if_exists` is a last resort

It is for files the template has nothing further to say about after the first render:
`README.md`, `DESIGN.md`, `go.mod`, `.config/mise.toml`, and the `cmd/` entry point.

Adding a file that carries template-maintained content stops every future fix from
reaching it, silently and permanently. A conflict is loud and usually small to
resolve, so take the conflict. `docs/DECISIONS.md` carries the worked reasoning.

## Feature flags

`use_goreleaser` and `publish_python` are the models. A flag is expressible when the
answer is genuinely binary. When the real answer is per-project (the cgo release
matrix, see `docs/DECISIONS.md`), document a recipe instead of adding a question.

Four things move together for a new flag: the question in `copier.yml`, the
conditional content, a `[output.".ctt/<name>"]` block in `ctt.toml`, and a matrix
entry in `.github/workflows/ci.yml`.

Conditional content has two forms. A conditional directory or filename
(`{% if flag %}name{% endif %}`) renders nothing when false and leaves no empty
directory. A whole-file `{% if %}` wrapper renders an empty file that
`_copier_post_generation.py` then deletes. Prefer the first.

## Verifying a change

Render it and run the generated project, because a template that renders is not a
template that works:

```sh
./sync_with_ctt.sh
cd .ctt/<variant> && mise run ci && golangci-lint run ./... && actionlint .github/workflows/*.yml
```

Delete any `dist/`, `.venv/`, or lockfile you create inside `.ctt/` before committing.

## Releasing

`bump_version.yml` runs on push to `main`, bumps with commitizen, and cuts the tag.
The commit type sets the bump, so a `feat:` cuts a minor and a `fix:` cuts a patch.
Children pin a tag in `.copier-answers.yml`, so nothing reaches them until one exists.

@AGENTS.local.md
