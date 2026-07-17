# 0014. Use Custom Session Timeout Middleware

**Status:** Accepted
**Date:** 2024-07-15

## Context

Django does not provide built-in session timeout functionality. Without it:

- Admin sessions remain active indefinitely after login
- Shared computers may leave admin panels accessible
- Compliance with security policies requires automatic session expiry
- There is no visibility into user activity timestamps

The `django-axes` brute force protection (ADR-0013) handles login attacks but does not address post-login session management.

## Decision

We implement two custom middleware classes in `apps/users/middleware.py`:

### SessionTimeoutMiddleware

Automatically logs out users after a configurable period of inactivity:

```python
class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.timeout_minutes = getattr(settings, 'SESSION_TIMEOUT_MINUTES', 60)

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                last_activity_time = timezone.datetime.fromisoformat(last_activity)
                if timezone.now() - last_activity_time > timedelta(minutes=self.timeout_minutes):
                    logout(request)
                    messages.warning(request, "Sesi Anda telah berakhir karena tidak ada aktivitas.")
                    return HttpResponse(status=302, headers={'Location': f"/akun/masuk/?next={request.path}"})
            request.session['last_activity'] = timezone.now().isoformat()
        return self.get_response(request)
```

### LastActivityMiddleware

Updates the user's `last_activity` timestamp in the database (throttled to once per minute):

```python
class LastActivityMiddleware:
    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            now = timezone.now()
            if not request.user.last_activity or \
               (now - request.user.last_activity).total_seconds() > 60:
                UserRepository().update_last_activity(request.user)
        return response
```

Configuration:

```python
SESSION_TIMEOUT_MINUTES = env.int('SESSION_TIMEOUT_MINUTES', 60)  # Default: 60 minutes
```

## Consequences

**Positive:**

- Users are automatically logged out after 60 minutes of inactivity (configurable).
- Session timeout is enforced at the middleware level, covering all authenticated views.
- Indonesian-language warning message informs users why they were logged out.
- Redirect preserves the originally requested URL via `?next=` parameter.
- `LastActivityMiddleware` is throttled to avoid a database write on every single request.

**Negative:**

- Session timeout uses session storage (not database) for `last_activity`, so it does not survive session flush.
- The redirect response is a manual `HttpResponse(302)` rather than using Django's `redirect()` to avoid import circularity.
- If the session backend is file-based, concurrent requests can cause file locking.

**Mitigations:**

- Session data is lightweight (single ISO timestamp string).
- Future migration to Redis session backend (ADR-0020) eliminates file locking.
- `LastActivityMiddleware` provides a database-level `last_activity` for admin display.
