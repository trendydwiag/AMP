from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'studio'

urlpatterns = [
    path('', views.AMPStudioDashboardView.as_view(), name='dashboard'),
    path('kalender/', views.AMPStudioCalendarView.as_view(), name='calendar'),
    path('media/', views.AMPStudioMediaExplorerView.as_view(), name='media_explorer'),
    path('analytics/', views.AMPStudioAnalyticsView.as_view(), name='analytics'),
    path('preview/<str:content_type>/<uuid:pk>/', views.AMPStudioPreviewView.as_view(), name='preview'),
    path('partner/switch/<uuid:partner_pk>/', views.PartnerSwitchView.as_view(), name='partner_switch'),
    path('partner/list/', views.PartnerListView.as_view(), name='partner_list'),
    # Sprint 3.5 — Founder Experience
    path('streaming/', views.StreamingCenterView.as_view(), name='streaming_center'),
    path('setup/', views.SetupWizardView.as_view(), name='setup_wizard'),
    # Broken-link redirect: /studio/stream/ → /studio/streaming/
    path('stream/', RedirectView.as_view(pattern_name='studio:streaming_center', permanent=True)),
    path('stream', RedirectView.as_view(pattern_name='studio:streaming_center', permanent=True)),
    # Sprint 3.6 — stub pages for previously dead sidebar links
    path('komunitas/', views.CommunityView.as_view(), name='community'),
    path('iklan/', views.IklanView.as_view(), name='iklan'),
]
