#!/usr/bin/env bash
# ==========================================
# Kabulhaden CMS — Deployment Script
# ==========================================
# Usage: ./scripts/deploy.sh [branch]
# Performs zero-downtime deployment via Docker Compose.

set -euo pipefail

# ── Configuration ────────────────────────────
APP_NAME="kabulhaden"
DEPLOY_DIR="${DEPLOY_DIR:-/var/www/kabulhaden}"
BRANCH="${1:-main}"
BACKUP_BEFORE_DEPLOY="${BACKUP_BEFORE_DEPLOY:-true}"
HEALTH_CHECK_URL="${HEALTH_CHECK_URL:-http://localhost:8000/health/}"
HEALTH_CHECK_TIMEOUT=60

# ── Colors ───────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log()    { echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"; }
success(){ echo -e "${GREEN}[✓]${NC} $1"; }
warn()   { echo -e "${YELLOW}[!]${NC} $1"; }
error()  { echo -e "${RED}[✗]${NC} $1"; exit 1; }

# ── Pre-flight Checks ────────────────────────
log "Starting deployment of ${APP_NAME} (branch: ${BRANCH})"

if [ ! -d "${DEPLOY_DIR}" ]; then
    error "Deploy directory ${DEPLOY_DIR} does not exist"
fi

if [ ! -f "${DEPLOY_DIR}/.env" ]; then
    error ".env file not found at ${DEPLOY_DIR}/.env"
fi

cd "${DEPLOY_DIR}"

# ── Backup Before Deploy ─────────────────────
if [ "${BACKUP_BEFORE_DEPLOY}" = "true" ] && [ -f "scripts/backup.sh" ]; then
    log "Running pre-deploy backup..."
    bash scripts/backup.sh || warn "Backup failed, continuing deployment"
fi

# ── Pull Latest Code ─────────────────────────
log "Pulling latest code from ${BRANCH}..."
git fetch origin
git checkout "${BRANCH}"
git pull origin "${BRANCH}"
success "Code updated to $(git rev-parse --short HEAD)"

# ── Build Docker Images ──────────────────────
log "Building Docker images..."
docker compose build --no-cache
success "Docker images built"

# ── Apply Database Migrations ────────────────
log "Running database migrations..."
docker compose exec -T web python manage.py migrate --noinput
success "Migrations applied"

# ── Collect Static Files ─────────────────────
log "Collecting static files..."
docker compose exec -T web python manage.py collectstatic --noinput --clear
success "Static files collected"

# ── Restart Services ─────────────────────────
log "Restarting services with zero downtime..."
docker compose up -d --remove-orphans
success "Services restarted"

# ── Health Check ─────────────────────────────
log "Running health check..."
elapsed=0
while [ ${elapsed} -lt ${HEALTH_CHECK_TIMEOUT} ]; do
    if curl -sf "${HEALTH_CHECK_URL}" > /dev/null 2>&1; then
        success "Health check passed"
        break
    fi
    sleep 2
    elapsed=$((elapsed + 2))
    echo -n "."
done

if [ ${elapsed} -ge ${HEALTH_CHECK_TIMEOUT} ]; then
    warn "Health check timed out after ${HEALTH_CHECK_TIMEOUT}s"
    log "Checking container logs..."
    docker compose logs --tail=20 web
    error "Deployment may have issues — check logs above"
fi

# ── Cleanup ──────────────────────────────────
log "Cleaning up old images..."
docker image prune -f --filter "until=168h" || true

# ── Summary ──────────────────────────────────
echo ""
success "═══════════════════════════════════════"
success " Deployment complete!"
success " Branch:  ${BRANCH}"
success " Commit:  $(git rev-parse --short HEAD)"
success " Time:    $(date '+%Y-%m-%d %H:%M:%S')"
success "═══════════════════════════════════════"
