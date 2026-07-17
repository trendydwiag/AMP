import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialize environment variables reading
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Ensure logs directory exists
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# Quick-start development settings - unsuitable for production
SECRET_KEY = env.str('DJANGO_SECRET_KEY')
DEBUG = env.bool('DJANGO_DEBUG', False)

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Application definition
INSTALLED_APPS = [
    # Custom apps loaded first to support system configurations
    'apps.users.apps.UsersConfig',
    'apps.core.apps.CoreConfig',
    'apps.settings.apps.SettingsConfig',
    'apps.media_manager.apps.MediaManagerConfig',
    'apps.radio.apps.RadioConfig',
    'apps.broadcast.apps.BroadcastConfig',
    'apps.podcast.apps.PodcastConfig',
    'apps.news.apps.NewsConfig',
    'apps.sponsor.apps.SponsorConfig',
    'apps.community.apps.CommunityConfig',
    'apps.website.apps.WebsiteConfig',
    'apps.content.apps.ContentConfig',
    'apps.studio.apps.StudioConfig',
    'apps.platform.apps.PlatformConfig',

    # Core Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party extensions
    'axes',  # Brute force security protection
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise for efficient asset serving
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Custom middleware
    'apps.users.middleware.SessionTimeoutMiddleware',
    'apps.users.middleware.LastActivityMiddleware',

    # AMP Studio — redirect /admin/ to /studio/ (Sprint 3.5)
    'apps.core.middleware.AdminRedirectMiddleware',

    # Security/Audit Logging middleware
    'apps.core.middleware.AuditLoggingMiddleware',

    # Axes Middleware for brute force detection
    'axes.middleware.AxesMiddleware',

    # Platform: Partner resolution middleware
    'apps.platform.partner.middleware.PartnerMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.global_settings',  # Core custom processor
                'apps.platform.context_processors.partner_context',  # Platform partner context
                'apps.platform.context_processors.platform_settings',  # Platform settings
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': env.db('DATABASE_URL', default='sqlite:///db.sqlite3')
}

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',  # Keep axes at front
    'django.contrib.auth.backends.ModelBackend',
]

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,  # Enterprise security recommendation
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Axes Login Rate Limiting Configuration
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 15  # Minutes
AXES_LOCKOUT_PARAMETERS = ['username', 'ip_address']
AXES_RESET_ON_SUCCESS = True

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = env.str('LANGUAGE_CODE', 'id')
TIME_ZONE = env.str('TIME_ZONE', 'Asia/Jakarta')
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static_root'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files (User Uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Django 5.0 custom storages configuration
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Session Configuration
SESSION_TIMEOUT_MINUTES = env.int('SESSION_TIMEOUT_MINUTES', 60)
LOGIN_URL = '/akun/masuk/'
LOGIN_REDIRECT_URL = '/studio/'
LOGOUT_REDIRECT_URL = '/akun/masuk/'

# Password reset token expiration (hours)
PASSWORD_RESET_TIMEOUT_HOURS = env.int('PASSWORD_RESET_TIMEOUT_HOURS', 48)

# Email verification token expiration (hours)
EMAIL_VERIFICATION_EXPIRY_HOURS = env.int('EMAIL_VERIFICATION_EXPIRY_HOURS', 48)

# Avatar upload settings
AVATAR_MAX_SIZE_MB = env.int('AVATAR_MAX_SIZE_MB', 5)
AVATAR_ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']

# Logging Infrastructure
LOGGING_LEVEL = env.str('LOG_LEVEL', 'INFO')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': LOGGING_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'application_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'application.log',
            'formatter': 'verbose',
        },
        'security_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'security.log',
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'error.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        # Catch-all logger
        'django': {
            'handlers': ['console', 'application_file'],
            'level': LOGGING_LEVEL,
            'propagate': True,
        },
        # Database or general system operations
        'django.db.backends': {
            'handlers': ['application_file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Dedicated security / request logging
        'security': {
            'handlers': ['console', 'security_file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Handle server-level and request issues
        'django.request': {
            'handlers': ['error_file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security_file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'radio': {
            'handlers': ['console', 'application_file'],
            'level': LOGGING_LEVEL,
            'propagate': False,
        },
    },
}

# Radio Engine Configuration
RADIO_CACHE_TTL_NOW_PLAYING = env.int('RADIO_CACHE_TTL_NOW_PLAYING', 15)
RADIO_CACHE_TTL_LISTENER = env.int('RADIO_CACHE_TTL_LISTENER', 30)
RADIO_CACHE_TTL_HEALTH = env.int('RADIO_CACHE_TTL_HEALTH', 60)

# Live Streaming Configuration (Temporary Broadcastindo Integration)
# All UI must consume /api/v1/radio/live/ — only this settings block knows the provider URL.
# To swap providers: change STREAM_PROVIDER + STREAM_API_URL; no template or JS changes needed.
STREAM_PROVIDER = os.environ.get('STREAM_PROVIDER', 'broadcastindo')
STREAM_API_URL = os.environ.get('STREAM_API_URL', 'https://a7.siar.us/api/nowplaying/kabulhaden')
STREAM_STATION_NAME = os.environ.get('STREAM_STATION_NAME', 'Kabulhaden')
STREAM_CACHE_TTL = int(os.environ.get('STREAM_CACHE_TTL', '20'))
# Direct audio stream URL for the browser — used as fallback when metadata API is unreachable.
# The browser connects here directly, so network restrictions on the Django server don't apply.
STREAM_LISTEN_URL = os.environ.get('STREAM_LISTEN_URL', 'https://stream.kabulhaden.online:8000/radio.mp3')

# Platform Configuration
PLATFORM_BASE_DOMAIN = env.str('PLATFORM_BASE_DOMAIN', 'kabulhaden.com')
PLATFORM_DEFAULT_PARTNER_SLUG = env.str('PLATFORM_DEFAULT_PARTNER_SLUG', 'kabulhaden-online')
PLATFORM_FEATURE_FLAGS_ENABLED = env.bool('PLATFORM_FEATURE_FLAGS_ENABLED', True)
PLATFORM_PLUGINS_ENABLED = env.bool('PLATFORM_PLUGINS_ENABLED', True)
