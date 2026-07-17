#!/usr/bin/env bash
# ==========================================
# Kabulhaden CMS — Database Backup Script
# ==========================================
# Usage:
#   ./scripts/backup.sh                  # Full backup (DB + media)
#   ./scripts/backup.sh --db-only        # Database only
#   ./scripts/backup.sh --media-only     # Media files only
#
# Cron example (daily at 2 AM):
#   0 2 * * * /var/www/kabulhaden/scripts/backup.sh >> /var/www/kabulhaden/logs/backup.log 2>&1

set -euo pipefail

# ── Configuration ────────────────────────────
BACKUP_DIR="${BACKUP_DIR:-/var/www/kabulhaden/backups}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.yml}"
DB_CONTAINER="${DB_CONTAINER:-kabulhaden_db}"
DB_NAME="${POSTGRES_DB:-kabulhaden_db}"
DB_USER="${POSTGRES_USER:-kabulhaden_user}"
DATE_STAMP=$(date '+%Y%m%d_%H%M%S')
HOSTNAME=$(hostname -s)

# ── Parse Arguments ──────────────────────────
DO_DB=true
DO_MEDIA=true

for arg in "$@"; do
    case $arg in
        --db-only)     DO_MEDIA=false ;;
        --media-only)  DO_DB=false ;;
        --help|-h)
            echo "Usage: $0 [--db-only|--media-only]"
            exit 0
            ;;
    esac
done

# ── Colors ───────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()    { echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1"; }
success(){ echo -e "${GREEN}[✓]${NC} $1"; }
warn()   { echo -e "${YELLOW}[!]${NC} $1"; }
error()  { echo -e "${RED}[✗]${NC} $1"; exit 1; }

# ── Create Backup Directory ──────────────────
mkdir -p "${BACKUP_DIR}/db" "${BACKUP_DIR}/media"
log "Backup directory: ${BACKUP_DIR}"

# ── Database Backup ──────────────────────────
if [ "${DO_DB}" = "true" ]; then
    DB_BACKUP_FILE="${BACKUP_DIR}/db/kabulhaden_${DATE_STAMP}.sql.gz"
    log "Starting database backup..."

    docker exec "${DB_CONTAINER}" \
        pg_dump -U "${DB_USER}" -d "${DB_NAME}" \
        --format=custom \
        --compress=9 \
        --verbose \
        > "${DB_BACKUP_FILE}" 2>/dev/null

    DB_SIZE=$(du -h "${DB_BACKUP_FILE}" | cut -f1)
    success "Database backup: ${DB_BACKUP_FILE} (${DB_SIZE})"
fi

# ── Media Backup ─────────────────────────────
if [ "${DO_MEDIA}" = "true" ]; then
    MEDIA_BACKUP_FILE="${BACKUP_DIR}/media/kabulhaden_media_${DATE_STAMP}.tar.gz"
    MEDIA_DIR="${MEDIA_DIR:-/var/www/kabulhaden/media}"

    if [ -d "${MEDIA_DIR}" ]; then
        log "Starting media backup..."
        tar -czf "${MEDIA_BACKUP_FILE}" -C "$(dirname ${MEDIA_DIR})" "$(basename ${MEDIA_DIR})" 2>/dev/null

        MEDIA_SIZE=$(du -h "${MEDIA_BACKUP_FILE}" | cut -f1)
        success "Media backup: ${MEDIA_BACKUP_FILE} (${MEDIA_SIZE})"
    else
        warn "Media directory not found, skipping media backup"
    fi
fi

# ── Prune Old Backups ────────────────────────
log "Pruning backups older than ${RETENTION_DAYS} days..."
PRUNED_DB=$(find "${BACKUP_DIR}/db" -name "kabulhaden_*.sql.gz" -mtime +${RETENTION_DAYS} -delete -print | wc -l)
PRUNED_MEDIA=$(find "${BACKUP_DIR}/media" -name "kabulhaden_media_*.tar.gz" -mtime +${RETENTION_DAYS} -delete -print | wc -l)
success "Pruned ${PRUNED_DB} old DB backups, ${PRUNED_MEDIA} old media backups"

# ── Summary ──────────────────────────────────
TOTAL_SIZE=$(du -sh "${BACKUP_DIR}" | cut -f1)
BACKUP_COUNT=$(find "${BACKUP_DIR}" -type f | wc -l | tr -d ' ')

echo ""
success "═══════════════════════════════════════"
success " Backup complete!"
success " Total backups: ${BACKUP_COUNT}"
success " Total size:    ${TOTAL_SIZE}"
success " Location:      ${BACKUP_DIR}"
success " Retention:     ${RETENTION_DAYS} days"
success "═══════════════════════════════════════"
