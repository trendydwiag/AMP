import logging
import json
from django.views.generic import TemplateView, View
from django.shortcuts import render
from django.http import JsonResponse

from apps.broadcast.services import (
    ProgramService, HostService, ScheduleService,
    BroadcastService, EpisodeService, CalendarService,
    AnnouncementService,
)
from apps.radio.services import (
    RadioStationService, NowPlayingService, ListenerService,
    PlayerService, BroadcastIntegrationService, MetadataService,
    FallbackService,
)
from apps.settings.models import SiteSettings, SEOSettings, SocialMediaSettings
from apps.podcast.services import PodcastService, PodcastEpisodeService
from apps.news.services import ArticleService, CategoryService, TagService
from apps.sponsor.services import PartnerService, AdvertisementService
from apps.community.services import DiscussionService, ReplyService

logger = logging.getLogger('website')


class HomeView(TemplateView):
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            program_svc = ProgramService()
            context['featured_programs'] = program_svc.get_featured_programs()
        except Exception:
            context['featured_programs'] = []

        try:
            episode_svc = EpisodeService()
            episodes_qs = episode_svc.get_published().select_related('program')[:6]
            context['latest_episodes'] = episodes_qs
        except Exception:
            context['latest_episodes'] = []

        try:
            broadcast_svc = BroadcastService()
            context['today_schedule'] = broadcast_svc.get_today_schedule()
            context['current_broadcast'] = broadcast_svc.get_current_broadcast()
            context['next_broadcast'] = broadcast_svc.get_next_broadcast()
        except Exception:
            context['today_schedule'] = []
            context['current_broadcast'] = None
            context['next_broadcast'] = None

        try:
            podcast_svc = PodcastService()
            context['featured_podcasts'] = podcast_svc.get_featured()[:4]
        except Exception:
            context['featured_podcasts'] = []

        try:
            article_svc = ArticleService()
            articles_qs = article_svc.get_published().select_related('category')[:6]
            context['latest_articles'] = articles_qs
        except Exception:
            context['latest_articles'] = []

        try:
            announcement_svc = AnnouncementService()
            context['current_announcements'] = announcement_svc.get_current_announcements()
        except Exception:
            context['current_announcements'] = []

        try:
            partner_svc = PartnerService()
            context['sponsors'] = partner_svc.get_featured_partners()
        except Exception:
            context['sponsors'] = []

        try:
            station_svc = RadioStationService()
            primary_station = station_svc.get_primary_station()
            station_id = primary_station.pk if primary_station else None

            if station_id:
                integration_svc = BroadcastIntegrationService()
                context['current_program_info'] = integration_svc.get_current_program(station_id)

                np_svc = NowPlayingService()
                context['now_playing'] = np_svc.get_now_playing(station_id)
            else:
                context['current_program_info'] = {'program': '', 'host': '', 'started_at': None, 'duration': ''}
                context['now_playing'] = None
        except Exception:
            context['current_program_info'] = {'program': '', 'host': '', 'started_at': None, 'duration': ''}
            context['now_playing'] = None

        try:
            player_svc = PlayerService()
            context['player_config'] = player_svc.get_player_config()
        except Exception:
            context['player_config'] = {}

        try:
            context['site_settings'] = SiteSettings.load()
        except Exception:
            context['site_settings'] = None

        return context


class AboutView(TemplateView):
    template_name = 'website/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            context['site_settings'] = SiteSettings.load()
        except Exception:
            context['site_settings'] = None

        try:
            context['social_media'] = SocialMediaSettings.load()
        except Exception:
            context['social_media'] = None

        try:
            partner_svc = PartnerService()
            context['partners'] = partner_svc.get_active_partners()
        except Exception:
            context['partners'] = []

        return context


class ProgramListView(TemplateView):
    template_name = 'website/program_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            program_svc = ProgramService()
            context['programs'] = program_svc.get_active_programs().select_related()
        except Exception:
            context['programs'] = []

        return context


class ProgramDetailView(TemplateView):
    template_name = 'website/program_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')

        try:
            program_svc = ProgramService()
            context['program'] = program_svc.get_by_slug(slug)
        except Exception:
            context['program'] = None

        if context.get('program'):
            program = context['program']
            try:
                episode_svc = EpisodeService()
                context['episodes'] = episode_svc.get_for_program(program.pk).select_related('program')
            except Exception:
                context['episodes'] = []

            try:
                schedule_svc = ScheduleService()
                context['schedules'] = schedule_svc.get_for_program(program.pk)
            except Exception:
                context['schedules'] = []
        else:
            context['episodes'] = []
            context['schedules'] = []

        return context


class ScheduleView(TemplateView):
    template_name = 'website/schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            calendar_svc = CalendarService()
            context['weekly_calendar'] = calendar_svc.get_weekly_calendar()
        except Exception:
            context['weekly_calendar'] = {}

        try:
            schedule_svc = ScheduleService()
            context['all_schedules'] = schedule_svc.get_active_schedules().select_related('program')
        except Exception:
            context['all_schedules'] = []

        return context


class PodcastListView(TemplateView):
    template_name = 'website/podcast_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            podcast_svc = PodcastService()
            context['podcasts'] = podcast_svc.get_active_programs()
        except Exception:
            context['podcasts'] = []

        try:
            podcast_svc = PodcastService()
            context['featured'] = podcast_svc.get_featured()
        except Exception:
            context['featured'] = []

        return context


