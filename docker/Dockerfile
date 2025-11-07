# Dockerfile for Autonomize AI Test Suite
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml ./
COPY uv.lock* ./

# Install dependencies using uv
# Use --frozen only if uv.lock exists, otherwise generate it
RUN if [ -f uv.lock ]; then \
        uv sync --frozen --no-dev; \
    else \
        uv sync --no-dev; \
    fi

# Copy application code
COPY . .

# Create reports directory
RUN mkdir -p reports logs

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTEST_CURRENT_TEST=""
ENV PATH="/app/.venv/bin:$PATH"

# Default command
CMD ["uv", "run", "pytest", "tests/", "-v", "--html=reports/report.html", "--self-contained-html"]

