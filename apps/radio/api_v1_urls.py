"""
AMP API v1 — radio endpoints.

All frontend UI must consume only these normalized endpoints.
Provider-specific URLs (e.g. a7.siar.us) must never appear in templates or JS.
"""
from django.urls import path
from .views import LiveRadioAPIView

urlpatterns = [
    path('radio/live/', LiveRadioAPIView.as_view(), name='api_v1_radio_live'),
]
