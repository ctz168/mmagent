# MiniMax Agent - Full Stack Application
# Multi-stage build for optimized production deployment

# ============================================
# Stage 1: Backend Build
# ============================================
FROM python:3.12-slim as backend-builder

WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast Python package management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy requirements and install dependencies
COPY backend/requirements.txt .
RUN uv pip install --system -r requirements.txt

# Copy backend source
COPY backend/ .

# ============================================
# Stage 2: Frontend Build
# ============================================
FROM node:20-alpine as frontend-builder

WORKDIR /app/frontend

# Copy frontend files
COPY frontend/package.json frontend/vite.config.js ./
COPY frontend/index.html ./
COPY frontend/src ./src

# Install dependencies
RUN npm install

# Build frontend
RUN npm run build

# ============================================
# Stage 3: Production
# ============================================
FROM python:3.12-slim

LABEL maintainer="MiniMax"
LABEL description="MiniMax Agent - AI Agent Platform"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    xz-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g pnpm

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Create non-root user
RUN useradd -m -s /bin/bash agent \
    && mkdir -p /workspace /app \
    && chown -R agent:agent /workspace /app

WORKDIR /app

# Copy backend from builder
COPY --from=backend-builder /app/backend/ ./backend/

# Copy frontend build
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Install Python dependencies
RUN uv pip install --system -r backend/requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV NODE_ENV=production
ENV API_HOST=0.0.0.0
ENV API_PORT=8000
ENV WORKSPACE_DIR=/workspace
ENV DISPLAY=:99

# Expose port
EXPOSE 8000

# Switch to non-root user
USER agent

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Start application
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
