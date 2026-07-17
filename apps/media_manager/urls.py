from django.urls import path
from . import views

app_name = 'media_manager'

urlpatterns = [
    path('', views.MediaDashboardView.as_view(), name='dashboard'),
    path('file/', views.MediaListView.as_view(), name='list'),
    path('upload/', views.MediaUploadView.as_view(), name='upload'),
    path('file/<uuid:pk>/', views.MediaDetailView.as_view(), name='detail'),
    path('file/<uuid:pk>/hapus/', views.MediaDeleteView.as_view(), name='delete'),
    path('bulk-delete/', views.MediaBulkDeleteView.as_view(), name='bulk_delete'),
    path('folder/', views.FoldersView.as_view(), name='folders'),
    path('folder/buat/', views.FolderCreateView.as_view(), name='folder_create'),
    path('folder/<uuid:pk>/hapus/', views.FolderDeleteView.as_view(), name='folder_delete'),
    path('tag/', views.TagsView.as_view(), name='tags'),
    path('tag/buat/', views.TagCreateView.as_view(), name='tag_create'),
    path('tag/<uuid:pk>/hapus/', views.TagDeleteView.as_view(), name='tag_delete'),
    path('api/search/', views.MediaSearchAPIView.as_view(), name='api_search'),
]
