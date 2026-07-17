from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('', views.CMSHomeView.as_view(), name='dashboard'),
    path('categories/', views.ContentCategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.ContentCategoryCreateView.as_view(), name='category_create'),
    path('categories/<uuid:pk>/edit/', views.ContentCategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<uuid:pk>/delete/', views.ContentCategoryDeleteView.as_view(), name='category_delete'),
    path('tags/', views.ContentTagListView.as_view(), name='tag_list'),
    path('tags/create/', views.ContentTagCreateView.as_view(), name='tag_create'),
    path('tags/<uuid:pk>/edit/', views.ContentTagUpdateView.as_view(), name='tag_edit'),
    path('tags/<uuid:pk>/delete/', views.ContentTagDeleteView.as_view(), name='tag_delete'),
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author_create'),
    path('authors/<uuid:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('authors/<uuid:pk>/edit/', views.AuthorUpdateView.as_view(), name='author_edit'),
    path('authors/<uuid:pk>/delete/', views.AuthorDeleteView.as_view(), name='author_delete'),
    path('seo/', views.SEOListView.as_view(), name='seo_list'),
    path('seo/create/', views.SEOCreateView.as_view(), name='seo_create'),
    path('seo/<uuid:pk>/edit/', views.SEOUpdateView.as_view(), name='seo_edit'),
    path('versions/', views.ContentVersionListView.as_view(), name='version_list'),
    path('versions/<uuid:pk>/', views.ContentVersionDetailView.as_view(), name='version_detail'),
    path('schedule/', views.PublishingQueueListView.as_view(), name='publishing_queue'),
    path('schedule/create/', views.PublishingQueueCreateView.as_view(), name='publishing_queue_create'),
    path('schedule/<uuid:pk>/cancel/', views.PublishingQueueCancelView.as_view(), name='publishing_queue_cancel'),
    path('highlights/', views.ContentHighlightListView.as_view(), name='highlight_list'),
    path('highlights/create/', views.ContentHighlightCreateView.as_view(), name='highlight_create'),
    path('highlights/<uuid:pk>/edit/', views.ContentHighlightUpdateView.as_view(), name='highlight_edit'),
    path('highlights/<uuid:pk>/delete/', views.ContentHighlightDeleteView.as_view(), name='highlight_delete'),
    path('search/', views.GlobalSearchView.as_view(), name='search'),
    path('audit-log/', views.ContentAuditLogView.as_view(), name='audit_log'),
]
