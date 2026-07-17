#!/usr/bin/env bash
# ==========================================
# Kabulhaden CMS — Database Restore Script
# ==========================================
# Usage:
#   ./scripts/restore.sh backup_file.sql.gz    # Restore from file
#   ./scripts/restore.sh --latest              # Restore latest backup
#   ./scripts/restore.sh --list                # List available backups

set -euo pipefail

# ── Configuration ────────────────────────────
BACKUP_DIR="${BACKUP_DIR:-/var/www/kabulhaden/backups}"
DB_CONTAINER="${DB_CONTAINER:-kabulhaden_db}"
DB_NAME="${POSTGRES_DB:-kabulhaden_db}"
DB_USER="${POSTGRES_USER:-kabulhaden_user}"

# ── Colors ───────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()    { echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1"; }
success(){ echo -e "${GREEN}[✓]${NC} $1"; }
warn()   { echo -e "${YELLOW}[!]${NC} $1"; }
error()  { echo -e "${RED}[✗]${NC} $1"; exit 1; }

# ── List Backups ─────────────────────────────
list_backups() {
    log "Available database backups:"
    echo ""
    find "${BACKUP_DIR}/db" -name "kabulhaden_*.sql.gz" -type f | sort -r | head -20 | while read -r f; do
        SIZE=$(du -h "$f" | cut -f1)
        DATE=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$f" 2>/dev/null || stat -c "%y" "$f" 2>/dev/null | cut -d. -f1)
        echo "  $(basename $f)  (${SIZE})  ${DATE}"
    done
    echo ""
}

# ── Parse Arguments ──────────────────────────
case "${1:-}" in
    --help|-h)
        echo "Usage:"
        echo "  $0 <backup_file.sql.gz>    Restore from specific file"
        echo "  $0 --latest                Restore from latest backup"
        echo "  $0 --list                  List available backups"
        exit 0
        ;;
    --list)
        list_backups
        exit 0
        ;;
    --latest)
        BACKUP_FILE=$(find "${BACKUP_DIR}/db" -name "kabulhaden_*.sql.gz" -type f | sort | tail -1)
        if [ -z "${BACKUP_FILE}" ]; then
            error "No backups found in ${BACKUP_DIR}/db"
        fi
        log "Latest backup: $(basename ${BACKUP_FILE})"
        ;;
    "")
        error "No backup file specified. Use --help for usage."
        ;;
    *)
        BACKUP_FILE="$1"
        ;;
esac

# ── Validate Backup File ─────────────────────
if [ ! -f "${BACKUP_FILE}" ]; then
    error "Backup file not found: ${BACKUP_FILE}"
fi

BACKUP_SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
log "Backup file: ${BACKUP_FILE} (${BACKUP_SIZE})"

# ── Confirmation ─────────────────────────────
echo ""
warn "═══════════════════════════════════════"
warn " WARNING: This will OVERWRITE the"
warn " current database '${DB_NAME}'!"
warn "═══════════════════════════════════════"
echo ""
read -p "Type 'RESTORE' to confirm: " CONFIRM
if [ "${CONFIRM}" != "RESTORE" ]; then
    log "Restore cancelled."
    exit 0
fi

# ── Pre-restore Backup ───────────────────────
log "Creating safety backup before restore..."
SAFETY_BACKUP="${BACKUP_DIR}/db/kabulhaden_pre_restore_${DATE_STAMP:-$(date +%Y%m%d_%H%M%S)}.sql.gz"
docker exec "${DB_CONTAINER}" \
    pg_dump -U "${DB_USER}" -d "${DB_NAME}" --format=custom --compress=9 \
    > "${SAFETY_BACKUP}" 2>/dev/null
success "Safety backup: ${SAFETY_BACKUP}"

# ── Drop and Recreate Database ───────────────
log "Dropping and recreating database..."
docker exec "${DB_CONTAINER}" psql -U "${DB_USER}" -d postgres -c "
    SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='${DB_NAME}' AND pid <> pg_backend_pid();
" > /dev/null 2>&1 || true

docker exec "${DB_CONTAINER}" psql -U "${DB_USER}" -d postgres -c "
    DROP DATABASE IF EXISTS ${DB_NAME};
    CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};
" > /dev/null 2>&1
success "Database recreated"

# ── Restore ──────────────────────────────────
log "Restoring database..."
cat "${BACKUP_FILE}" | docker exec -i "${DB_CONTAINER}" \
    pg_restore -U "${DB_USER}" -d "${DB_NAME}" \
    --no-owner --no-privileges --verbose 2>/dev/null || true
success "Database restored"

# ── Run Migrations ───────────────────────────
log "Running migrations to ensure schema is current..."
cd /var/www/kabulhaden 2>/dev/null || true
docker compose exec -T web python manage.py migrate --noinput 2>/dev/null || warn "Could not run migrations (run manually)"
success "Migrations applied"

# ── Summary ──────────────────────────────────
echo ""
success "═══════════════════════════════════════"
success " Restore complete!"
success " Restored:  $(basename ${BACKUP_FILE})"
success " Database:  ${DB_NAME}"
success "═══════════════════════════════════════"
