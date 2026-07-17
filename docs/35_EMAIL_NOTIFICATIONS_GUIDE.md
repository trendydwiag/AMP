# 35. Email & Notifications Guide

## Overview

This guide covers the email and notification systems in Kabulhaden CMS, including transactional emails, in-app notifications, and push notifications.

---

## Email System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Email System                             │
│                                                              │
│  ┌─────────────────┐     ┌─────────────────────────────┐    │
│  │   Django Admin   │────▶│     Email Backend            │    │
│  │   User Actions   │     │  (SMTP / Console / File)     │    │
│  └─────────────────┘     └──────────────┬──────────────┘    │
│                                          │                   │
│                         ┌────────────────┼────────────────┐  │
│                         ▼                ▼                ▼  │
│                   ┌──────────┐    ┌──────────┐    ┌────────┐ │
│                   │  SMTP    │    │ Console  │    │  File  │ │
│                   │  Server  │    │  Output  │    │  Log   │ │
│                   └──────────┘    └──────────┘    └────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Email Configuration

```python
# config/settings/base.py
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env('EMAIL_PORT', default=587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='Kabulhaden <noreply@kabulhaden.id>')
```

---

## Email Templates

### Available Templates

| Template | Purpose | Trigger |
|----------|---------|---------|
| `verification_email.html` | Email verification | Registration |
| `password_reset_email.html` | Password reset | Reset request |
| `welcome_email.html` | Welcome new user | Admin creates user |
| `role_change_email.html` | Role updated | Admin changes role |
| `password_changed_email.html` | Password changed | User changes password |
| `weekly_digest.html` | Weekly summary | Cron job |

### Email Template Structure

```html
<!-- templates/emails/base_email.html -->
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #1e3a5f; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f9f9f9; }
        .button { 
            display: inline-block; 
            padding: 12px 24px; 
            background: #1e3a5f; 
            color: white; 
            text-decoration: none; 
            border-radius: 4px; 
        }
        .footer { padding: 20px; text-align: center; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Kabulhaden CMS</h1>
        </div>
        <div class="content">
            {% block content %}{% endblock %}
        </div>
        <div class="footer">
            <p>&copy; {{ year }} Kabulhaden Community Radio</p>
        </div>
    </div>
</body>
</html>
```

### Verification Email

```html
<!-- templates/emails/verification_email.html -->
{% extends 'emails/base_email.html' %}

{% block content %}
<h2>Verifikasi Email Anda</h2>
<p>Hai {{ user.first_name }},</p>
<p>Terima kasih telah mendaftar di Kabulhaden CMS.</p>
<p>Silakan klik tombol di bawah untuk memverifikasi email Anda:</p>

<p style="text-align: center; margin: 30px 0;">
    <a href="{{ verification_url }}" class="button">Verifikasi Email</a>
</p>

<p>Link ini akan kedaluwarsa dalam 24 jam.</p>
<p>Jika Anda tidak mendaftar, abaikan email ini.</p>
{% endblock %}
```

---

## Email Service

```python
# apps/users/services.py
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailService:
    @staticmethod
    def send_verification_email(user, token):
        verification_url = f"{settings.SITE_URL}/akun/verifikasi-email/?token={token}"
        
        html_message = render_to_string('emails/verification_email.html', {
            'user': user,
            'verification_url': verification_url,
            'year': timezone.now().year,
        })
        
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject='Verifikasi Email - Kabulhaden CMS',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
        )
    
    @staticmethod
    def send_password_reset_email(user, token):
        reset_url = f"{settings.SITE_URL}/akun/reset-password/konfirmasi/?token={token}"
        
        html_message = render_to_string('emails/password_reset_email.html', {
            'user': user,
            'reset_url': reset_url,
            'year': timezone.now().year,
        })
        
        send_mail(
            subject='Reset Password - Kabulhaden CMS',
            message=strip_tags(html_message),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
        )
    
    @staticmethod
    def send_welcome_email(user, temp_password):
        html_message = render_to_string('emails/welcome_email.html', {
            'user': user,
            'temp_password': temp_password,
            'login_url': f"{settings.SITE_URL}/akun/masuk/",
            'year': timezone.now().year,
        })
        
        send_mail(
            subject='Selamat Datang di Kabulhaden CMS',
            message=strip_tags(html_message),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
        )
```

---

## In-App Notifications

### Notification Model

```python
# apps/core/models.py
class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=[
        ('info', 'Info'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ])
    link = models.URLField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
```

### Notification UI

