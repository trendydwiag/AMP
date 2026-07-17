from django.urls import path
from . import views

app_name = 'platform'

urlpatterns = [
    path('', views.PlatformDashboardView.as_view(), name='dashboard'),
    path('partners/', views.PartnerListView.as_view(), name='partner_list'),
    path('partners/create/', views.PartnerCreateView.as_view(), name='partner_create'),
    path('partners/<uuid:pk>/', views.PartnerDetailView.as_view(), name='partner_detail'),
    path('partners/<uuid:pk>/edit/', views.PartnerUpdateView.as_view(), name='partner_edit'),
    path('providers/', views.ProviderListView.as_view(), name='provider_list'),
    path('features/', views.FeatureFlagListView.as_view(), name='feature_list'),
    path('themes/', views.ThemeListView.as_view(), name='theme_list'),
    path('themes/<uuid:partner_pk>/edit/', views.ThemeEditView.as_view(), name='theme_edit'),
]
