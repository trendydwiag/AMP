# Kabulhaden CMS — Backup & Disaster Recovery

Complete backup strategy and disaster recovery procedures.

---

## Table of Contents

1. [Backup Strategy](#backup-strategy)
2. [Automated Backups](#automated-backups)
3. [Backup Verification](#backup-verification)
4. [Restore Procedures](#restore-procedures)
5. [Disaster Recovery](#disaster-recovery)
6. [Off-Site Backup](#off-site-backup)

---

## Backup Strategy

### What to Back Up

| Component | Method | Frequency | Retention |
|-----------|--------|-----------|-----------|
| PostgreSQL database | `pg_dump` via backup.sh | Daily (2 AM) | 30 days |
| Media files | `tar.gz` archive | Daily (2 AM) | 30 days |
| `.env` file | Manual / config mgmt | On change | Indefinite |
| Application code | Git repository | Every push | Indefinite |
| Nginx config | File copy | On change | Indefinite |

### Backup Location

```
/var/www/kabulhaden/backups/
├── db/
│   ├── kabulhaden_20250115_020000.sql.gz
│   ├── kabulhaden_20250116_020000.sql.gz
│   └── ...
├── media/
│   ├── kabulhaden_media_20250115_020000.tar.gz
│   └── ...
└── config/
    └── .env.backup
```

---

## Automated Backups

### Setup Cron Job

```bash
# Edit crontab
crontab -e

# Add these entries:

# Daily database backup at 2 AM
0 2 * * * /var/www/kabulhaden/scripts/backup.sh --db-only >> /var/www/kabulhaden/logs/backup.log 2>&1

# Weekly full backup (DB + media) on Sundays at 3 AM
0 3 * * 0 /var/www/kabulhaden/scripts/backup.sh >> /var/www/kabulhaden/logs/backup.log 2>&1

# Prune backups older than 30 days (daily at 4 AM)
0 4 * * * find /var/www/kabulhaden/backups -name "*.sql.gz" -mtime +30 -delete
0 4 * * * find /var/www/kabulhaden/backups -name "*.tar.gz" -mtime +30 -delete
```

### Manual Backup

```bash
# Full backup
./scripts/backup.sh

# Database only
./scripts/backup.sh --db-only

# Media only
./scripts/backup.sh --media-only
```

### Docker Backup (Non-Cron)

```bash
# Backup PostgreSQL from Docker
docker exec kabulhaden_db pg_dump -U kabulhaden_user -d kabulhaden_db \
  --format=custom --compress=9 > backup_$(date +%Y%m%d).sql.gz

# Backup media volume
docker run --rm -v kabulhaden_media:/data -v $(pwd):/backup \
  alpine tar czf /backup/media_$(date +%Y%m%d).tar.gz -C /data .
```

---

## Backup Verification

### Automated Verification Script

Create `scripts/verify_backup.sh`:

```bash
#!/bin/bash
BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file.sql.gz>"
    exit 1
fi

# Check file exists and is not empty
if [ ! -s "$BACKUP_FILE" ]; then
    echo "FAIL: File is empty or missing"
    exit 1
fi

# Check file is valid gzip
if ! gzip -t "$BACKUP_FILE" 2>/dev/null; then
    echo "FAIL: File is not valid gzip"
    exit 1
fi

# Test restore to temporary database
TEMP_DB="kabulhaden_verify_$$"
createdb "$TEMP_DB"
gunzip -c "$BACKUP_FILE" | pg_restore -U kabulhaden_user -d "$TEMP_DB" 2>/dev/null

# Check table count
TABLE_COUNT=$(psql -U kabulhaden_user -d "$TEMP_DB" -t -c \
  "SELECT count(*) FROM information_schema.tables WHERE table_schema='public';" | tr -d ' ')

dropdb "$TEMP_DB"

if [ "$TABLE_COUNT" -gt 5 ]; then
    echo "PASS: Backup contains $TABLE_COUNT tables"
else
    echo "FAIL: Only $TABLE_COUNT tables found (expected >5)"
    exit 1
fi
```

### Manual Verification

```bash
# List backup contents
gunzip -l backup_file.sql.gz

# Test restore to temp database
createdb kabulhaden_test_restore
gunzip -c backup_file.sql.gz | pg_restore -U kabulhaden_user -d kabulhaden_test_restore
psql -U kabulhaden_user -d kabulhaden_test_restore -c "\dt"
dropdb kabulhaden_test_restore
```

---

## Restore Procedures

### Database Restore

```bash
# Interactive restore (with confirmation)
./scripts/restore.sh --latest

# Restore specific backup
./scripts/restore.sh /var/www/kabulhaden/backups/db/kabulhaden_20250115_020000.sql.gz

# List available backups
./scripts/restore.sh --list
```

### Docker Restore

```bash
# Stop web container
docker compose stop web

# Restore database
cat backup.sql.gz | gunzip | docker exec -i kabulhaden_db \
  psql -U kabulhaden_user -d kabulhaden_db

# Restart web
docker compose start web

# Run migrations
docker compose exec web python manage.py migrate --noinput
```

### Media Restore

```bash
# Restore media files
tar -xzf media_backup.tar.gz -C /var/www/kabulhaden/
chown -R kabulhaden:kabulhaden /var/www/kabulhaden/media
```

---

## Disaster Recovery

### Scenario 1: Database Corruption

```bash
# 1. Stop the application
docker compose stop web

# 2. Restore from latest backup
./scripts/restore.sh --latest

# 3. Run migrations
docker compose exec web python manage.py migrate --noinput

# 4. Verify and restart
docker compose start web
./scripts/health_check.sh
```

### Scenario 2: Server Failure

```bash
# 1. Provision new server
sudo bash scripts/setup.sh your-domain.com

# 2. Restore .env
cp /backup/.env /var/www/kabulhaden/.env

# 3. Deploy application
cd /var/www/kabulhaden
docker compose up -d --build

# 4. Restore database
./scripts/restore.sh --latest

# 5. Restore media
tar -xzf media_backup.tar.gz -C /var/www/kabulhaden/

# 6. Verify
./scripts/health_check.sh
curl -I https://your-domain.com
```

### Scenario 3: Accidental Data Deletion

```bash
# 1. Stop writes (optional: put site in maintenance mode)
docker compose stop web

# 2. Create safety backup
./scripts/backup.sh --db-only

# 3. Restore to specific point-in-time (if using WAL archiving)
# Or restore from most recent backup
./scripts/restore.sh --latest

# 4. Restart
docker compose start web
```

### Recovery Time Objectives

| Scenario | RTO (Recovery Time) | RPO (Data Loss) |
|----------|-------------------|-----------------|
| Database restore | 10-30 min | < 24 hours |
| Server rebuild | 30-60 min | < 24 hours |
| Application restart | < 5 min | 0 |

---

## Off-Site Backup

### Option A: SCP to Remote Server

```bash
# Add to backup script
REMOTE_HOST="backup-server.example.com"
REMOTE_USER="backup"
REMOTE_DIR="/backups/kabulhaden"

scp ${BACKUP_DIR}/db/*.sql.gz ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/db/
scp ${BACKUP_DIR}/media/*.tar.gz ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/media/
```

### Option B: S3 / Cloud Storage

```bash
# Using AWS CLI
aws s3 sync ${BACKUP_DIR}/db/ s3://your-backup-bucket/kabulhaden/db/ \
  --storage-class STANDARD_IA

aws s3 sync ${BACKUP_DIR}/media/ s3://your-backup-bucket/kabulhaden/media/ \
  --storage-class STANDARD_IA
```

### Option C: Rclone (Multi-Cloud)

```bash
# Install rclone
curl https://rclone.org/install.sh | bash

# Configure remote
rclone config

# Sync backups
rclone sync /var/www/kabulhaden/backups remote:kabulhaden-backups --progress
```
