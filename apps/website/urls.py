from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('tentang/', views.AboutView.as_view(), name='about'),
    path('program/', views.ProgramListView.as_view(), name='program_list'),
    path('program/<slug:slug>/', views.ProgramDetailView.as_view(), name='program_detail'),
    path('jadwal/', views.ScheduleView.as_view(), name='schedule'),
    path('podcast/', views.PodcastListView.as_view(), name='podcast_list'),
    path('podcast/<slug:slug>/', views.PodcastDetailView.as_view(), name='podcast_detail'),
    path('podcast/episode/<uuid:pk>/', views.PodcastEpisodeView.as_view(), name='podcast_episode'),
    path('berita/', views.NewsListView.as_view(), name='news_list'),
    path('berita/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('komunitas/', views.CommunityView.as_view(), name='community'),
    path('komunitas/<slug:slug>/', views.CommunityDiscussionView.as_view(), name='community_discussion'),
    path('mitra/', views.PartnerListView.as_view(), name='partner_list'),
    path('sponsor/', views.SponsorListView.as_view(), name='sponsor_list'),
    path('kontak/', views.ContactView.as_view(), name='contact'),
    path('kebijakan-privasi/', views.PrivacyView.as_view(), name='privacy'),
    path('syarat-ketentuan/', views.TermsView.as_view(), name='terms'),
    path('pencarian/', views.SearchView.as_view(), name='search'),
    path('pemeliharaan/', views.MaintenanceView.as_view(), name='maintenance'),
    path('radio-live/', views.HomeView.as_view(), name='radio_live'),
    path('newsletter/subscribe/', views.NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),
]
