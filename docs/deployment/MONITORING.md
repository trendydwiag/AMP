# Kabulhaden CMS — Monitoring & Logging Guide

Monitoring, alerting, and log management for the Kabulhaden CMS platform.

---

## Table of Contents

1. [Logging Architecture](#logging-architecture)
2. [Log Files](#log-files)
3. [Docker Logs](#docker-logs)
4. [Application Monitoring](#application-monitoring)
5. [Database Monitoring](#database-monitoring)
6. [System Monitoring](#system-monitoring)
7. [Health Checks](#health-checks)
8. [Alerting](#alerting)

---

## Logging Architecture

Kabulhaden CMS uses Django's logging framework with multiple handlers:

```
┌─────────────┐     ┌──────────────────────────────┐
│  Django App  │────▶│  Logging Configuration        │
└─────────────┘     ├──────────────────────────────┤
                    │  Console (stdout)             │
                    │  application.log (DEBUG+)     │
                    │  security.log (INFO+)         │
                    │  error.log (ERROR+)           │
                    └──────────────────────────────┘
```

Configured in `config/settings/base.py`:

| Logger | Level | Handler | Purpose |
|--------|-------|---------|---------|
| `django` | INFO | console, application_file | General Django operations |
| `django.db.backends` | INFO | application_file | Database queries |
| `security` | INFO | console, security_file | Security/audit events |
| `django.request` | ERROR | error_file, console | Request errors |
| `django.security` | WARNING | security_file, console | Security warnings |
| `radio` | INFO | console, application_file | Radio engine events |

---

## Log Files

All logs stored in `/var/www/kabulhaden/logs/` (or `./logs/` locally):

| File | Description | Rotation |
|------|-------------|----------|
| `application.log` | General application events | Daily, 14 days |
| `security.log` | Auth events, permission changes | Daily, 30 days |
| `error.log` | Errors and exceptions | Daily, 30 days |
| `backup.log` | Backup script output | Append only |

### Viewing Logs

```bash
# Real-time application log
tail -f logs/application.log

# Security events
tail -f logs/security.log

# Errors only
tail -f logs/error.log

# Search for specific event
grep "login" logs/security.log
grep "ERROR" logs/application.log | tail -20

# Today's errors
grep "$(date +%Y-%m-%d)" logs/error.log
```

### Log Format

```
INFO 2025-01-15 10:30:45,123 module 1234 5678 {message}
│    │                    │     │     │     └─ Log message
│    │                    │     │     └─ Thread ID
│    │                    │     └─ Process ID
│    │                    │     └─ Module name
│    │                    └─ Timestamp
│    └─ Log level
```

---

## Docker Logs

### Container Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f web
docker compose logs -f db
docker compose logs -f nginx

# Last 100 lines
docker compose logs --tail=100 web

# Since specific time
docker compose logs --since="2025-01-15T10:00:00" web

# Since 1 hour ago
docker compose logs --since="1h" web
```

### Log Driver Configuration

Docker defaults to `json-file` driver. For production, consider:

```yaml
# In docker-compose.yml
services:
  web:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "5"
```

---

## Application Monitoring

### Health Endpoint

The CMS exposes a health check endpoint:

```bash
# Basic health check
curl http://localhost:8000/health/

# Expected response: HTTP 200 OK
```

### Custom Health Check Script

```bash
# Full health check
./scripts/health_check.sh

# JSON output (for monitoring tools)
./scripts/health_check.sh --json

# Quiet mode (exit code only, for cron)
./scripts/health_check.sh --quiet
```

### Key Metrics to Monitor

| Metric | Warning Threshold | Critical Threshold |
|--------|-------------------|-------------------|
| Response time | > 2s | > 5s |
| Error rate | > 1% | > 5% |
| CPU usage | > 70% | > 90% |
| Memory usage | > 70% | > 85% |
| Disk usage | > 80% | > 90% |
| DB connections | > 80% pool | > 95% pool |

---

## Database Monitoring

### PostgreSQL Status

```bash
# Check if accepting connections
docker exec kabulhaden_db pg_isready -U kabulhaden_user

# Connection count
docker exec kabulhaden_db psql -U kabulhaden_user -d kabulhaden_db -c \
  "SELECT count(*) FROM pg_stat_activity;"

# Database size
docker exec kabulhaden_db psql -U kabulhaden_user -d kabulhaden_db -c \
  "SELECT pg_size_pretty(pg_database_size('kabulhaden_db'));"

# Active queries
docker exec kabulhaden_db psql -U kabulhaden_user -d kabulhaden_db -c \
  "SELECT pid, state, query, query_start
   FROM pg_stat_activity
   WHERE datname='kabulhaden_db' AND state='active'
   ORDER BY query_start;"

# Table sizes
docker exec kabulhaden_db psql -U kabulhaden_user -d kabulhaden_db -c \
  "SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
   FROM pg_catalog.pg_statio_user_tables
   ORDER BY pg_total_relation_size(relid) DESC
   LIMIT 10;"
```

### Slow Query Detection

```sql
-- Enable slow query logging (in postgresql.conf)
-- log_min_duration_statement = 1000  -- log queries > 1s

-- Find slow queries
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

---

## System Monitoring

### Quick System Overview

```bash
# CPU and memory
htop

# Disk usage
df -h

# Docker resource usage
docker stats --no-stream

# Network connections
ss -tunlp | grep -E ':(80|443|5432|8000)'
```

### Monitoring Script

Create `/usr/local/bin/kabulhaden-monitor.sh`:

```bash
#!/bin/bash
echo "=== Kabulhaden CMS Monitor ==="
echo "Timestamp: $(date)"
echo ""
echo "--- Docker Containers ---"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep kabulhaden
echo ""
echo "--- Disk Usage ---"
df -h / | tail -1
echo ""
echo "--- Memory ---"
free -h | grep Mem
echo ""
echo "--- Recent Errors ---"
tail -5 /var/www/kabulhaden/logs/error.log 2>/dev/null || echo "No errors"
```

---

## Health Checks

### Docker Health Checks

Configured in `docker-compose.yml`:

| Service | Check | Interval | Timeout | Retries |
|---------|-------|----------|---------|---------|
| `web` | `curl -f http://localhost:8000/health/` | 30s | 10s | 3 |
| `db` | `pg_isready` | 10s | 5s | 5 |

### External Monitoring (Uptime Robot / BetterStack)

Monitor these endpoints:
- `https://your-domain.com/` — Main site
- `https://your-domain.com/admin/` — Admin panel
- `https://your-domain.com/health/` — Health check (for programmatic monitoring)

---

## Alerting

### Recommended Alerts

| Alert | Condition | Severity |
|-------|-----------|----------|
| Site Down | Health check fails 3x | Critical |
| High Error Rate | > 10 errors/min | Warning |
| Slow Response | P95 > 5s for 5min | Warning |
| Disk Full | > 90% usage | Critical |
| DB Connection Pool Exhausted | > 90% | Critical |
| Memory Exhausted | > 90% | Critical |
| Backup Failed | Backup script exit code != 0 | Critical |

### Email Alerting (Django)

Django's `django.request` logger captures server errors. For production:

1. Configure `ADMINS` in production settings for email error reports
2. Set `SERVER_EMAIL` for the from address
3. Errors trigger automatic email to all admins

```python
# In production.py (add to settings)
ADMINS = [
    ('Admin Name', 'admin@your-domain.com'),
]
SERVER_EMAIL = 'errors@your-domain.com'
```
