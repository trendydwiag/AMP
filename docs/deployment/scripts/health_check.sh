#!/usr/bin/env bash
# ==========================================
# Kabulhaden CMS — Health Check Script
# ==========================================
# Usage:
#   ./scripts/health_check.sh              # Check all services
#   ./scripts/health_check.sh --json       # JSON output
#   ./scripts/health_check.sh --quiet      # Exit code only

set -euo pipefail

# ── Configuration ────────────────────────────
APP_URL="${APP_URL:-http://localhost:8000}"
HEALTH_ENDPOINT="${APP_URL}/health/"
DB_CONTAINER="${DB_CONTAINER:-kabulhaden_db}"
WEB_CONTAINER="${WEB_CONTAINER:-kabulhaden_web}"
NGINX_CONTAINER="${NGINX_CONTAINER:-kabulhaden_nginx}"
TIMEOUT=10

# ── Parse Arguments ──────────────────────────
JSON_MODE=false
QUIET_MODE=false

for arg in "$@"; do
    case $arg in
        --json)  JSON_MODE=true ;;
        --quiet) QUIET_MODE=true ;;
    esac
done

# ── Colors ───────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ── Results ──────────────────────────────────
CHECKS_PASSED=0
CHECKS_FAILED=0
CHECKS_WARNING=0
RESULTS=""

check_pass() {
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
    RESULTS="${RESULTS}  ✓ $1\n"
    [ "${QUIET_MODE}" = "false" ] && echo -e "${GREEN}✓${NC} $1"
}

check_fail() {
    CHECKS_FAILED=$((CHECKS_FAILED + 1))
    RESULTS="${RESULTS}  ✗ $1\n"
    [ "${QUIET_MODE}" = "false" ] && echo -e "${RED}✗${NC} $1"
}

check_warn() {
    CHECKS_WARNING=$((CHECKS_WARNING + 1))
    RESULTS="${RESULTS}  ! $1\n"
    [ "${QUIET_MODE}" = "false" ] && echo -e "${YELLOW}!${NC} $1"
}

# ── Check: Docker Containers ─────────────────
[ "${QUIET_MODE}" = "false" ] && echo -e "\n${BLUE}── Docker Containers ──${NC}"

if docker ps --format '{{.Names}}' | grep -q "${WEB_CONTAINER}"; then
    check_pass "Web container is running"
else
    check_fail "Web container is NOT running"
fi

if docker ps --format '{{.Names}}' | grep -q "${DB_CONTAINER}"; then
    check_pass "Database container is running"
else
    check_fail "Database container is NOT running"
fi

if docker ps --format '{{.Names}}' | grep -q "${NGINX_CONTAINER}"; then
    check_pass "Nginx container is running"
else
    check_warn "Nginx container is not running (may not be deployed)"
fi

# ── Check: Application HTTP ──────────────────
[ "${QUIET_MODE}" = "false" ] && echo -e "\n${BLUE}── HTTP Health ──${NC}"

HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout ${TIMEOUT} "${HEALTH_ENDPOINT}" 2>/dev/null || echo "000")

if [ "${HTTP_STATUS}" = "200" ]; then
    check_pass "HTTP health endpoint returned 200"
elif [ "${HTTP_STATUS}" = "000" ]; then
    check_fail "HTTP health endpoint is unreachable"
else
    check_warn "HTTP health endpoint returned status ${HTTP_STATUS}"
fi

RESPONSE_TIME=$(curl -s -o /dev/null -w "%{time_total}" --connect-timeout ${TIMEOUT} "${APP_URL}/" 2>/dev/null || echo "N/A")
if [ "${RESPONSE_TIME}" != "N/A" ]; then
    RESPONSE_MS=$(echo "${RESPONSE_TIME} * 1000" | bc 2>/dev/null || echo "${RESPONSE_TIME}")
    if (( $(echo "${RESPONSE_TIME} < 2" | bc -l 2>/dev/null || echo 0) )); then
        check_pass "Response time: ${RESPONSE_MS}ms"
    elif (( $(echo "${RESPONSE_TIME} < 5" | bc -l 2>/dev/null || echo 0) )); then
        check_warn "Response time: ${RESPONSE_MS}ms (slow)"
    else
        check_fail "Response time: ${RESPONSE_MS}ms (very slow)"
    fi
fi

# ── Check: Database Connectivity ─────────────
[ "${QUIET_MODE}" = "false" ] && echo -e "\n${BLUE}── Database ──${NC}"

DB_CHECK=$(docker exec "${DB_CONTAINER}" pg_isready -U "${POSTGRES_USER:-kabulhaden_user}" 2>/dev/null || echo "failed")
if echo "${DB_CHECK}" | grep -q "accepting connections"; then
    check_pass "PostgreSQL is accepting connections"
else
    check_fail "PostgreSQL is NOT accepting connections"
fi

# ── Check: Disk Space ────────────────────────
[ "${QUIET_MODE}" = "false" ] && echo -e "\n${BLUE}── System ──${NC}"

DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
if [ "${DISK_USAGE}" -lt 80 ]; then
    check_pass "Disk usage: ${DISK_USAGE}%"
elif [ "${DISK_USAGE}" -lt 90 ]; then
    check_warn "Disk usage: ${DISK_USAGE}% (getting high)"
else
    check_fail "Disk usage: ${DISK_USAGE}% (critical)"
fi

# Memory
MEMORY_FREE=$(free -m 2>/dev/null | awk '/^Mem:/ {print $7}' || echo "N/A")
if [ "${MEMORY_FREE}" != "N/A" ]; then
    if [ "${MEMORY_FREE}" -gt 256 ]; then
        check_pass "Available memory: ${MEMORY_FREE}MB"
    else
        check_warn "Available memory: ${MEMORY_FREE}MB (low)"
    fi
fi

# ── Check: Log Files ─────────────────────────
if [ -d "/var/www/kabulhaden/logs" ]; then
    ERROR_COUNT=$(grep -c "ERROR" /var/www/kabulhaden/logs/error.log 2>/dev/null || echo "0")
    RECENT_ERRORS=$(tail -100 /var/www/kabulhaden/logs/error.log 2>/dev/null | grep -c "$(date '+%Y-%m-%d')" || echo "0")
    if [ "${RECENT_ERRORS}" -lt 5 ]; then
        check_pass "Recent errors today: ${RECENT_ERRORS}"
    else
        check_warn "Recent errors today: ${RECENT_ERRORS}"
    fi
fi

# ── Summary ──────────────────────────────────
TOTAL=$((CHECKS_PASSED + CHECKS_FAILED + CHECKS_WARNING))

if [ "${JSON_MODE}" = "true" ]; then
    echo "{"
    echo "  \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
    echo "  \"passed\": ${CHECKS_PASSED},"
    echo "  \"failed\": ${CHECKS_FAILED},"
    echo "  \"warnings\": ${CHECKS_WARNING},"
    echo "  \"total\": ${TOTAL}"
    echo "}"
else
    echo ""
    echo -e "═══════════════════════════════════════"
    echo -e " Health Check Summary"
    echo -e " Passed:   ${GREEN}${CHECKS_PASSED}${NC}"
    echo -e " Failed:   ${RED}${CHECKS_FAILED}${NC}"
    echo -e " Warnings: ${YELLOW}${CHECKS_WARNING}${NC}"
    echo -e " Total:    ${TOTAL}"
    echo -e "═══════════════════════════════════════"
fi

# Exit code: non-zero if any checks failed
[ "${CHECKS_FAILED}" -eq 0 ] && exit 0 || exit 1