class PodcastDetailView(TemplateView):
    template_name = 'website/podcast_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')

        try:
            podcast_svc = PodcastService()
            context['podcast'] = podcast_svc.get_by_slug(slug)
        except Exception:
            context['podcast'] = None

        if context.get('podcast'):
            podcast = context['podcast']
            try:
                episode_svc = PodcastEpisodeService()
                context['episodes'] = episode_svc.get_for_podcast(podcast.pk).select_related('podcast')
            except Exception:
                context['episodes'] = []
        else:
            context['episodes'] = []

        return context


class PodcastEpisodeView(TemplateView):
    template_name = 'website/podcast_episode.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        episode_pk = self.kwargs.get('pk')

        try:
            episode_svc = PodcastEpisodeService()
            episode = episode_svc.repository.get_by_id(episode_pk)
            context['episode'] = episode
            if episode:
                context['podcast'] = episode.podcast
            else:
                context['podcast'] = None
        except Exception:
            context['episode'] = None
            context['podcast'] = None

        return context


class NewsListView(TemplateView):
    template_name = 'website/news_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            article_svc = ArticleService()
            context['articles'] = article_svc.get_published().select_related('category')
        except Exception:
            context['articles'] = []

        try:
            category_svc = CategoryService()
            context['categories'] = category_svc.get_active()
        except Exception:
            context['categories'] = []

        return context


class ArticleDetailView(TemplateView):
    template_name = 'website/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')

        try:
            article_svc = ArticleService()
            context['article'] = article_svc.repository.get_by_slug(slug)
        except Exception:
            context['article'] = None

        if context.get('article'):
            article = context['article']
            try:
                article_svc = ArticleService()
                context['related_articles'] = (
                    article_svc.get_published()
                    .select_related('category')
                    .exclude(pk=article.pk)[:3]
                )
            except Exception:
                context['related_articles'] = []

            try:
                article_svc = ArticleService()
                article_svc.increment_views(article.pk)
            except Exception:
                pass
        else:
            context['related_articles'] = []

        return context


class CommunityView(TemplateView):
    template_name = 'website/community.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            discussion_svc = DiscussionService()
            context['discussions'] = discussion_svc.get_recent_discussions()
        except Exception:
            context['discussions'] = []

        try:
            discussion_svc = DiscussionService()
            context['pinned'] = discussion_svc.get_pinned_discussions()
        except Exception:
            context['pinned'] = []

        return context


class CommunityDiscussionView(TemplateView):
    template_name = 'website/community_discussion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')

        try:
            discussion_svc = DiscussionService()
            context['discussion'] = discussion_svc.get_by_slug(slug)
        except Exception:
            context['discussion'] = None

        if context.get('discussion'):
            discussion = context['discussion']
            try:
                reply_svc = ReplyService()
                context['replies'] = reply_svc.get_for_discussion(discussion.pk)
            except Exception:
                context['replies'] = []

            try:
                discussion_svc = DiscussionService()
                discussion_svc.increment_views(discussion.pk)
            except Exception:
                pass
        else:
            context['replies'] = []

        return context


class PartnerListView(TemplateView):
    template_name = 'website/partner_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            partner_svc = PartnerService()
            context['sponsors'] = partner_svc.get_active_partners()
        except Exception:
            context['sponsors'] = []

        try:
            partner_svc = PartnerService()
            context['partners'] = partner_svc.get_by_type('partner')
        except Exception:
            context['partners'] = []

        return context


class SponsorListView(TemplateView):
    template_name = 'website/sponsor_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            partner_svc = PartnerService()
            context['partners'] = partner_svc.get_active_partners()
        except Exception:
            context['partners'] = []

        return context


class ContactView(TemplateView):
    template_name = 'website/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            context['site_settings'] = SiteSettings.load()
        except Exception:
            context['site_settings'] = None

        try:
            context['social_media'] = SocialMediaSettings.load()
        except Exception:
            context['social_media'] = None

        return context


class PrivacyView(TemplateView):
    template_name = 'website/privacy.html'


class TermsView(TemplateView):
    template_name = 'website/terms.html'


class MaintenanceView(TemplateView):
    template_name = 'website/maintenance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            context['site_settings'] = SiteSettings.load()
        except Exception:
            context['site_settings'] = None

        return context


class SearchView(View):
    template_name = 'website/search.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        results = {
            'programs': [],
            'articles': [],
            'podcasts': [],
        }

        if query:
            try:
                program_svc = ProgramService()
                results['programs'] = program_svc.search_programs(query)
            except Exception:
                pass

            try:
                article_svc = ArticleService()
                results['articles'] = article_svc.search_articles(query)
            except Exception:
                pass

            try:
                podcast_svc = PodcastService()
                results['podcasts'] = podcast_svc.search_podcasts(query)
            except Exception:
                pass

        context = {
            'query': query,
            'results': results,
            'total_results': (
                len(results['programs'])
                + len(results['articles'])
                + len(results['podcasts'])
            ),
        }

        return render(request, self.template_name, context)


class Website404View(TemplateView):
    template_name = 'website/404.html'
    status_code = 404

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['status'] = self.status_code
        return super().render_to_response(context, **response_kwargs)


class Website500View(TemplateView):
    template_name = 'website/500.html'
    status_code = 500

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['status'] = self.status_code
        return super().render_to_response(context, **response_kwargs)


class NewsletterSubscribeView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip()
            if not email:
                return JsonResponse({'success': False, 'message': 'Email harus diisi.'})
            return JsonResponse({'success': True, 'message': 'Terima kasih! Anda telah berlangganan.'})
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'success': False, 'message': 'Data tidak valid.'})
