from django.urls import path
from .views import (
    ArticleCMSListView, ArticleCMSCreateView, ArticleCMSUpdateView,
    ArticleCMSDeleteView, ArticleCMSDetailView, ArticleCMSWorkflowView,
    ArticleCMSPublishView, ArticleCMSUnpublishView, ArticleCMSScheduleView,
    ArticleCMSAutosaveView,
)

app_name = 'news'

urlpatterns = [
    # CMS Article Management
    path('cms/artikel/', ArticleCMSListView.as_view(), name='cms_article_list'),
    path('cms/artikel/tambah/', ArticleCMSCreateView.as_view(), name='cms_article_create'),
    path('cms/artikel/<uuid:pk>/', ArticleCMSDetailView.as_view(), name='cms_article_detail'),
    path('cms/artikel/<uuid:pk>/edit/', ArticleCMSUpdateView.as_view(), name='cms_article_edit'),
    path('cms/artikel/<uuid:pk>/hapus/', ArticleCMSDeleteView.as_view(), name='cms_article_delete'),
    path('cms/artikel/<uuid:pk>/workflow/', ArticleCMSWorkflowView.as_view(), name='cms_article_workflow'),
    path('cms/artikel/<uuid:pk>/publish/', ArticleCMSPublishView.as_view(), name='cms_article_publish'),
    path('cms/artikel/<uuid:pk>/unpublish/', ArticleCMSUnpublishView.as_view(), name='cms_article_unpublish'),
    path('cms/artikel/<uuid:pk>/schedule/', ArticleCMSScheduleView.as_view(), name='cms_article_schedule'),
    path('cms/artikel/<uuid:pk>/autosave/', ArticleCMSAutosaveView.as_view(), name='cms_article_autosave'),
]
