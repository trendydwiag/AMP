from django.urls import path
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
]
