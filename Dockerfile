# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Install uv — fast Python package manager used across the deepagents ecosystem
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# Copy dependency files first to maximise Docker layer caching
COPY pyproject.toml ./
COPY uv.lock* ./

# Install production dependencies only (no dev extras)
RUN uv sync --frozen --no-dev --no-install-project

# Copy application source
COPY mass/ ./mass/

# Cloud Run expects the container to listen on $PORT (default 8080)
EXPOSE 8080

# Use uv run so the managed venv is always used
CMD ["uv", "run", "uvicorn", "mass.main:app", "--host", "0.0.0.0", "--port", "8080"]

