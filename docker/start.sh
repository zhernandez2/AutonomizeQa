#!/bin/bash
set -e

# Autonomize AI Test Suite - Startup Script
# This script handles initialization and test execution in Docker

echo "=========================================="
echo "Autonomize AI Test Suite"
echo "=========================================="

# NOTE: Once we have a viable application to test against, add health check logic here
# to wait for the application service to be ready before running tests

# Display test configuration
echo ""
echo "Configuration:"
echo "  API URL: ${API_BASE_URL:-Not set}"
echo "  Log Level: ${LOG_LEVEL:-INFO}"
echo "  Test Data: ${TEST_DATA_PATH:-/app/tests/fixtures/data}"
echo ""

# Run pytest with configured options
# You can override these by passing arguments to docker run
if [ $# -eq 0 ]; then
    echo "Running all tests..."
    exec uv run pytest tests/ \
        -v \
        --html=reports/report.html \
        --self-contained-html \
        --json-report \
        --json-report-file=reports/report.json \
        --junitxml=reports/junit.xml
else
    echo "Running tests with custom arguments: $@"
    exec uv run pytest "$@"
fi

