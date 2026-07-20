from django.urls import path
from . import views

app_name = 'broadcast'

urlpatterns = [
    # Dashboard
    path('', views.BroadcastDashboardView.as_view(), name='dashboard'),

    # Program
    path('program/', views.ProgramListView.as_view(), name='program_list'),
    path('program/buat/', views.ProgramCreateView.as_view(), name='program_create'),
    path('program/<uuid:pk>/edit/', views.ProgramEditView.as_view(), name='program_edit'),
    path('program/<uuid:pk>/hapus/', views.ProgramDeleteView.as_view(), name='program_delete'),

    # Host
    path('host/', views.HostListView.as_view(), name='host_list'),
    path('host/buat/', views.HostCreateView.as_view(), name='host_create'),
    path('host/<uuid:pk>/edit/', views.HostEditView.as_view(), name='host_edit'),
    path('host/<uuid:pk>/hapus/', views.HostDeleteView.as_view(), name='host_delete'),

    # Schedule
    path('jadwal/', views.ScheduleListView.as_view(), name='schedule_list'),
    path('jadwal/buat/', views.ScheduleCreateView.as_view(), name='schedule_create'),
    path('jadwal/<uuid:pk>/edit/', views.ScheduleEditView.as_view(), name='schedule_edit'),
    path('jadwal/<uuid:pk>/hapus/', views.ScheduleDeleteView.as_view(), name='schedule_delete'),

    # Broadcast Sessions
    path('sesi/', views.BroadcastSessionListView.as_view(), name='session_list'),
    path('sesi/buat/', views.BroadcastSessionCreateView.as_view(), name='session_create'),
    path('sesi/<uuid:pk>/edit/', views.BroadcastSessionEditView.as_view(), name='session_edit'),
    path('sesi/<uuid:pk>/hapus/', views.BroadcastSessionDeleteView.as_view(), name='session_delete'),

    # Episodes
    path('episode/', views.EpisodeListView.as_view(), name='episode_list'),
    path('episode/buat/', views.EpisodeCreateView.as_view(), name='episode_create'),
    path('episode/<uuid:pk>/edit/', views.EpisodeEditView.as_view(), name='episode_edit'),
    path('episode/<uuid:pk>/hapus/', views.EpisodeDeleteView.as_view(), name='episode_delete'),

    # Announcements
    path('playlist/', views.PlaylistListView.as_view(), name='playlist_list'),
    path('playlist/buat/', views.PlaylistCreateView.as_view(), name='playlist_create'),
    path('playlist/<uuid:pk>/edit/', views.PlaylistEditView.as_view(), name='playlist_edit'),
    path('playlist/<uuid:pk>/hapus/', views.PlaylistDeleteView.as_view(), name='playlist_delete'),

    path('pengumuman/', views.AnnouncementListView.as_view(), name='announcement_list'),
    path('pengumuman/buat/', views.AnnouncementCreateView.as_view(), name='announcement_create'),
    path('pengumuman/<uuid:pk>/edit/', views.AnnouncementEditView.as_view(), name='announcement_edit'),
    path('pengumuman/<uuid:pk>/hapus/', views.AnnouncementDeleteView.as_view(), name='announcement_delete'),

    # Calendar
    path('kalender/', views.CalendarView.as_view(), name='calendar'),

    # CMS Program
    path('cms/program/', views.ProgramCMSListView.as_view(), name='cms_program_list'),
    path('cms/program/tambah/', views.ProgramCMSCreateView.as_view(), name='cms_program_create'),
    path('cms/program/<uuid:pk>/', views.ProgramCMSDetailView.as_view(), name='cms_program_detail'),
    path('cms/program/<uuid:pk>/edit/', views.ProgramCMSUpdateView.as_view(), name='cms_program_edit'),
    path('cms/program/<uuid:pk>/hapus/', views.ProgramCMSDeleteView.as_view(), name='cms_program_delete'),
    path('cms/program/<uuid:pk>/workflow/', views.ProgramCMSWorkflowView.as_view(), name='cms_program_workflow'),
    # CMS Episodes
    path('cms/episode/', views.BroadcastEpisodeCMSListView.as_view(), name='cms_episode_list'),
    path('cms/episode/tambah/', views.BroadcastEpisodeCMSCreateView.as_view(), name='cms_episode_create'),
    path('cms/episode/<uuid:pk>/', views.BroadcastEpisodeCMSDetailView.as_view(), name='cms_episode_detail'),
    path('cms/episode/<uuid:pk>/edit/', views.BroadcastEpisodeCMSUpdateView.as_view(), name='cms_episode_edit'),
    path('cms/episode/<uuid:pk>/hapus/', views.BroadcastEpisodeCMSDeleteView.as_view(), name='cms_episode_delete'),
    path('cms/episode/<uuid:pk>/workflow/', views.BroadcastEpisodeCMSWorkflowView.as_view(), name='cms_episode_workflow'),

    # Public API
    path('api/programs/', views.ProgramListAPIView.as_view(), name='api_programs'),
    path('api/program/<slug:slug>/', views.ProgramDetailAPIView.as_view(), name='api_program_detail'),
    path('api/schedule/', views.ScheduleAPIView.as_view(), name='api_schedule'),
    path('api/today/', views.TodayScheduleAPIView.as_view(), name='api_today'),
    path('api/current/', views.CurrentBroadcastAPIView.as_view(), name='api_current'),
    path('api/next/', views.NextBroadcastAPIView.as_view(), name='api_next'),
    path('api/hosts/', views.HostListAPIView.as_view(), name='api_hosts'),
    path('api/host/<uuid:pk>/', views.HostDetailAPIView.as_view(), name='api_host_detail'),
    path('api/episodes/', views.EpisodeListAPIView.as_view(), name='api_episodes'),
    path('api/playlist/', views.PlaylistAPIView.as_view(), name='api_playlist'),
]
