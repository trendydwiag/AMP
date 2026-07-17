# Kabulhaden CMS — Operations Runbook

Step-by-step operational procedures for common tasks.

---

## Table of Contents

1. [Daily Operations](#daily-operations)
2. [Deployment Procedures](#deployment-procedures)
3. [Maintenance Tasks](#maintenance-tasks)
4. [Incident Response](#incident-response)
5. [User Management](#user-management)
6. [Database Operations](#database-operations)
7. [Emergency Procedures](#emergency-procedures)

---

## Daily Operations

### Morning Health Check

```bash
# Run full health check
./scripts/health_check.sh

# Quick status check
docker compose ps

# Check for overnight errors
grep "$(date +%Y-%m-%d)" logs/error.log | wc -l
```

### Verify Backups

```bash
# Check today's backup exists
ls -la backups/db/kabulhaden_$(date +%Y%m%d)*

# Check backup log
tail -20 logs/backup.log
```

### Monitor Disk Space

```bash
df -h /
docker system df
```

---

## Deployment Procedures

### Standard Deployment (Docker)

```bash
# 1. Pull latest code
cd /var/www/kabulhaden
git pull origin main

# 2. Run deployment script
./scripts/deploy.sh main

# 3. Verify
./scripts/health_check.sh
curl -I https://your-domain.com
```

### Rolling Back a Deployment

```bash
# 1. Find the last good commit
git log --oneline -10

# 2. Checkout previous version
git checkout <commit-hash>

# 3. Rebuild and restart
docker compose down
docker compose up -d --build

# 4. Rollback migrations if needed
docker compose exec web python manage.py migrate <app> <previous_migration>

# 5. Verify
./scripts/health_check.sh
```

### Database Migration (Production)

```bash
# 1. Create backup first
./scripts/backup.sh --db-only

# 2. Apply migrations
docker compose exec web python manage.py migrate --noinput

# 3. Verify
docker compose exec web python manage.py showmigrations
```

### New Feature Deployment

```bash
# 1. Create feature branch
git checkout -b feature/new-feature main

# 2. Make changes and commit
git add .
git commit -m "feat: add new feature"

# 3. Push and test
git push origin feature/new-feature

# 4. Merge to main after review
git checkout main
git merge feature/new-feature

# 5. Deploy
./scripts/deploy.sh main
```

---

## Maintenance Tasks

### Weekly

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Clean Docker resources
docker system prune -f --filter "until=168h"

# Check SSL certificate expiry
echo | openssl s_client -connect your-domain.com:443 2>/dev/null | \
  openssl x509 -noout -dates

# Review security logs
grep "Failed" logs/security.log | wc -l
```

### Monthly

```bash
# Rotate Django secret key (quarterly)
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
# Update in .env, restart application

# Review and update dependencies
pip list --outdated
npm outdated

# Database maintenance
docker exec kabulhaden_db psql -U kabulhaden_user -d kabulhaden_db -c \
  "VACUUM ANALYZE;"

# Check for orphaned media files
python manage.py shell -c "
import os
from django.conf import settings
media_files = set()
for root, dirs, files in os.walk(settings.MEDIA_ROOT):
    for f in files:
        media_files.add(os.path.join(root, f))
print(f'{len(media_files)} files in media directory')
"
```

### Quarterly

```bash
# Full backup restore test
./scripts/restore.sh --list  # See available backups
# Restore to a test database
# Verify data integrity

# Security audit
# Review user accounts
# Check permissions matrix
# Review access logs

# Performance review
# Check slow queries
# Review response times
# Analyze traffic patterns
```

---

## Incident Response

### Severity Levels

| Level | Description | Response Time | Example |
|-------|-------------|---------------|---------|
| P1 | Site down | Immediate | Complete outage |
| P2 | Major feature broken | < 1 hour | Admin panel 500 |
| P3 | Minor feature issue | < 4 hours | CSS not loading |
| P4 | Cosmetic / low impact | Next business day | Typo in UI |

### P1: Site Down

```bash
# 1. Assess
docker compose ps
curl -I https://your-domain.com

# 2. Check logs
docker compose logs --tail=50 web
docker compose logs --tail=50 db
tail -20 logs/error.log

# 3. Quick fixes to try
docker compose restart web
docker compose restart db
docker compose restart nginx

# 4. If database is down
docker compose restart db
sleep 10
docker compose restart web

# 5. If still down, check infrastructure
df -h
free -m
docker stats --no-stream
```

### P2: Admin Panel 500 Error

```bash
# 1. Check error log
tail -50 logs/error.log

# 2. Common causes and fixes
# Missing migrations
docker compose exec web python manage.py migrate

# Missing superuser
docker compose exec web python manage.py create_superadmin

# Static files issue
docker compose exec web python manage.py collectstatic --noinput

# Database connection
docker exec kabulhaden_db pg_isready -U kabulhaden_user
```

### Post-Incident

1. Document the incident (time, impact, cause, resolution)
2. Update this runbook if new failure mode discovered
3. Implement preventive measures
4. Notify affected users if necessary

---

## User Management

### Create Superadmin

```bash
docker compose exec web python manage.py create_superadmin
```

### Reset Admin Password

```bash
docker compose exec web python manage.py reset_admin
```

### Reset User Password

```bash
docker compose exec web python manage.py reset_password <username>
```

### Unlock User Account

```bash
docker compose exec web python manage.py unlock_user <username>
```

### Disable User Account

```bash
docker compose exec web python manage.py shell -c "
from apps.users.models import User
user = User.objects.get(username='<username>')
user.is_active = False
user.save()
print(f'User {user.username} disabled')
"
```

### View Active Sessions

```bash
docker compose exec web python manage.py shell -c "
from django.contrib.sessions.models import Session
from django.utils import timezone
import json

sessions = Session.objects.filter(expire_date__gte=timezone.now())
for session in sessions:
    data = session.get_decoded()
    print(f'User: {data.get(\"_auth_user_id\", \"N/A\")}, Expires: {session.expire_date}')
"
```

---

## Database Operations

### Connect to Database

```bash
# Docker
docker exec -it kabulhaden_db psql -U kabulhaden_user -d kabulhaden_db

# Bare metal
psql -U kabulhaden_user -d kabulhaden_db
```

### Useful Queries

```sql
-- Database size
SELECT pg_size_pretty(pg_database_size('kabulhaden_db'));

-- Active connections
SELECT count(*) FROM pg_stat_activity WHERE datname='kabulhaden_db';

-- Table sizes
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- Long-running queries
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE state = 'active' AND now() - pg_stat_activity.query_start > interval '5 minutes';
```

### Backup and Restore

```bash
# Backup
./scripts/backup.sh --db-only

# Restore
./scripts/restore.sh --latest
```

### Create Test Database

```bash
docker exec kabulhaden_db createdb -U kabulhaden_user kabulhaden_test
docker exec kabulhaden_db pg_dump -U kabulhaden_user kabulhaden_db | \
  docker exec -i kabulhaden_db psql -U kabulhaden_user -d kabulhaden_test
```

---

## Emergency Procedures

### Put Site in Maintenance Mode

```bash
# Create maintenance flag
docker compose exec web touch /app/maintenance.flag

# Or use Django's built-in
docker compose exec web python manage.py changepassword admin
```

### Emergency Stop

```bash
# Stop everything immediately
docker compose down

# Stop only web (keep DB running)
docker compose stop web
```

### Emergency Database Access

```bash
# If web container is down, access DB directly
docker exec -it kabulhaden_db psql -U kabulhaden_user -d kabulhaden_db

# If DB container is down
docker compose up -d db
sleep 10
docker exec -it kabulhaden_db psql -U kabulhaden_user -d kabulhaden_db
```

### Nuclear Option: Full Reset

```bash
# WARNING: This destroys all data

# 1. Backup first!
./scripts/backup.sh

# 2. Stop everything
docker compose down -v  # -v removes volumes

# 3. Remove data
rm -rf media/ logs/*.log

# 4. Rebuild
docker compose up -d --build

# 5. Setup fresh
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
docker compose exec web python manage.py create_superadmin
```
