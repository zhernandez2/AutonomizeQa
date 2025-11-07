# Autonomize AI - QA Test Suite

### Overview
This repository contains a comprehensive test suite for validating an Agentic Platform's data validation and model integration processes, with a strong emphasis on patient safety and compliance. The test suite covers agent integration, model integration, UX/UI validation, and includes extensive safety and privacy testing.

### Table of Contents
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Test Execution](#test-execution)
- [Test Cases](#test-cases)
- [CI/CD Integration](#cicd-integration)
- [Safety & Privacy Testing](#safety--privacy-testing)
- [Reporting](#reporting)

### Project Structure
```
Autonomize/
├── tests/
│   ├── agent_integration/      # Agent Integration Tests (Automated)
│   ├── model_integration/       # Model Integration Tests (Automated)
│   ├── fixtures/                # Test fixtures and mocks
│   └── utils/                   # Test utilities
├── reports/                     # Test reports (generated)
├── docker/                      # Docker configurations
│   ├── Dockerfile               # Docker image definition
│   ├── docker-compose.yml       # Docker compose configuration
│   └── start.sh                 # Container startup script
├── .github/workflows/           # GitHub Actions CI/CD workflows
├── docs/                        # Test case documentation
├── justfile                     # Just command runner recipes
├── pyproject.toml               # Project configuration and dependencies
└── uv.lock                      # Locked dependency versions (generated)
```

### Prerequisites
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (latest version) - Fast Python package installer and resolver
- [just](https://github.com/casey/just) (recommended) - Command runner for easier workflow management
- Docker and Docker Compose (optional)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Autonomize
   ```

2. **Install uv** (if not already installed)
   ```bash
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   

3. **Install dependencies using uv**
   ```bash
   uv sync
   ```
   This will create a virtual environment, install all dependencies from `pyproject.toml`, and generate a `uv.lock` file for reproducible builds.
   
   **Note:** The `uv.lock` file should be committed to version control to ensure all team members use the same dependency versions.


### Test Execution

#### Quick Commands with Just

This project uses [`just`](https://github.com/casey/just) as a command runner for easier workflow management.

```bash
# On macOS
brew install just

# On Windows - Using Winget (built into Windows 10/11):
winget install --id Casey.Just
```

**Note:** If you don't have `just` installed, you can still run all commands directly using `uv run pytest ...` - see examples below.

**View all available commands:**
```bash
just
# or
just --list
```

**Test Commands:**
```bash
# Run all tests
just test

# Run specific test groups
just test-agent      # Agent integration tests
just test-model      # Model integration tests

# Run all test groups in sequence
just test-all

# Run tests with HTML report
just test-report
```

**Other useful commands:**
```bash
# Install dependencies
just install

# Format code
just format

# Run linters
just lint

# Clean generated files
just clean

# Update all dependencies
just update-deps
```

#### Run All Tests (Direct Command)
```bash
uv run pytest tests/ -v --html=reports/report.html --self-contained-html
```

#### Run Specific Test Suites (Direct Commands)
```bash
# Agent Integration Tests
uv run pytest tests/agent_integration/ -v -m agent

# Model Integration Tests
uv run pytest tests/model_integration/ -v -m model

# Run tests with specific markers
uv run pytest tests/ -v -m smoke
uv run pytest tests/ -v -m regression
```

#### Run Tests with Docker

The Docker setup uses a `start.sh` script for streamlined test execution with health checks and configuration display.

```bash
# Using just (recommended)
just docker-build         # Build Docker image
just docker-run          # Build and run tests in Docker
just docker-run-quick    # Run tests without rebuilding
just docker-logs         # View test runner logs
just docker-down         # Stop and remove containers

# Or directly
docker-compose -f docker/docker-compose.yml up --build

# Run with custom test arguments
docker-compose -f docker/docker-compose.yml run test-runner /app/start.sh tests/agent_integration/ -v -m agent
```

#### Run Tests in CI/CD Pipeline
Tests automatically run on push and pull requests via GitHub Actions. See `.github/workflows/qa-tests.yml` for configuration.

### Test Cases

Detailed test case documentation is available in the `docs/` directory:
- [Agent Integration Test Cases](docs/test_cases/agent_integration.md) - **Automated tests**
- [Model Integration Test Cases](docs/test_cases/model_integration.md) - **Automated tests**
- [Safety & Privacy Test Cases](docs/test_cases/safety_privacy.md) - Proposed test suite documentation
- [UI/UX Validation Test Cases](docs/test_cases/ui_ux_validation.md) - Manual test documentation

#### Test Case Prioritization

Each test case is classified with three dimensions to guide test execution planning:

- **Priority**: Determines execution order (Critical → High → Medium → Low)
  - **Critical**: Must be executed first, blockers for production deployment
  - **High**: Core functionality tests, executed in every test run
  - **Medium**: Important but not blocking, can be deferred under time constraints
  - **Low**: Nice-to-have validations, optional for quick test cycles

- **Risk**: Impact if the feature fails in production (Critical → High → Medium → Low)
  - **Critical**: Patient safety or regulatory compliance risk (HIPAA violations, data breaches)
  - **High**: Significant business impact or data integrity issues
  - **Medium**: User experience degradation or minor data issues
  - **Low**: Cosmetic issues or edge case failures

- **Complexity**: Test implementation and maintenance effort (High → Medium → Low)
  - **High**: Requires complex setup, multiple integrations, or extensive data preparation
  - **Medium**: Standard integration testing with moderate setup
  - **Low**: Simple unit-style tests with minimal dependencies

This prioritization helps QA engineers determine what to automate first and what to execute when time is limited.

### CI/CD Integration

The test suite is integrated with GitHub Actions for continuous integration. The workflow file (`.github/workflows/qa-tests.yml`) automatically runs tests on:
- Pull requests to `main` branch

The workflow runs tests on Python 3.13 and generates comprehensive test reports and coverage data using `uv` for fast dependency management.

#### Accessing CI/CD Test Reports

Test reports are automatically generated and uploaded as artifacts on every workflow run:

1. **Navigate to Upload test results**
   - Go to your repository on GitHub
   - Click the **"Actions"** tab at the top

2. **Download the artifact url**
   - Open up the folder you just downloaded
   - Open up the html file to see the test results

### Safety & Privacy Testing

Proposed test cases for safeguarding member/patient safety and privacy compliance:
- **HIPAA Compliance**: PHI encryption in transit and at rest
- **Access Control**: Role-based access (RBAC) with audit trails
- **Audit Logging**: Comprehensive PHI access tracking
- **Patient Safety**: Critical risk alert accuracy and validation
- **Data Protection**: Encryption standards and secure transmission
- **Regulatory Compliance**: HITECH Act breach notification requirements

These test cases are documented in `docs/test_cases/safety_privacy.md` and would be implemented once core agent and model integration testing is validated. They represent critical requirements for a production healthcare system.

### Reporting

Test reports are generated automatically and include:
- Test execution summary
- Pass/fail statistics
- Defect summaries
- Recommendations for regression testing
- Risk assessment

Reports are saved in the `reports/` directory in HTML, JSON, and XML formats.

### Dependency Management

This project uses [uv](https://github.com/astral-sh/uv) for fast and reliable dependency management. Dependencies are defined in `pyproject.toml` and locked in `uv.lock`.

**Adding a new dependency:**
```bash
just add-dep package-name
# or directly: uv add package-name
```

**Installing/syncing dependencies:**
```bash
just install
# or directly: uv sync
```

**Updating dependencies:**
```bash
just update-deps
# or directly: uv sync --upgrade
```

**Removing a dependency:**
```bash
just remove-dep package-name
# or directly: uv remove package-name
```

### Contributing

1. Follow the test case template in `docs/templates/`
2. Ensure all tests include proper assertions and error handling
3. Update test documentation when adding new test cases
4. Run linters and formatters before committing:
   ```bash
   just format      # Format code with ruff
   just lint        # Check for linting issues
   just lint-fix    # Auto-fix linting issues
   ```
5. Use `uv` for dependency management

