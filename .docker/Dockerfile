# Multi-stage Dockerfile for Agno Template
# Stage 1: Builder - Install dependencies
FROM python:3.13-slim AS builder

# Install UV package manager for fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Set working directory
WORKDIR /app

# Copy only pyproject.toml for dependency resolution (better layer caching)
COPY pyproject.toml ./

# Create virtual environment and install dependencies using UV workflow
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Use UV to compile dependencies and sync (equivalent to pip compile + pip sync)
RUN uv pip compile pyproject.toml --upgrade --all-extras -o requirements.txt \
    && uv pip sync requirements.txt

# Stage 2: Runtime - Lean production image
FROM python:3.13-slim

# Install only runtime necessities
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set environment variables
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app
WORKDIR /app
RUN chown app:app /app

# Copy application code
COPY --chown=app:app . .

# Switch to non-root user
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Use CMD for flexibility (can be overridden in docker-compose)
CMD ["python", "main.py"]