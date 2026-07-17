# 32. Authentication & Authorization Guide

## Overview

This guide documents the authentication and authorization system in Kabulhaden CMS, including user roles, permissions, decorators, middleware, and security best practices.

---

## User Roles Hierarchy

```
SUPERUSER
    │
    ▼
ADMINISTRATOR
    │
    ▼
EDITOR
    │
    ▼
VIEWER
```

### Role Definitions

| Role | Description | Permissions |
|------|-------------|-------------|
| `SUPERUSER` | Full system access | All permissions, can manage admins |
| `ADMINISTRATOR` | CMS management | Manage users, settings, all content |
| `EDITOR` | Content creation | Create/edit/publish content |
| `VIEWER` | Read-only access | View content only |

### Role Choices (from `utils/choices.py`)

```python
class UserRole(models.TextChoices):
    SUPERUSER = 'SUPERUSER', 'Superuser'
    ADMINISTRATOR = 'ADMINISTRATOR', 'Administrator'
    EDITOR = 'EDITOR', 'Editor'
    VIEWER = 'VIEWER', 'Viewer'
```

---

## Authentication Flow

### Login Process

```
┌─────────────┐
│  User visits  │
│  /akun/masuk/ │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Enter email  │
│  & password   │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Django backend   │
│  authenticates    │
│  + Axes check     │
└──────┬──────────┘
       │
       ├──→ Fail: Increment attempt counter
       │    (After 5 attempts: Lock for 1 hour)
       │
       ▼
┌─────────────────┐
│  Check email     │
│  verified?       │
└──────┬──────────┘
       │
       ├──→ No: Redirect to verification page
       │
       ▼
┌─────────────────┐
│  Check password  │
│  expired?        │
└──────┬──────────┘
       │
       ├──→ Yes: Force password change
       │
       ▼
┌─────────────────┐
│  Login success   │
│  Create session  │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Redirect to     │
│  /akun/dashboard/│
└─────────────────┘
```

### Session Management

```python
# config/settings/base.py
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True  # Production only
```

---

## Authorization Decorators

### Available Decorators (`apps/users/decorators.py`)

| Decorator | Purpose |
|-----------|---------|
| `@login_required_custom` | Custom login check with redirect |
| `@role_required(*roles)` | Require specific role(s) |
| `@admin_required` | Require ADMINISTRATOR or SUPERUSER |
| `@email_verified_required` | Require verified email |
| `@guest_only` | Only allow unauthenticated users |
| `@force_password_change_required` | Redirect if password change needed |

### Usage Examples

```python
from apps.users.decorators import (
    login_required_custom,
    role_required,
    admin_required,
    email_verified_required,
)

@login_required_custom
def dashboard_view(request):
    """Any logged-in user."""
    pass

@admin_required
def user_create_view(request):
    """ADMINISTRATOR or SUPERUSER only."""
    pass

@role_required('EDITOR', 'ADMINISTRATOR', 'SUPERUSER')
def content_create_view(request):
    """EDITOR, ADMINISTRATOR, or SUPERUSER."""
    pass

@email_verified_required
def verified_view(request):
    """User must have verified email."""
    pass
```

### Role Check Logic

```python
# From apps/users/decorators.py
def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('users:login')
            
            if request.user.role not in allowed_roles:
                messages.error(request, 'Akses ditolak.')
                return redirect('users:dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
```

---

## Middleware Stack

### Request Processing Order

```
Request
    │
    ▼
┌─────────────────────────┐
│ SessionMiddleware        │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ AuthenticationMiddleware │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ SecurityMiddleware       │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ AxesMiddleware           │  ← Brute-force protection
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ SessionTimeoutMiddleware │  ← Auto-logout after inactivity
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ LastActivityMiddleware   │  ← Track last activity time
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ AuditLoggingMiddleware   │  ← Log user actions
└────────────┬────────────┘
             │
             ▼
         View
```

### Axes Configuration

```python
# config/settings/base.py
INSTALLED_APPS = [
    ...
    'axes',
    ...
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Axes settings
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = timedelta(hours=1)
AXES_LOCKOUT_TEMPLATE = 'users/locked_out.html'
AXES_RESET_ON_SUCCESS = True
```

### Session Timeout Middleware

```python
# apps/users/middleware.py
class SessionTimeoutMiddleware:
    TIMEOUT_MINUTES = 30
    
    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                elapsed = timezone.now() - datetime.fromisoformat(last_activity)
                if elapsed > timedelta(minutes=self.TIMEOUT_MINUTES):
                    logout(request)
                    messages.warning(request, 'Sesi expired. Silakan masuk kembali.')
                    return redirect('users:login')
            request.session['last_activity'] = timezone.now().isoformat()
        
        response = self.get_response(request)
        return response
```

### Audit Logging Middleware

```python
# apps/core/middleware.py
class AuditLoggingMiddleware:
    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated:
            AuditLog.objects.create(
                user=request.user,
                action=request.method,
                path=request.path,
                ip_address=self.get_client_ip(request),
                status_code=response.status_code,
            )
        
        return response
```

---

## Password Policies

### Validation Rules

```python
# utils/validators.py
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

### Custom Validation

```python
class StrongPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError('Password minimal 8 karakter.')
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password harus mengandung huruf besar.')
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password harus mengandung huruf kecil.')
        if not re.search(r'\d', password):
            raise ValidationError('Password harus mengandung angka.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Password harus mengandung simbol.')
```

---

## Permission Matrix

### Users Management

| Action | VIEWER | EDITOR | ADMINISTRATOR | SUPERUSER |
|--------|--------|--------|---------------|-----------|
| View users | ✗ | ✗ | ✓ | ✓ |
| Create users | ✗ | ✗ | ✓ | ✓ |
| Edit users | ✗ | ✗ | ✓ | ✓ |
| Delete users | ✗ | ✗ | ✗ | ✓ |
| Change roles | ✗ | ✗ | ✗ | ✓ |

### Content Management

| Action | VIEWER | EDITOR | ADMINISTRATOR | SUPERUSER |
|--------|--------|--------|---------------|-----------|
| View content | ✓ | ✓ | ✓ | ✓ |
| Create content | ✗ | ✓ | ✓ | ✓ |
| Edit content | ✗ | ✓* | ✓ | ✓ |
| Delete content | ✗ | ✗ | ✓ | ✓ |
| Publish content | ✗ | ✗ | ✓ | ✓ |

*Editor can only edit own content

### Settings

| Action | VIEWER | EDITOR | ADMINISTRATOR | SUPERUSER |
|--------|--------|--------|---------------|-----------|
| View settings | ✗ | ✗ | ✓ | ✓ |
| Edit settings | ✗ | ✗ | ✓ | ✓ |

*See `permission_matrix.md` for complete matrix*

---

## Email Verification Flow

```
┌─────────────────┐
│  User registers  │
│  or requests     │
│  verification    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Generate token  │
│  (expires: 24h)  │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Send email with │
│  verification    │
│  link            │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  User clicks     │
│  link            │
└──────┬──────────┘
       │
       ├──→ Expired: Show error, option to resend
       │
       ▼
┌─────────────────┐
│  Mark email as   │
│  verified        │
└─────────────────┘
```

---

## Security Headers (Production)

```python
# config/settings/production.py
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## Related Documentation

- `permission_matrix.md` - Complete permission matrix
- `03_USER_PERSONAS.md` - User role descriptions
- `14_FORM_DESIGN.md` - Login/form patterns
- `20_ERROR_PAGES.md` - Error page handling

---

*Last updated: 2026-07-15*
