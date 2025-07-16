# Multi-stage Dockerfile for MASS Framework Production Deployment
# Stage 1: Base Python environment
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create app user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Stage 2: Dependencies
FROM base as dependencies

# Set working directory
WORKDIR /app

# Copy requirements files
COPY requirements.txt .
COPY test_requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r test_requirements.txt

# Stage 3: Frontend build
FROM node:18-alpine as frontend-builder

WORKDIR /app/frontend

# Copy frontend files
COPY frontend/package*.json ./
RUN npm ci --only=production

# Copy frontend source
COPY frontend/src ./src
COPY frontend/public ./public

# Build frontend
RUN npm run build

# Stage 4: Production application
FROM base as production

# Set working directory
WORKDIR /app

# Copy Python dependencies from dependencies stage
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Copy built frontend from frontend-builder stage
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# Copy application code
COPY main.py .
COPY simple_server.py .
COPY core/ ./core/
COPY universal_mass_framework/ ./universal_mass_framework/
COPY agents/ ./agents/
COPY config/ ./config/
COPY ai_intelligence/ ./ai_intelligence/
COPY data_sources/ ./data_sources/
COPY data_orchestration/ ./data_orchestration/
COPY security/ ./security/
COPY trust_framework/ ./trust_framework/
COPY REVOLUTIONARY_FEATURES/ ./REVOLUTIONARY_FEATURES/

# Copy configuration files
COPY config/ ./config/
COPY .env.example .env

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/cache

# Set ownership to app user
RUN chown -R appuser:appuser /app

# Switch to app user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the application
CMD ["python", "main.py"]

# Stage 5: Development (optional)
FROM base as development

WORKDIR /app

# Copy requirements
COPY requirements.txt .
COPY test_requirements.txt .

# Install all dependencies including dev dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r test_requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/cache

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to app user
USER appuser

# Expose port
EXPOSE 8000

# Start development server
CMD ["python", "main.py"]
