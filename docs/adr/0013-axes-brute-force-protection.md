# 0013. Use django-axes for Brute Force Protection

**Status:** Accepted
**Date:** 2024-07-15

## Context

The CMS admin panel is a high-value target for credential stuffing and brute force attacks. Without protection:

- Attackers can attempt unlimited login combinations
- No automatic lockout after repeated failures
- No visibility into login attack patterns
- Compliance requirements (if any) may mandate account lockout

Django has no built-in brute force protection.

## Decision

We use **django-axes 6.4+** for login attempt tracking and automatic lockout.

Configuration in `config/settings/base.py`:

```python
INSTALLED_APPS = [
    # ...
    'axes',
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',  # Must be first
    'django.contrib.auth.backends.ModelBackend',
]

MIDDLEWARE = [
    # ...
    'axes.middleware.AxesMiddleware',
]

# Axes Configuration
AXES_FAILURE_LIMIT = 5              # Lockout after 5 failed attempts
AXES_COOLOFF_TIME = 15              # Lockout duration: 15 minutes
AXES_LOCKOUT_PARAMETERS = ['username', 'ip_address']  # Lock by username + IP
AXES_RESET_ON_SUCCESS = True        # Reset counter on successful login
```

## Consequences

**Positive:**

- After 5 failed login attempts, the account/IP is locked out for 15 minutes.
- Dual lockout parameters (`username` + `ip_address`) prevent both targeted and distributed attacks.
- `RESET_ON_SUCCESS` resets the failure counter on successful authentication.
- `AxesBackend` is placed first in `AUTHENTICATION_BACKENDS` to ensure all login attempts are tracked.
- Integrates seamlessly with Django's authentication middleware.

**Negative:**

- Legitimate users can be locked out if they forget their password.
- Lockout by IP can affect users sharing NAT/proxy addresses.
- `AxesBackend` as the first backend adds a small overhead to every authentication check.

**Mitigations:**

- 15-minute lockout duration is short enough to not frustrate legitimate users.
- Password reset functionality allows self-service account recovery.
- The `SecuritySettings` model (ADR-0011) stores `max_login_attempts` and `lockout_duration_minutes` for admin configurability.
