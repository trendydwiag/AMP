# Kabulhaden CMS — Security Hardening Guide

Security configuration and best practices for the Kabulhaden CMS platform.

---

## Table of Contents

1. [Django Security Settings](#django-security-settings)
2. [SSL/TLS Configuration](#ssltls-configuration)
3. [Authentication & Authorization](#authentication--authorization)
4. [Brute Force Protection](#brute-force-protection)
5. [Content Security Policy](#content-security-policy)
6. [Server Hardening](#server-hardening)
7. [Docker Security](#docker-security)
8. [Secret Management](#secret-management)
9. [Audit Logging](#audit-logging)
10. [Security Checklist](#security-checklist)

---

## Django Security Settings

Already configured in `config/settings/production.py`:

```python
# HTTPS Redirect
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cookie Security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# HSTS (1 year)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Browser Security Headers
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'same-origin'
X_FRAME_OPTIONS = 'DENY'
```

### Password Policy

```python
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

Minimum 12 characters, no common passwords, no numeric-only.

---

## SSL/TLS Configuration

### Option A: Nginx + Certbot (Recommended)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal (certbot installs cron automatically)
sudo certbot renew --dry-run
```

### Option B: Docker with SSL termination

Place certificates in `nginx_certs/` volume:

```
nginx_certs/
├── fullchain.pem
└── privkey.pem
```

Then enable the HTTPS server block in `nginx.conf`.

### SSL Best Practices

- Use TLS 1.2 and 1.3 only
- Enable HSTS with `includeSubDomains` and `preload`
- Use strong cipher suites
- Redirect all HTTP to HTTPS

---

## Authentication & Authorization

### Axes (Brute Force Protection)

```python
AXES_FAILURE_LIMIT = 5        # Lock after 5 failures
AXES_COOLOFF_TIME = 15         # 15 minute lockout
AXES_LOCKOUT_PARAMETERS = ['username', 'ip_address']
AXES_RESET_ON_SUCCESS = True
```

### Session Security

```python
SESSION_TIMEOUT_MINUTES = 60   # Auto-logout after 60 min inactivity
PASSWORD_RESET_TIMEOUT_HOURS = 48
LOGIN_URL = '/akun/masuk/'
```

### Custom Middleware

Already in place:
- `SessionTimeoutMiddleware` — Enforces session timeout
- `LastActivityMiddleware` — Tracks last activity timestamp
- `AuditLoggingMiddleware` — Logs security-relevant events

### Role-Based Access Control

Managed via Django's permission system and custom role assignments. See `docs/33_ROLE_BASED_ACCESS_CONTROL_GUIDE.md`.

---

## Brute Force Protection

### Axes Configuration

- **5 failed attempts** → 15-minute lockout
- Locks by both **username** and **IP address**
- Resets counter on successful login

### Monitoring

```bash
# Check lockout events
grep "locked out" logs/security.log

# Check failed login attempts
grep "Failed login" logs/security.log | tail -20
```

### Fail2Ban Integration

```ini
# /etc/fail2ban/jail.local
[django-login]
enabled = true
filter = django-login
logpath = /var/www/kabulhaden/logs/security.log
maxretry = 5
bantime = 3600
findtime = 600
```

Create `/etc/fail2ban/filter.d/django-login.conf`:

```ini
[Definition]
failregex = ^.*Login failed for.*from <HOST>.*$
ignoreregex =
```

---

## Content Security Policy

### Production CSP

```python
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_SCRIPT_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'", "data:")
CSP_FONT_SRC = ("'self'",)
CSP_OBJECT_SRC = ("'none'",)
CSP_FRAME_ANCESTORS = ("'none'",)
```

### CSP Reporting

```python
# Enable report-only mode for testing
CSP_REPORT_ONLY = True

# Configure report URI (when ready)
# CSP_REPORT_URI = "https://your-domain.com/csp-report/"
```

---

## Server Hardening

### UFW Firewall

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### SSH Hardening

```bash
# /etc/ssh/sshd_config
PermitRootLogin no
PasswordAuthentication no
MaxAuthTries 3
AllowUsers kabulhaden
```

### System Updates

```bash
# Enable automatic security updates
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### Nginx Security Headers

```nginx
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "same-origin" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

---

## Docker Security

### Non-Root User

The Dockerfile creates a non-root `django` user:

```dockerfile
RUN groupadd -g 1000 django && \
    useradd -u 1000 -g django -s /bin/bash -m django
USER django
```

### Read-Only Filesystem (Optional)

```yaml
services:
  web:
    read_only: true
    tmpfs:
      - /tmp
      - /app/logs
```

### No New Privileges

```yaml
services:
  web:
    security_opt:
      - no-new-privileges:true
```

### Resource Limits

```yaml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '2.0'
```

### Image Scanning

```bash
# Scan for vulnerabilities
docker scout cves kabulhaden-cms:latest

# Or use trivy
trivy image kabulhaden-cms:latest
```

---

## Secret Management

### Environment Variables

- **Never** commit `.env` to version control
- Use `.env.example` as template
- Generate secrets with:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Production Secrets

For production, consider:
- Docker secrets (for Swarm)
- Cloud provider secret managers (AWS SSM, GCP Secret Manager)
- HashiCorp Vault

### Key Rotation

- Rotate `DJANGO_SECRET_KEY` every 90 days
- Rotate database passwords quarterly
- Rotate email passwords when staff leave
- Rotate SSL certificates (auto-renewed via Certbot)

---

## Audit Logging

The `AuditLoggingMiddleware` logs:
- Login attempts (success/failure)
- Password changes
- Permission changes
- Model create/update/delete operations
- Admin panel access

### Security Log Analysis

```bash
# Failed logins in last 24 hours
grep "Failed" logs/security.log | grep "$(date +%Y-%m-%d)" | wc -l

# Successful logins
grep "login successful" logs/security.log | tail -10

# Admin panel access
grep "admin" logs/security.log | tail -10
```

---

## Security Checklist

### Pre-Deployment

- [ ] `DJANGO_DEBUG=False`
- [ ] `DJANGO_SECRET_KEY` is strong and unique (50+ chars)
- [ ] `DJANGO_ALLOWED_HOSTS` is restrictive
- [ ] `DATABASE_URL` uses strong password
- [ ] SSL certificates are valid and configured
- [ ] `.env` is not in version control
- [ ] Admin passwords are strong (12+ chars)
- [ ] UFW firewall is enabled
- [ ] Fail2Ban is installed and configured

### Post-Deployment

- [ ] HTTPS redirect is working
- [ ] HSTS header is present
- [ ] CSP headers are present
- [ ] Axes brute force protection is active
- [ ] Session timeout is configured
- [ ] Logs are rotating
- [ ] Backups are running
- [ ] Health checks are passing

### Ongoing

- [ ] Security updates applied monthly
- [ ] SSL certificates renewed
- [ ] Access reviews quarterly
- [ ] Log audits monthly
- [ ] Backup restore tested quarterly
