# ==========================================
# Kabulhaden CMS — Multi-stage Dockerfile
# ==========================================
# Build: docker build -t kabulhaden-cms .
# Run:   docker run -p 8000:8000 --env-file .env kabulhaden-cms

# ==========================================
# Stage 1: Builder — install build deps & pip packages
# ==========================================
FROM python:3.10-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements/base.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# ==========================================
# Stage 2: Production — minimal runtime image
# ==========================================
FROM python:3.10-slim AS production

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Install runtime-only system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    netcat-openbsd \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtualenv from builder
COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

# Create directories
RUN mkdir -p /app/logs /app/static_root /app/media && \
    touch /app/logs/application.log /app/logs/security.log /app/logs/error.log

# Copy application code
COPY . /app/

# Make entrypoint executable
RUN chmod +x /app/scripts/entrypoint.sh

# Create non-root user
RUN groupadd -g 1000 django && \
    useradd -u 1000 -g django -s /bin/bash -m django && \
    chown -R django:django /app

# Collect static files as non-root (requires code to be in place)
RUN python manage.py collectstatic --noinput --settings=config.settings.production || true

USER django

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

ENTRYPOINT ["/app/scripts/entrypoint.sh"]
