from django.urls import path
from apps.core.views import HomeView, health_check, OfflineView

app_name = 'core'

urlpatterns = [
    # Homepage view
    path('', HomeView.as_view(), name='home'),
    
    # Offline page
    path('offline/', OfflineView.as_view(), name='offline'),
    
    # System health check
    path('health/', health_check, name='health_check'),
]
