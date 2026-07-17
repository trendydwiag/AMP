from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize Django Admin Branding
admin.site.site_header = 'Kabulhaden CMS'
admin.site.site_title = 'Kabulhaden CMS Admin'
admin.site.index_title = 'Panel Kontrol Kabulhaden CMS'

# Define custom error handlers
handler400 = 'apps.core.views.bad_request'
handler403 = 'apps.core.views.permission_denied'
handler404 = 'apps.core.views.page_not_found'
handler500 = 'apps.core.views.server_error'

urlpatterns = [
    # AMP Studio — Premium Admin Interface
    path('studio/', include('apps.studio.urls')),

    # Public Website
    path('', include('apps.website.urls')),

    # Django Admin Panel
    path('admin/', admin.site.urls),

    # Core system views (Homepage, Health checks)
    path('', include('apps.core.urls')),

    # Authentication & User Management
    path('akun/', include('apps.users.urls')),

    # System Settings
    path('pengaturan/', include('apps.settings.urls')),

    # Media Manager
    path('media/', include('apps.media_manager.urls')),

    # Radio Engine
    path('radio/', include('apps.radio.urls')),

    # AMP Internal API v1 — normalized, provider-agnostic endpoints for all UI
    path('api/v1/', include('apps.radio.api_v1_urls')),

    # Broadcast Management
    path('broadcast/', include('apps.broadcast.urls')),

    # News & Article CMS
    path('berita/', include('apps.news.urls')),

    # Podcast
    path('podcast/', include('apps.podcast.urls')),

    # Content Management
    path('konten/', include('apps.content.urls')),

    # Platform Management
    path('platform/', include('apps.platform.urls')),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Enable django-debug-toolbar in development if installed
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
