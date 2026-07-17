from django.urls import path
from . import views

app_name = 'podcast'

urlpatterns = [
    # CMS Podcast
    path('cms/podcast/', views.PodcastCMSListView.as_view(), name='cms_podcast_list'),
    path('cms/podcast/tambah/', views.PodcastCMSCreateView.as_view(), name='cms_podcast_create'),
    path('cms/podcast/<uuid:pk>/', views.PodcastCMSDetailView.as_view(), name='cms_podcast_detail'),
    path('cms/podcast/<uuid:pk>/edit/', views.PodcastCMSUpdateView.as_view(), name='cms_podcast_edit'),
    path('cms/podcast/<uuid:pk>/hapus/', views.PodcastCMSDeleteView.as_view(), name='cms_podcast_delete'),
    path('cms/podcast/<uuid:pk>/workflow/', views.PodcastCMSWorkflowView.as_view(), name='cms_podcast_workflow'),
    # CMS Episodes
    path('cms/episode/', views.PodcastEpisodeCMSListView.as_view(), name='cms_episode_list'),
    path('cms/episode/tambah/', views.PodcastEpisodeCMSCreateView.as_view(), name='cms_episode_create'),
    path('cms/episode/<uuid:pk>/', views.PodcastEpisodeCMSDetailView.as_view(), name='cms_episode_detail'),
    path('cms/episode/<uuid:pk>/edit/', views.PodcastEpisodeCMSUpdateView.as_view(), name='cms_episode_edit'),
    path('cms/episode/<uuid:pk>/hapus/', views.PodcastEpisodeCMSDeleteView.as_view(), name='cms_episode_delete'),
    path('cms/episode/<uuid:pk>/workflow/', views.PodcastEpisodeCMSWorkflowView.as_view(), name='cms_episode_workflow'),
]