```
┌──────────────────────────────────────────────────────────┐
│  🔔 Notifikasi (3)                       [Tandai semua   │
│                                            dibaca]       │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 🔴 Encoder "Studio A" terputus                     │  │
│  │    5 menit lalu                                    │  │
│  └────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 🟢 Berita "Hari Kemerdekaan" berhasil dipublikasi │  │
│  │    1 jam lalu                                      │  │
│  └────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 🟡 Jadwal baru ditambahkan untuk Senin             │  │
│  │    2 jam lalu                                      │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### Notification Service

```python
# apps/core/services.py
class NotificationService:
    @staticmethod
    def create_notification(user, title, message, notification_type='info', link=''):
        return Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            link=link,
        )
    
    @staticmethod
    def notify_stream_error(station, error_message):
        admins = CustomUser.objects.filter(
            role__in=['ADMINISTRATOR', 'SUPERUSER'],
            is_active=True
        )
        for admin in admins:
            NotificationService.create_notification(
                user=admin,
                title=f'Encoder "{station.name}" terputus',
                message=error_message,
                notification_type='error',
                link=f'/broadcast/encoder/{station.pk}/',
            )
    
    @staticmethod
    def notify_content_published(content, author):
        editors = CustomUser.objects.filter(
            role__in=['EDITOR', 'ADMINISTRATOR', 'SUPERUSER'],
            is_active=True
        ).exclude(pk=author.pk)
        
        for user in editors:
            NotificationService.create_notification(
                user=user,
                title=f'Konten "{content.title}" berhasil dipublikasi',
                message=f'{author.get_full_name()} telah mempublikasikan konten baru.',
                notification_type='success',
                link=f'/berita/{content.slug}/',
            )
```

---

## Push Notifications (Future)

### Web Push (pywebpush)

```python
# requirements additions
pywebpush==2.0.0

# config/settings/base.py
VAPID_PRIVATE_KEY = env('VAPID_PRIVATE_KEY', default='')
VAPID_PUBLIC_KEY = env('VAPID_PUBLIC_KEY', default='')
VAPID_CLAIMS = {'sub': 'mailto:admin@kabulhaden.id'}
```

### Push Notification Types

| Event | Title | Priority |
|-------|-------|----------|
| Stream live | "Radio is Live!" | High |
| Stream error | "Encoder Disconnected" | High |
| New comment | "New Comment on Article" | Normal |
| Scheduled publish | "Content Published" | Normal |
| Weekly digest | "Weekly Summary" | Low |

---

## Email Queue (Background Processing)

### Using Django-Q or Celery

```python
# tasks/email_tasks.py
from django_q.tasks import async_task


def send_verification_email_async(user_id):
    user = CustomUser.objects.get(pk=user_id)
    EmailService.send_verification_email(user)


def send_notification_email_async(notification_id):
    notification = Notification.objects.get(pk=notification_id)
    EmailService.send_notification(notification)
```

### Task Scheduling

```python
# Weekly digest cron
from django_q.tasks import schedule

schedule(
    'tasks.email_tasks.send_weekly_digest',
    schedule_type='W',
    cron='0 9 * * 1',  # Every Monday at 9 AM
)
```

---

## Notification Preferences

```python
# apps/users/models.py
class NotificationPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Email notifications
    email_stream_errors = models.BooleanField(default=True)
    email_content_published = models.BooleanField(default=True)
    email_new_comments = models.BooleanField(default=False)
    email_weekly_digest = models.BooleanField(default=True)
    
    # In-app notifications
    app_stream_errors = models.BooleanField(default=True)
    app_content_published = models.BooleanField(default=True)
    app_new_comments = models.BooleanField(default=True)
    
    # Push notifications
    push_enabled = models.BooleanField(default=False)
    push_stream_errors = models.BooleanField(default=True)
```

---

## Email Templates Index

| Template | Subject | Auto-Translated |
|----------|---------|:---------------:|
| `verification_email.html` | Verifikasi Email - Kabulhaden CMS | ✓ |
| `password_reset_email.html` | Reset Password - Kabulhaden CMS | ✓ |
| `welcome_email.html` | Selamat Datang di Kabulhaden CMS | ✓ |
| `role_change_email.html` | Perubahan Role - Kabulhaden CMS | ✓ |
| `password_changed_email.html` | Password Berhasil Diubah | ✓ |
| `weekly_digest.html` | Ringkasan Mingguan - Kabulhaden CMS | ✓ |

---

## Testing Emails

### Development Console Backend

```python
# config/settings/development.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Test Email Sending

```bash
python manage.py sendtestemail user@example.com --subject="Test Email"
```

### Unit Tests

```python
from django.core import mail
from django.test import TestCase


class EmailServiceTest(TestCase):
    def test_verification_email_sent(self):
        user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        EmailService.send_verification_email(user, 'test-token')
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Verifikasi Email - Kabulhaden CMS')
        self.assertIn(user.email, mail.outbox[0].to)
```

---

## Related Documentation

- `17_TOAST_NOTIFICATION.md` - Toast notification UI
- `23_ACCESSIBILITY.md` - Accessible notifications
- `26_ALPINEJS_PATTERNS.md` - Dynamic notification badge
- `18_LOADING_STATES.md` - Loading states for async sends

---

*Last updated: 2026-07-15*
