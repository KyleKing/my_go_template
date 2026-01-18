# Simple Makefile for test-template
# For full functionality, use: mise run <task>

.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: test
test: ## Run tests
	go test -v ./...

.PHONY: build
build: ## Build binary
	go build -v ./...

.PHONY: ci
ci: test build ## Run CI checks (test + build)

.PHONY: format
format: ## Format code
	golangci-lint run --fix ./...
	golines -w .

.PHONY: lint
lint: ## Run linter
	golangci-lint run ./...

.PHONY: clean
clean: ## Clean build artifacts

	rm -f coverage.out

.PHONY: coverage
coverage: ## Generate and view coverage report
	go test -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out
