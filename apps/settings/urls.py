from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('', views.SiteSettingsView.as_view(), name='site'),
    path('seo/', views.SEOSettingsView.as_view(), name='seo'),
    path('email/', views.EmailSettingsView.as_view(), name='email'),
    path('keamanan/', views.SecuritySettingsView.as_view(), name='security'),
    path('tampilan/', views.AppearanceSettingsView.as_view(), name='appearance'),
    path('notifikasi/', views.NotificationSettingsView.as_view(), name='notification'),
    path('media-sosial/', views.SocialMediaSettingsView.as_view(), name='social_media'),
    path('konten/', views.ContentSettingsView.as_view(), name='content'),
    path('bahasa/', views.LanguageSettingsView.as_view(), name='language'),
    path('media/', views.MediaSettingsView.as_view(), name='media'),
]
