#!/usr/bin/env bash
# ==========================================
# Kabulhaden CMS — Initial Server Setup
# ==========================================
# Usage: sudo bash scripts/setup.sh
# Provisions a fresh Ubuntu/Debian server for Kabulhaden CMS.

set -euo pipefail

# ── Configuration ────────────────────────────
APP_USER="${APP_USER:-kabulhaden}"
APP_DIR="${APP_DIR:-/var/www/kabulhaden}"
DOMAIN="${1:-localhost}"

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

# ── Check Root ───────────────────────────────
if [ "$(id -u)" -ne 0 ]; then
    error "This script must be run as root (sudo)"
fi

log "Starting server setup for Kabulhaden CMS"
log "Domain: ${DOMAIN}"

# ── System Updates ───────────────────────────
log "Updating system packages..."
apt-get update -qq
apt-get upgrade -y -qq
success "System packages updated"

# ── Install Dependencies ─────────────────────
log "Installing system dependencies..."
apt-get install -y -qq \
    curl \
    git \
    wget \
    unzip \
    build-essential \
    libpq-dev \
    postgresql-client \
    nginx \
    certbot \
    python3-certbot-nginx \
    ufw \
    fail2ban \
    htop \
    tree
success "System dependencies installed"

# ── Install Docker ───────────────────────────
if ! command -v docker &> /dev/null; then
    log "Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
    success "Docker installed"
else
    success "Docker already installed"
fi

# ── Install Docker Compose Plugin ────────────
if ! docker compose version &> /dev/null; then
    log "Installing Docker Compose plugin..."
    apt-get install -y -qq docker-compose-plugin
    success "Docker Compose installed"
else
    success "Docker Compose already installed"
fi

# ── Create App User ──────────────────────────
if ! id "${APP_USER}" &>/dev/null; then
    log "Creating application user..."
    useradd -m -s /bin/bash "${APP_USER}"
    usermod -aG docker "${APP_USER}"
    success "User '${APP_USER}' created"
else
    success "User '${APP_USER}' already exists"
fi

# ── Clone Application ────────────────────────
log "Cloning application repository..."
if [ ! -d "${APP_DIR}" ]; then
    mkdir -p "${APP_DIR}"
    git clone https://github.com/your-org/kabulhaden.git "${APP_DIR}"
    chown -R "${APP_USER}:${APP_USER}" "${APP_DIR}"
    success "Repository cloned to ${APP_DIR}"
else
    warn "Directory ${APP_DIR} already exists, skipping clone"
fi

# ── Configure Environment ────────────────────
if [ ! -f "${APP_DIR}/.env" ]; then
    log "Creating .env from template..."
    cp "${APP_DIR}/.env.example" "${APP_DIR}/.env"

    # Generate Django secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
    sed -i "s/replace-with-a-very-secure-random-key-min-50-chars/${SECRET_KEY}/" "${APP_DIR}/.env"
    sed -i "s/DJANGO_DEBUG=True/DJANGO_DEBUG=False/" "${APP_DIR}/.env"
    sed -i "s/DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0/DJANGO_ALLOWED_HOSTS=${DOMAIN},www.${DOMAIN}/" "${APP_DIR}/.env"
    sed -i "s/DJANGO_SETTINGS_MODULE=config.settings.development/DJANGO_SETTINGS_MODULE=config.settings.production/" "${APP_DIR}/.env"

    warn "Please edit ${APP_DIR}/.env and set:"
    warn "  - POSTGRES_PASSWORD (strong password)"
    warn "  - EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD"
    success ".env created with generated SECRET_KEY"
fi

# ── Configure Firewall ───────────────────────
log "Configuring UFW firewall..."
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
success "Firewall configured"

# ── Configure Fail2Ban ───────────────────────
log "Configuring Fail2Ban..."
cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime  = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true

[nginx-http-auth]
enabled = true

[nginx-limit-req]
enabled = true
EOF
systemctl enable fail2ban
systemctl restart fail2ban
success "Fail2Ban configured"

# ── Configure Log Rotation ───────────────────
log "Configuring log rotation..."
cat > /etc/logrotate.d/kabulhaden << 'EOF'
/var/www/kabulhaden/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 kabulhaden kabulhaden
    sharedscripts
}
EOF
success "Log rotation configured"

# ── Deploy Application ───────────────────────
log "Building and starting application..."
cd "${APP_DIR}"
docker compose -f docker-compose.yml up -d --build
success "Application containers started"

# ── Run Initial Commands ─────────────────────
log "Running initial migrations..."
docker compose exec -T web python manage.py migrate --noinput
docker compose exec -T web python manage.py collectstatic --noinput
success "Initial setup commands completed"

# ── Setup Certbot ────────────────────────────
if [ "${DOMAIN}" != "localhost" ]; then
    log "Setting up SSL with Certbot..."
    certbot --nginx -d "${DOMAIN}" -d "www.${DOMAIN}" --non-interactive --agree-tos --email admin@${DOMAIN} || warn "Certbot setup failed — run manually later"
    success "SSL configured"
fi

# ── Summary ──────────────────────────────────
echo ""
success "═══════════════════════════════════════════════"
success " Server setup complete!"
success ""
success " Application: http://${DOMAIN}"
success " Admin panel: http://${DOMAIN}/admin/"
success ""
success " Next steps:"
success "   1. Edit ${APP_DIR}/.env with production values"
success "   2. Create superuser: docker compose exec web python manage.py createsuperuser"
success "   3. Configure DNS to point to this server"
success "   4. Set up automated backups (cron)"
success "═══════════════════════════════════════════════"
