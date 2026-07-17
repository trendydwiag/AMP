# 33. Role-Based Access Control (RBAC) Guide

## Overview

This guide details the Role-Based Access Control system in Kabulhaden CMS, defining roles, permissions, and enforcement mechanisms across the application.

---

## RBAC Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    RBAC System                            │
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │    User      │  │    Role     │  │   Permission     │  │
│  │  (has role)  │──│  (has perms)│──│  (action+object) │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
│                                                          │
│  Enforcement Points:                                     │
│  - Decorators (view-level)                               │
│  - Middleware (request-level)                             │
│  - Templates (UI-level)                                  │
│  - Models (data-level)                                   │
└──────────────────────────────────────────────────────────┘
```

---

## Role Definitions

### Role Model

```python
# apps/users/models.py
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.VIEWER,
    )
    is_email_verified = models.BooleanField(default=False)
    # ...
```

### Role Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                       SUPERUSER                             │
│  - Full system access                                       │
│  - Can manage administrators                                │
│  - System configuration                                     │
│  - Can delete any content                                   │
└───────────────────────────┬─────────────────────────────────┘
                            │ delegates to
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    ADMINISTRATOR                             │
│  - User management (except superuser)                       │
│  - All settings                                             │
│  - All content types                                        │
│  - Broadcast control                                        │
└───────────────────────────┬─────────────────────────────────┘
                            │ delegates to
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                        EDITOR                               │
│  - Content creation/editing                                 │
│  - Media upload                                             │
│  - Own content management                                   │
│  - View statistics                                          │
└───────────────────────────┬─────────────────────────────────┘
                            │ limited to
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                        VIEWER                               │
│  - Read-only access                                         │
│  - View published content                                   │
│  - View public statistics                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Permission Matrix

### Users Module

| Action | VIEWER | EDITOR | ADMINISTRATOR | SUPERUSER |
|--------|:------:|:------:|:-------------:|:---------:|
| View user list | ✗ | ✗ | ✓ | ✓ |
| View user detail | ✗ | ✗ | ✓ | ✓ |
| Create user | ✗ | ✗ | ✓ | ✓ |
| Edit user | ✗ | ✗ | ✓ | ✓ |
| Delete user | ✗ | ✗ | ✗ | ✓ |
| Change user role | ✗ | ✗ | ✗ | ✓ |
| View own profile | ✓ | ✓ | ✓ | ✓ |
| Edit own profile | ✓ | ✓ | ✓ | ✓ |
| Change own password | ✓ | ✓ | ✓ | ✓ |

### Content Modules (News, Podcast, Community)

| Action | VIEWER | EDITOR | ADMINISTRATOR | SUPERUSER |
|--------|:------:|:------:|:-------------:|:---------:|
| View content list | ✓ | ✓ | ✓ | ✓ |
| View content detail | ✓ | ✓ | ✓ | ✓ |
| Create content | ✗ | ✓ | ✓ | ✓ |
| Edit own content | ✗ | ✓ | ✓ | ✓ |
| Edit any content | ✗ | ✗ | ✓ | ✓ |
| Delete own content | ✗ | ✗ | ✓ | ✓ |
| Delete any content | ✗ | ✗ | ✗ | ✓ |
| Publish content | ✗ | ✗ | ✓ | ✓ |

### Media Manager

| Action | VIEWER | EDITOR | ADMINISTRATOR | SUPERUSER |
|--------|:------:|:------:|:-------------:|:---------:|
| View media list | ✗ | ✓ | ✓ | ✓ |
| View media detail | ✗ | ✓ | ✓ | ✓ |
| Upload media | ✗ | ✓ | ✓ | ✓ |
| Edit media metadata | ✗ | ✓ | ✓ | ✓ |
| Delete media | ✗ | ✗ | ✓ | ✓ |
| Organize folders | ✗ | ✗ | ✓ | ✓ |
| Cleanup/compress | ✗ | ✗ | ✓ | ✓ |

### Radio Module

| Action | VIEWER | EDITOR | ADMINISTRATOR | SUPERUSER |
|--------|:------:|:------:|:-------------:|:---------:|
| View stations | ✓ | ✓ | ✓ | ✓ |
| View programs | ✓ | ✓ | ✓ | ✓ |
| View schedules | ✓ | ✓ | ✓ | ✓ |
| Create/edit stations | ✗ | ✗ | ✓ | ✓ |
| Create/edit programs | ✗ | ✓ | ✓ | ✓ |
| Create/edit schedules | ✗ | ✓ | ✓ | ✓ |
| Manage play queue | ✗ | ✗ | ✓ | ✓ |
| View statistics | ✗ | ✓ | ✓ | ✓ |
| Refresh cache | ✗ | ✗ | ✓ | ✓ |

### Broadcast Module

| Action | VIEWER | EDITOR | ADMINISTRATOR | SUPERUSER |
|--------|:------:|:------:|:-------------:|:---------:|
| View encoders | ✗ | ✗ | ✓ | ✓ |
| View streams | ✓ | ✓ | ✓ | ✓ |
| Start/stop encoder | ✗ | ✗ | ✓ | ✓ |
| Create/edit encoders | ✗ | ✗ | ✓ | ✓ |
| Create/edit streams | ✗ | ✗ | ✓ | ✓ |
| Manage playlists | ✗ | ✓ | ✓ | ✓ |
| View recordings | ✗ | ✗ | ✓ | ✓ |
| Download recordings | ✗ | ✗ | ✓ | ✓ |
| View statistics | ✗ | ✗ | ✓ | ✓ |

### Settings Module

| Action | VIEWER | EDITOR | ADMINISTRATOR | SUPERUSER |
|--------|:------:|:------:|:-------------:|:---------:|
| View settings | ✗ | ✗ | ✓ | ✓ |
| Edit settings | ✗ | ✗ | ✓ | ✓ |

---

## Enforcement Mechanisms

### 1. Decorator-Level (View Protection)

```python
# apps/users/decorators.py

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Silakan masuk terlebih dahulu.')
            return redirect('users:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('users:login')
            if request.user.role not in allowed_roles:
                messages.error(request, 'Anda tidak memiliki akses.')
                return redirect('users:dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def admin_required(view_func):
    return role_required('ADMINISTRATOR', 'SUPERUSER')(view_func)
```

### Usage in Views

```python
# apps/users/views.py
from apps.users.decorators import login_required_custom, admin_required


@login_required_custom
def profile_view(request):
    # Any authenticated user
    pass


@admin_required
def user_create_view(request):
    # ADMINISTRATOR or SUPERUSER only
    pass


@role_required('EDITOR', 'ADMINISTRATOR', 'SUPERUSER')
def content_create_view(request):
    # EDITOR, ADMINISTRATOR, or SUPERUSER
    pass
```

### 2. Middleware-Level (Session Checks)

```python
# apps/users/middleware.py

class SessionTimeoutMiddleware:
    """Auto-logout after 30 minutes inactivity."""
    
    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                elapsed = timezone.now() - datetime.fromisoformat(last_activity)
                if elapsed > timedelta(minutes=30):
                    from django.contrib.auth import logout
                    logout(request)
                    messages.warning(request, 'Sesi telah berakhir.')
                    return redirect('users:login')
            request.session['last_activity'] = timezone.now().isoformat()
        
        return self.get_response(request)


class LastActivityMiddleware:
    """Track user last activity for admin monitoring."""
    
    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            CustomUser.objects.filter(pk=request.user.pk).update(
                last_activity=timezone.now()
            )
        return response
```

### 3. Template-Level (UI Visibility)

```html
<!-- templates/includes/sidebar.html -->

{% if user.role == 'SUPERUSER' or user.role == 'ADMINISTRATOR' %}
<li class="nav-item">
    <a href="{% url 'users:user_list' %}">Pengguna</a>
</li>
<li class="nav-item">
    <a href="{% url 'settings:index' %}">Pengaturan</a>
</li>
{% endif %}

{% if user.role != 'VIEWER' %}
<li class="nav-item">
    <a href="{% url 'media:list' %}">Media</a>
</li>
{% endif %}

{% if user.role == 'SUPERUSER' or user.role == 'ADMINISTRATOR' or user.role == 'EDITOR' %}
<li class="nav-item">
    <a href="{% url 'radio:program_list' %}">Program</a>
</li>
{% endif %}
```

### 4. Model-Level (QuerySet Filtering)

```python
# apps/news/views.py

class NewsListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        user = self.request.user
        
        if user.role in ('SUPERUSER', 'ADMINISTRATOR'):
            return News.objects.all()
        elif user.role == 'EDITOR':
            return News.objects.filter(author=user)
        else:
            return News.objects.filter(status='published')
```

---

## Custom Permission Checks

### Utility Function

```python
# utils/permissions.py

def has_permission(user, action, model=None):
    """Check if user has permission for action on model."""
    permissions = {
        'SUPERUSER': {
            'create': True,
            'read': True,
            'update': True,
            'delete': True,
            'manage_users': True,
            'manage_settings': True,
        },
        'ADMINISTRATOR': {
            'create': True,
            'read': True,
            'update': True,
            'delete': True,
            'manage_users': True,
            'manage_settings': True,
        },
        'EDITOR': {
            'create': True,
            'read': True,
            'update': 'own',  # Only own content
            'delete': False,
            'manage_users': False,
            'manage_settings': False,
        },
        'VIEWER': {
            'create': False,
            'read': True,
            'update': False,
            'delete': False,
            'manage_users': False,
            'manage_settings': False,
        },
    }
    
    role_perms = permissions.get(user.role, {})
    return role_perms.get(action, False)


def can_edit_content(user, content):
    """Check if user can edit specific content."""
    if user.role in ('SUPERUSER', 'ADMINISTRATOR'):
        return True
    if user.role == 'EDITOR' and content.author == user:
        return True
    return False
```

---

## Role Assignment Rules

| Assignment | Allowed By | Constraints |
|------------|------------|-------------|
| SUPERUSER | Only existing SUPERUSER | Max 3 superusers |
| ADMINISTRATOR | SUPERUSER only | Max 10 administrators |
| EDITOR | ADMINISTRATOR, SUPERUSER | Unlimited |
| VIEWER | ADMINISTRATOR, SUPERUSER | Unlimited |
| Role downgrade | SUPERUSER only | Cannot downgrade self |
| Role upgrade | SUPERUSER only | — |

---

## Audit Trail

```python
# apps/core/models.py
class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20)  # CREATE, UPDATE, DELETE
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    changes = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
```

---

## Related Documentation

- `32_AUTHENTICATION_AUTHORIZATION_GUIDE.md` - Authentication flow
- `permission_matrix.md` - Complete permission matrix
- `03_USER_PERSONAS.md` - User role descriptions
- `23_ACCESSIBILITY.md` - Accessible role indicators

---

*Last updated: 2026-07-15*
