# 0005. Use Custom User Model

**Status:** Accepted
**Date:** 2024-07-01

## Context

Django's default `auth.User` model lacks:

- Role-based access control (RBAC) fields
- Two-factor authentication (2FA) support
- Account status lifecycle management (active, suspended, locked)
- Audit fields (last activity, failed login attempts)
- A related profile model for extended personal data

The CMS requires a role hierarchy (Superuser, Administrator, Editor, Viewer) and security features that the default model cannot support.

## Decision

We define a custom `User` model set via `AUTH_USER_MODEL = 'users.User'` in settings. This must be configured **before the first migration** — a well-known Django requirement.

```python
# apps/users/models.py
class User(UUIDPrimaryKeyMixin, TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=UserRole.choices, default=UserRole.VIEWER)
    two_factor_enabled = models.BooleanField(default=False)
    account_status = models.CharField(max_length=20, choices=AccountStatus.choices, default=AccountStatus.ACTIVE)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    last_activity = models.DateTimeField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    force_password_change = models.BooleanField(default=False)
    # ... AbstractBaseUser, PermissionsMixin fields
```

Supporting models:

- `UserProfile` — OneToOneField to User for avatar, bio, phone, address
- `LoginHistory` — Audit trail for login attempts
- `PasswordHistory` — Prevents password reuse
- `AuditLog` — System-wide action tracking
- `EmailVerification` — Token-based email confirmation
- `TwoFactorDevice` — TOTP secrets for 2FA

## Consequences

**Positive:**

- RBAC via `role` field with 4 choices: `SUPERUSER`, `ADMINISTRATOR`, `EDITOR`, `VIEWER`.
- 2FA support via `TOTPHelper` class implementing RFC 6238.
- Account locking integrates with `django-axes` for brute-force protection.
- `UserProfile` separation keeps the main User table lean.
- Custom `UserManager` handles `create_user()` and `create_superuser()` with role defaults.

**Negative:**

- Must set `AUTH_USER_MODEL` before any migrations (cannot change later without data migration).
- All ForeignKey references to User must use `settings.AUTH_USER_MODEL` string notation.
- Slightly more complex than using Django's default.

**Mitigations:**

- `AUTH_USER_MODEL = 'users.User'` is set in `config/settings/base.py` from project inception.
- Custom `UserManager` ensures consistent user creation across admin and management commands.
- `UserRole` choices are defined in `utils/choices.py` for reuse across the codebase.
