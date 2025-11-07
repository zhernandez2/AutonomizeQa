.PHONY: install test lint format clean help

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies using uv
	uv sync

test: ## Run all tests
	uv run pytest tests/ -v

test-agent: ## Run agent integration tests
	uv run pytest tests/agent_integration/ -v -m "agent and p0"

test-model: ## Run model integration tests
	uv run pytest tests/model_integration/ -v -m "model and p0"

test-ui: ## Run UI/UX tests
	uv run pytest tests/ui_ux_validation/ -v -m "ui and p0"

test-safety: ## Run safety & privacy tests
	uv run pytest tests/safety_privacy/ -v -m "safety and p0"

test-report: ## Run all tests with HTML report
	uv run pytest tests/ -v --html=reports/report.html --self-contained-html

lint: ## Run linters
	uv run flake8 tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
	uv run flake8 tests/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format: ## Format code (if black is available)
	uv run black tests/ || echo "black not available"

clean: ## Clean generated files
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf reports/*.html
	rm -rf reports/*.xml
	rm -rf reports/*.json
	rm -rf reports/coverage
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

update-deps: ## Update all dependencies
	uv sync --upgrade

add-dep: ## Add a new dependency (usage: make add-dep PKG=package-name)
	uv add $(PKG)

remove-dep: ## Remove a dependency (usage: make remove-dep PKG=package-name)
	uv remove $(PKG)

docker-build: ## Build Docker image
	docker build -f docker/Dockerfile -t autonomize-test-suite .

docker-run: ## Run tests in Docker
	docker-compose -f docker/docker-compose.yml up --build

