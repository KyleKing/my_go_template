# my_go_template

Copier template for Go projects with best practices, linting, testing, and CI/CD.

## Features

- **Project types**: CLI or library
- **Linting**: golangci-lint with 40+ linters
- **Git hooks**: hk framework with pre-commit/pre-push hooks
- **Task runner**: mise for consistent development tasks
- **CI/CD**: GitHub Actions with testing and linting
- **Release**: goreleaser for multi-platform binaries (CLI projects)
- **Documentation**: README, CONTRIBUTING, AGENTS.md (AI guidelines)
- **Dependencies**: Dependabot for automated updates

## Usage

Install copier:

```bash
pipx install copier
```

Create a new project:

```bash
copier copy gh:kyleking/my_go_template your-project-name
cd your-project-name
```

Install tools and hooks:

```bash
mise install
hk install --mise
```

Run CI checks:

```bash
mise run ci
```

## Template Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `development_branch` | `main` | Branch used for development |
| `project_name` | - | Project name (lowercase, hyphens) |
| `project_description` | - | Brief project description |
| `author_name` | `Kyle King` | Your name |
| `author_email` | `dev.act.kyle@gmail.com` | Your email |
| `repository_provider` | `https://github.com` | Repository provider URL |
| `author_username` | `kyleking` | Username on the repository provider |
| `repository_namespace` | `{author_username}` | Repository namespace |
| `module_path` | `github.com/{namespace}/{name}` | Go module import path |
| `copyright_date` | current year | Copyright year for LICENSE |
| `project_type` | `cli` | Type: cli, library |
| `use_goreleaser` | `true` | Include release automation |

## Generated Files

### Configuration
- `.cz.toml` - Commitizen versioning configuration
- `.golangci.toml` - Linter configuration (40+ rules)
- `.ls-lint.yml` - Filename convention linter
- `hk.pkl` - Git hooks framework
- `.editorconfig` - Editor settings
- `.gitignore` - Go-specific ignore patterns
- `.gitattributes` - Line ending normalization

### Development
- `.config/mise.toml` - MISE_ENV selection and shared settings
- `.config/mise.hk.toml` - Env-gated tool installations
- `.config/mise/conf.d/template.toml` - Task definitions (loaded unconditionally, regardless of `MISE_ENV`)
- `go.mod` - Go module definition

### CI/CD
- `.github/workflows/bump_version.yml` - Commitizen version bumps
- `.github/workflows/ci.yml` - Test and lint
- GoReleaser runs inside `bump_version.yml` (if enabled), because tags pushed with `GITHUB_TOKEN` never trigger a separate on-tag workflow
- `.github/dependabot.yml` - Dependency updates
- `Formula/<project>.rb` - Homebrew formula (if goreleaser enabled)

### Documentation
- `README.md` - Project overview and usage
- `CONTRIBUTING.md` - Development guide
- `AGENTS.md` - AI agent guidelines
- `LICENSE` - MIT license
- `.github/PULL_REQUEST_TEMPLATE.md` - PR template

### Source (CLI projects)
- `cmd/<project>/main.go` - Entry point with version/help flags

## Development

### Testing the Template

```bash
# Install pre-commit hooks
pre-commit install

# Test template generation
pre-commit run copier-template-tester --all-files

# Or manually
copier copy . /tmp/test-project --data project_name=test
```

### Updating

```bash
# Update existing project with template changes
copier update
```

### Upstreaming improvements from a project

Generated files split into two kinds: universal guidance shared by every project
(for example `AGENTS.md`, the `.golangci.toml` rules, the mise task set) and
project-specific content (`DESIGN.md`, `README.md`, source). When you improve
*universal* guidance while working in a downstream project, mirror the change back
here so it isn't lost on the next `copier update`:

1. Make the equivalent edit in the matching template source under `go_template/`
   (for example `go_template/AGENTS.md.jinja`), reintroducing any `{{ jinja }}`
   variables the rendered file had filled in
2. Verify the render still matches: `copier copy --trust . /tmp/test-project --data project_name=test` and diff the generated file
3. Commit and tag a release (commitizen bump), then run `copier update` in the
   downstream projects to pull the change cleanly

Keep project-specific edits (`DESIGN.md`, domain docs) in the project only; those are
protected by `_skip_if_exists` and must not be pushed into the template.

## License

MIT License - see [LICENSE](LICENSE)
