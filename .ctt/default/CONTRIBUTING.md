# Contributing to test-template

## Development Setup

### Prerequisites

- Go (see `go.mod` for minimum version)
- [mise](https://mise.jdx.dev/) - Task runner and tool manager
- [hk](https://hk.jdx.dev/) - Git hooks framework

### Initial Setup

```bash
# Install all tools via mise
mise install

# Install git hooks
hk install --mise

# Verify setup
mise run ci
```

## Project Structure



See [AGENTS.md](AGENTS.md) for detailed code organization guidelines.

## Development Workflow

### Running Tests

```bash
# Run all tests
mise run test

# Run specific package
go test ./internal/...

# View coverage
mise run test:view-coverage
```

### Linting and Formatting

```bash
# Auto-fix issues
mise run format

# Or use hk directly
hk fix

# Check without fixing
hk check
```

### Available Tasks

```bash
# List all tasks
mise tasks

# Common tasks
mise run ci              # Full CI check (tests + build)
mise run test            # Run tests with coverage
mise run format          # Format code
mise run hooks           # Run git hooks
```

## Code Guidelines

### Style

- Follow [AGENTS.md](AGENTS.md) guidelines
- Use `golangci-lint` (configured in `.golangci.toml`)
- Write table-driven tests
- Add context to errors: `fmt.Errorf("operation: %w", err)`

### Package Organization

- One package = one responsibility
- Avoid `util`, `common`, `misc` packages
- Use `internal/` for private code
- Keep `main.go` minimal

### Testing

- Use table-driven tests
- Test files: `*_test.go` adjacent to code
- Use `_test` package suffix for black-box testing
- Aim for meaningful coverage, not 100%

### Error Handling

- Return errors, don't panic
- Add context when wrapping: `fmt.Errorf("context: %w", err)`
- Use custom error types for domain errors
- Use sentinel errors (`var ErrNotFound = errors.New(...)`) sparingly

## Git Workflow

### Commits

Commits are enforced via commitizen:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Pre-commit Hooks

Hooks run automatically via hk:
- Linting (golangci-lint)
- Formatting (golines)
- YAML validation
- Filename conventions (ls-lint)

### Pre-push Hooks

Additional checks before push:
- Full CI suite (`mise run ci`)
- Commit message validation

## Release Process


Releases are automated via goreleaser:

1. Create and push tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. GitHub Actions builds binaries for:
   - Linux (amd64, arm64, 386)
   - macOS (amd64, arm64)
   - Windows (amd64, 386)
   - FreeBSD (amd64, arm64, 386)

3. Creates GitHub release with artifacts


## Troubleshooting

### Tool Installation Issues

```bash
# Reinstall all tools
mise install --force

# Check tool versions
mise list
```

### Hook Issues

```bash
# Reinstall hooks
hk install --mise --force

# Test hooks without commit
hk fix
```

### Test Failures

```bash
# Verbose test output
go test -v ./...

# Run specific test
go test -v -run TestName ./package
```

## Resources

- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
- [Uber Go Style Guide](https://github.com/uber-go/guide/blob/master/style.md)
- [AGENTS.md](AGENTS.md) - Project-specific guidelines
