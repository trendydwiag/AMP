from .base import *

# Override debug mode
DEBUG = True

# Disable security policies for local development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Content Security Policy (CSP) for dev: Allow local hot reloads, CDNs, inline tools
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'", "https://cdn.jsdelivr.net", "https://unpkg.com")
CSP_IMG_SRC = ("'self'", "data:", "https://images.unsplash.com")
CSP_CONNECT_SRC = ("'self'", "ws:", "http:")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com")
CSP_OBJECT_SRC = ("'none'",)

# Allow all Replit proxy origins for CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://*.replit.dev',
    'https://*.repl.co',
    'http://localhost:5000',
    'http://127.0.0.1:5000',
]

# Dev specific emails
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# If django-debug-toolbar is installed, add it
try:
    import debug_toolbar
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1', 'localhost']
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        # ProfilingPanel crashes with "Another profiling tool is already active"
        # when concurrent requests arrive (e.g. radio status poller every 10s).
        'DISABLE_PANELS': {
            'debug_toolbar.panels.profiling.ProfilingPanel',
        },
    }
except ImportError:
    pass

# Use basic static files storage in dev to bypass manifest generation requirement
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

