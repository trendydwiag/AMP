from django.urls import path
from . import views

app_name = 'radio'

urlpatterns = [
    path('', views.RadioDashboardView.as_view(), name='dashboard'),
    path('station/', views.RadioStationListView.as_view(), name='station_list'),
    path('station/buat/', views.RadioStationCreateView.as_view(), name='station_create'),
    path('station/<uuid:pk>/edit/', views.RadioStationEditView.as_view(), name='station_edit'),
    path('station/<uuid:pk>/hapus/', views.RadioStationDeleteView.as_view(), name='station_delete'),
    path('provider/', views.RadioProviderListView.as_view(), name='provider_list'),
    path('provider/buat/', views.RadioProviderCreateView.as_view(), name='provider_create'),
    path('provider/<uuid:pk>/edit/', views.RadioProviderEditView.as_view(), name='provider_edit'),
    path('provider/<uuid:pk>/hapus/', views.RadioProviderDeleteView.as_view(), name='provider_delete'),
    path('analytics/', views.RadioAnalyticsView.as_view(), name='analytics'),
    path('export/csv/<uuid:station_id>/', views.ExportCSVView.as_view(), name='export_csv'),
    path('export/excel/<uuid:station_id>/', views.ExportExcelView.as_view(), name='export_excel'),
    path('api/status/', views.RadioStatusAPIView.as_view(), name='api_status'),
    path('api/player/', views.RadioPlayerAPIView.as_view(), name='api_player'),
    path('api/now-playing/', views.RadioNowPlayingAPIView.as_view(), name='api_now_playing'),
    path('api/listener/', views.RadioListenerAPIView.as_view(), name='api_listener'),
    path('api/health/', views.RadioHealthAPIView.as_view(), name='api_health'),
    path('api/current-program/', views.RadioCurrentProgramAPIView.as_view(), name='api_current_program'),
    path('api/current-host/', views.RadioCurrentHostAPIView.as_view(), name='api_current_host'),
    path('api/providers/', views.RadioProvidersAPIView.as_view(), name='api_providers'),
    path('api/player-config/', views.RadioPlayerConfigAPIView.as_view(), name='api_player_config'),
]
