# Set shell for Windows compatibility
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

# List all available commands
default:
    @just --list

# ============================================================================
# SETUP & DEPENDENCIES
# ============================================================================

# Install dependencies using uv
install:
    uv sync

# Update all dependencies
update-deps:
    uv sync --upgrade

# Add a new dependency (usage: just add-dep package-name)
add-dep PKG:
    uv add {{PKG}}

# Remove a dependency (usage: just remove-dep package-name)
remove-dep PKG:
    uv remove {{PKG}}

# ============================================================================
# CODE QUALITY
# ============================================================================

# Format code with ruff
format:
    uv run ruff format tests/

# Run linters with ruff
lint:
    uv run ruff check tests/

# Fix linting issues automatically
lint-fix:
    uv run ruff check --fix tests/

# ============================================================================
# TESTING
# ============================================================================

# Run all tests
test:
    uv run pytest tests/ -v

# Run agent integration tests
test-agent:
    uv run pytest tests/agent_integration/ -v -m agent

# Run model integration tests
test-model:
    uv run pytest tests/model_integration/ -v -m model

# Run all tests with HTML report
test-report:
    uv run pytest tests/ -v --html=reports/report.html --self-contained-html

# Run all test commands in sequence
test-all: test-agent test-model
    @echo "All test groups completed!"

# ============================================================================
# CLEANUP
# ============================================================================

# Clean generated files
clean:
    @echo "Cleaning generated files..."
    @if (Test-Path .pytest_cache) { Remove-Item -Recurse -Force .pytest_cache }
    @if (Test-Path .coverage) { Remove-Item -Force .coverage }
    @if (Test-Path htmlcov) { Remove-Item -Recurse -Force htmlcov }
    @if (Test-Path reports/*.html) { Remove-Item -Force reports/*.html }
    @if (Test-Path reports/*.xml) { Remove-Item -Force reports/*.xml }
    @if (Test-Path reports/*.json) { Remove-Item -Force reports/*.json }
    @if (Test-Path reports/coverage) { Remove-Item -Recurse -Force reports/coverage }
    @Get-ChildItem -Recurse -Directory -Filter __pycache__ -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
    @Get-ChildItem -Recurse -Filter *.pyc -ErrorAction SilentlyContinue | Remove-Item -Force
    @echo "Cleanup complete!"

# ============================================================================
# DOCKER
# ============================================================================

# Build Docker image
docker-build:
    docker build -f docker/Dockerfile -t autonomize-test-suite .

# Run tests in Docker
docker-run:
    docker-compose -f docker/docker-compose.yml up --build

# Run tests in Docker (no rebuild)
docker-run-quick:
    docker-compose -f docker/docker-compose.yml up

# Stop and remove Docker containers
docker-down:
    docker-compose -f docker/docker-compose.yml down

# View Docker logs
docker-logs:
    docker-compose -f docker/docker-compose.yml logs -f test-runner
