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
│   ├── agent_integration/      # Agent Integration Tests
│   ├── model_integration/       # Model Integration Tests
│   ├── ui_ux_validation/        # UX/UI Validation Tests
│   ├── safety_privacy/          # Safety & Privacy Tests
│   ├── fixtures/                # Test fixtures and mocks
│   └── utils/                   # Test utilities
├── config/                      # Configuration files
├── reports/                     # Test reports (generated)
├── docker/                      # Docker configurations
├── .github/workflows/           # GitHub Actions CI/CD workflows
├── docs/                        # Test case documentation
├── pyproject.toml               # Project configuration and dependencies
└── uv.lock                      # Locked dependency versions (generated)
```

### Prerequisites
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (latest version) - Fast Python package installer and resolver
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
   
   # Or using pip
   pip install uv
   ```

3. **Install dependencies using uv**
   ```bash
   uv sync
   ```
   This will create a virtual environment, install all dependencies from `pyproject.toml`, and generate a `uv.lock` file for reproducible builds.
   
   **Note:** The `uv.lock` file should be committed to version control to ensure all team members use the same dependency versions.

4. **Set up environment variables**
   ```bash
   cp config/.env.example config/.env
   # Edit config/.env with your configuration
   ```

### Test Execution

#### Run All Tests
```bash
uv run pytest tests/ -v --html=reports/report.html --self-contained-html
```

#### Run Specific Test Suites
```bash
# Agent Integration Tests
uv run pytest tests/agent_integration/ -v

# Model Integration Tests
uv run pytest tests/model_integration/ -v

# UX/UI Validation Tests
uv run pytest tests/ui_ux_validation/ -v

# Safety & Privacy Tests
uv run pytest tests/safety_privacy/ -v
```

#### Using the Test Runner Script
```bash
# Run all tests with summary
uv run python run_tests.py --summary

# Run specific test suite
uv run python run_tests.py --suite agent_integration --marker p0

# Run with custom options
uv run python run_tests.py --suite model_integration --no-coverage
```

#### Run Tests with Docker
```bash
docker-compose -f docker/docker-compose.yml up --build
```

#### Run Tests in CI/CD Pipeline
Tests automatically run on push and pull requests via GitHub Actions. See `.github/workflows/qa-tests.yml` for configuration.

### Test Cases

#### Test Case Prioritization
- **P0 (Critical)**: Patient safety, data integrity, HIPAA compliance
- **P1 (High)**: Core functionality, data accuracy, model correctness
- **P2 (Medium)**: Edge cases, error handling, UX improvements
- **P3 (Low)**: Nice-to-have features, minor improvements

Detailed test case documentation is available in the `docs/` directory:
- [Agent Integration Test Cases](docs/test_cases/agent_integration.md)
- [Model Integration Test Cases](docs/test_cases/model_integration.md)
- [UX/UI Validation Test Cases](docs/test_cases/ui_ux_validation.md)
- [Safety & Privacy Test Cases](docs/test_cases/safety_privacy.md)

### CI/CD Integration

The test suite is integrated with GitHub Actions for continuous integration. The workflow file (`.github/workflows/qa-tests.yml`) automatically runs tests on:
- Pull requests to `main` branch

The workflow runs tests on Python 3.13 and generates comprehensive test reports and coverage data using `uv` for fast dependency management.

### Safety & Privacy Testing

Additional test cases have been created to safeguard member/patient safety and privacy:
- HIPAA compliance validation
- PHI (Protected Health Information) handling
- Data encryption validation
- Access control verification
- Audit logging
- Data retention policies
- Consent management

See `docs/test_cases/safety_privacy.md` for detailed test cases.

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
uv add package-name
```

**Updating dependencies:**
```bash
uv sync
```

**Removing a dependency:**
```bash
uv remove package-name
```

### Contributing

1. Follow the test case template in `docs/templates/`
2. Ensure all tests include proper assertions and error handling
3. Update test documentation when adding new test cases
4. Run linters and formatters before committing
5. Use `uv` for dependency management

