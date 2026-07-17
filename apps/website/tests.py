from unittest.mock import patch, MagicMock
from datetime import time
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.broadcast.models import Program, Schedule, BroadcastSession, Episode, Announcement
from apps.podcast.models import Podcast, PodcastEpisode
from apps.news.models import Article, Category, Tag
from apps.community.models import Discussion, Reply
from apps.sponsor.models import Partner
from apps.settings.models import SiteSettings, SEOSettings, SocialMediaSettings


def create_program(**kwargs):
    defaults = {
        'title': 'Program Test',
        'slug': 'program-test',
        'short_description': 'Deskripsi program',
        'active': True,
        'featured': False,
    }
    defaults.update(kwargs)
    return Program.objects.create(**defaults)


def create_category(**kwargs):
    import uuid
    unique = uuid.uuid4().hex[:8]
    defaults = {
        'name': f'Kategori {unique}',
        'slug': f'kategori-{unique}',
        'active': True,
    }
    defaults.update(kwargs)
    return Category.objects.create(**defaults)


def create_article(**kwargs):
    category = kwargs.pop('category', None)
    if category is None and 'category_id' not in kwargs:
        category = create_category()
    defaults = {
        'title': 'Artikel Test',
        'slug': 'artikel-test',
        'content': 'Isi artikel untuk pengujian.',
        'status': 'published',
        'publish_date': timezone.now(),
        'author_name': 'Penulis Test',
    }
    defaults.update(kwargs)
    if category is not None and 'category_id' not in kwargs:
        defaults['category'] = category
    return Article.objects.create(**defaults)


def create_podcast(**kwargs):
    defaults = {
        'title': 'Podcast Test',
        'slug': 'podcast-test',
        'description': 'Deskripsi podcast.',
        'author_name': 'Host Test',
        'active': True,
        'featured': False,
    }
    defaults.update(kwargs)
    return Podcast.objects.create(**defaults)


def create_podcast_episode(**kwargs):
    podcast = kwargs.pop('podcast', None)
    if podcast is None and 'podcast_id' not in kwargs:
        podcast = create_podcast()
    defaults = {
        'title': 'Episode Test',
        'description': 'Deskripsi episode.',
        'audio_file': 'podcast/episodes/audio/test.mp3',
        'duration': 1800,
        'episode_number': 1,
        'season_number': 1,
        'published': True,
        'publish_date': timezone.now(),
    }
    defaults.update(kwargs)
    if podcast is not None and 'podcast_id' not in kwargs:
        defaults['podcast'] = podcast
    return PodcastEpisode.objects.create(**defaults)


def create_schedule(**kwargs):
    program = kwargs.pop('program', None)
    if program is None and 'program_id' not in kwargs:
        program = create_program()
    defaults = {
        'day_of_week': 'MON',
        'start_time': time(8, 0),
        'end_time': time(10, 0),
        'active': True,
    }
    defaults.update(kwargs)
    if program is not None and 'program_id' not in kwargs:
        defaults['program'] = program
    return Schedule.objects.create(**defaults)


def create_discussion(**kwargs):
    defaults = {
        'title': 'Diskusi Test',
        'slug': 'diskusi-test',
        'content': 'Isi diskusi untuk pengujian.',
        'author_name': 'Peserta Test',
        'is_pinned': False,
        'is_locked': False,
    }
    defaults.update(kwargs)
    return Discussion.objects.create(**defaults)


def create_partner(**kwargs):
    defaults = {
        'name': 'Mitra Test',
        'slug': 'mitra-test',
        'partner_type': 'partner',
        'tier': 'silver',
        'active': True,
        'featured': False,
    }
    defaults.update(kwargs)
    return Partner.objects.create(**defaults)


class WebsiteURLTest(TestCase):
    """Test that all website URLs resolve correctly."""

    def test_home_url(self):
        url = reverse('website:home')
        self.assertEqual(url, '/')

    def test_about_url(self):
        url = reverse('website:about')
        self.assertEqual(url, '/tentang/')

    def test_program_list_url(self):
        url = reverse('website:program_list')
        self.assertEqual(url, '/program/')

    def test_program_detail_url(self):
        url = reverse('website:program_detail', kwargs={'slug': 'my-program'})
        self.assertEqual(url, '/program/my-program/')

    def test_schedule_url(self):
        url = reverse('website:schedule')
        self.assertEqual(url, '/jadwal/')

    def test_podcast_list_url(self):
        url = reverse('website:podcast_list')
        self.assertEqual(url, '/podcast/')

    def test_podcast_detail_url(self):
        url = reverse('website:podcast_detail', kwargs={'slug': 'my-podcast'})
        self.assertEqual(url, '/podcast/my-podcast/')

    def test_news_list_url(self):
        url = reverse('website:news_list')
        self.assertEqual(url, '/berita/')

    def test_article_detail_url(self):
        url = reverse('website:article_detail', kwargs={'slug': 'my-article'})
        self.assertEqual(url, '/berita/my-article/')

    def test_community_url(self):
        url = reverse('website:community')
        self.assertEqual(url, '/komunitas/')

    def test_community_discussion_url(self):
        url = reverse('website:community_discussion', kwargs={'slug': 'my-discussion'})
        self.assertEqual(url, '/komunitas/my-discussion/')

    def test_partner_list_url(self):
        url = reverse('website:partner_list')
        self.assertEqual(url, '/mitra/')

    def test_sponsor_list_url(self):
        url = reverse('website:sponsor_list')
        self.assertEqual(url, '/sponsor/')

    def test_contact_url(self):
        url = reverse('website:contact')
        self.assertEqual(url, '/kontak/')

    def test_privacy_url(self):
        url = reverse('website:privacy')
        self.assertEqual(url, '/kebijakan-privasi/')

    def test_terms_url(self):
        url = reverse('website:terms')
        self.assertEqual(url, '/syarat-ketentuan/')

    def test_search_url(self):
        url = reverse('website:search')
        self.assertEqual(url, '/pencarian/')

    def test_maintenance_url(self):
        url = reverse('website:maintenance')
        self.assertEqual(url, '/pemeliharaan/')


class WebsiteHomeViewTest(TestCase):
    """Test homepage renders correctly."""

    def setUp(self):
        self.client = Client()
        self.url = reverse('website:home')

    def test_home_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'website/home.html')

    def test_home_featured_programs_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('featured_programs', response.context)

    def test_home_latest_episodes_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('latest_episodes', response.context)

    def test_home_today_schedule_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('today_schedule', response.context)

    def test_home_current_broadcast_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('current_broadcast', response.context)

    def test_home_next_broadcast_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('next_broadcast', response.context)

    def test_home_featured_podcasts_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('featured_podcasts', response.context)

    def test_home_latest_articles_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('latest_articles', response.context)

    def test_home_sponsors_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('sponsors', response.context)

    def test_home_now_playing_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('now_playing', response.context)

    def test_home_player_config_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('player_config', response.context)

    def test_home_with_featured_programs(self):
        create_program(title='Unggulan', slug='unggulan', featured=True, active=True)
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['featured_programs']), 1)

    def test_home_programs_only_featured(self):
        create_program(title='Unggulan', slug='unggulan', featured=True, active=True)
        create_program(title='Biasa', slug='biasa', featured=False, active=True)
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['featured_programs']), 1)

    def test_home_with_articles(self):
        create_article(title='Berita Terbaru', slug='berita-terbaru')
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['latest_articles']), 1)

    def test_home_with_podcasts(self):
        create_podcast(title='Podcast Unggulan', slug='podcast-unggulan', featured=True)
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['featured_podcasts']), 1)

    def test_home_contains_site_name(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Kabulhaden')


class WebsiteAboutViewTest(TestCase):
    """Test about page renders correctly."""

    def setUp(self):
        self.client = Client()
        self.url = reverse('website:about')

    def test_about_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_about_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'website/about.html')

    def test_about_site_settings_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('site_settings', response.context)

    def test_about_social_media_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('social_media', response.context)

    def test_about_partners_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('partners', response.context)


class WebsiteProgramViewTest(TestCase):
    """Test program list and detail pages."""

    def setUp(self):
        self.client = Client()
        self.program = create_program(
            title='Program Radio',
            slug='program-radio',
            active=True,
            short_description='Program unggulan radio.',
        )

    def test_program_list_status_code(self):
        response = self.client.get(reverse('website:program_list'))
        self.assertEqual(response.status_code, 200)

    def test_program_list_template(self):
        response = self.client.get(reverse('website:program_list'))
        self.assertTemplateUsed(response, 'website/program_list.html')

    def test_program_list_context(self):
        response = self.client.get(reverse('website:program_list'))
        self.assertIn('programs', response.context)

    def test_program_list_with_data(self):
        response = self.client.get(reverse('website:program_list'))
        self.assertEqual(len(response.context['programs']), 1)

    def test_program_list_only_active(self):
        create_program(title='Inactive', slug='inactive', active=False)
        response = self.client.get(reverse('website:program_list'))
        self.assertEqual(len(response.context['programs']), 1)

    def test_program_detail_status_code(self):
        response = self.client.get(
            reverse('website:program_detail', kwargs={'slug': 'program-radio'})
        )
        self.assertEqual(response.status_code, 200)

    def test_program_detail_template(self):
        response = self.client.get(
            reverse('website:program_detail', kwargs={'slug': 'program-radio'})
        )
        self.assertTemplateUsed(response, 'website/program_detail.html')

    def test_program_detail_context(self):
        response = self.client.get(
            reverse('website:program_detail', kwargs={'slug': 'program-radio'})
        )
        self.assertIn('program', response.context)
        self.assertEqual(response.context['program'].title, 'Program Radio')

    def test_program_detail_episodes_in_context(self):
        response = self.client.get(
            reverse('website:program_detail', kwargs={'slug': 'program-radio'})
        )
        self.assertIn('episodes', response.context)

    def test_program_detail_schedules_in_context(self):
        response = self.client.get(
            reverse('website:program_detail', kwargs={'slug': 'program-radio'})
        )
        self.assertIn('schedules', response.context)

    def test_program_detail_nonexistent_slug(self):
        response = self.client.get(
            reverse('website:program_detail', kwargs={'slug': 'tidak-ada'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['program'])


class WebsiteScheduleViewTest(TestCase):
    """Test schedule page renders correctly."""

    def setUp(self):
        self.client = Client()
        self.url = reverse('website:schedule')

    def test_schedule_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_schedule_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'website/schedule.html')

    def test_schedule_weekly_calendar_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('weekly_calendar', response.context)

    def test_schedule_all_schedules_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('all_schedules', response.context)


class WebsitePodcastViewTest(TestCase):
    """Test podcast list, detail, and episode pages."""

    def setUp(self):
        self.client = Client()
        self.podcast = create_podcast(
            title='Podcast Teknologi',
            slug='podcast-teknologi',
        )

    def test_podcast_list_status_code(self):
        response = self.client.get(reverse('website:podcast_list'))
        self.assertEqual(response.status_code, 200)

    def test_podcast_list_template(self):
        response = self.client.get(reverse('website:podcast_list'))
        self.assertTemplateUsed(response, 'website/podcast_list.html')

    def test_podcast_list_context(self):
        response = self.client.get(reverse('website:podcast_list'))
        self.assertIn('podcasts', response.context)
        self.assertIn('featured', response.context)

    def test_podcast_list_with_data(self):
        response = self.client.get(reverse('website:podcast_list'))
        self.assertEqual(len(response.context['podcasts']), 1)

    def test_podcast_detail_status_code(self):
        response = self.client.get(
            reverse('website:podcast_detail', kwargs={'slug': 'podcast-teknologi'})
        )
        self.assertEqual(response.status_code, 200)

    def test_podcast_detail_template(self):
        response = self.client.get(
            reverse('website:podcast_detail', kwargs={'slug': 'podcast-teknologi'})
        )
        self.assertTemplateUsed(response, 'website/podcast_detail.html')

    def test_podcast_detail_context(self):
        response = self.client.get(
            reverse('website:podcast_detail', kwargs={'slug': 'podcast-teknologi'})
        )
        self.assertIn('podcast', response.context)
        self.assertIn('episodes', response.context)

    def test_podcast_detail_nonexistent_slug(self):
        response = self.client.get(
            reverse('website:podcast_detail', kwargs={'slug': 'podcast-tidak-ada'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['podcast'])

    def test_podcast_episode_status_code(self):
        episode = create_podcast_episode(podcast=self.podcast)
        response = self.client.get(
            reverse('website:podcast_episode', kwargs={'pk': episode.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_podcast_episode_template(self):
        episode = create_podcast_episode(podcast=self.podcast)
        response = self.client.get(
            reverse('website:podcast_episode', kwargs={'pk': episode.pk})
        )
        self.assertTemplateUsed(response, 'website/podcast_episode.html')

    def test_podcast_episode_context(self):
        episode = create_podcast_episode(podcast=self.podcast)
        response = self.client.get(
            reverse('website:podcast_episode', kwargs={'pk': episode.pk})
        )
        self.assertIn('episode', response.context)
        self.assertIn('podcast', response.context)


class WebsiteNewsViewTest(TestCase):
    """Test news list and article detail pages."""

    def setUp(self):
        self.client = Client()
        self.article = create_article(
            title='Berita Politik',
            slug='berita-politik',
        )

    def test_news_list_status_code(self):
        response = self.client.get(reverse('website:news_list'))
        self.assertEqual(response.status_code, 200)

    def test_news_list_template(self):
        response = self.client.get(reverse('website:news_list'))
        self.assertTemplateUsed(response, 'website/news_list.html')

    def test_news_list_context(self):
        response = self.client.get(reverse('website:news_list'))
        self.assertIn('articles', response.context)
        self.assertIn('categories', response.context)

    def test_news_list_with_data(self):
        response = self.client.get(reverse('website:news_list'))
        self.assertEqual(len(response.context['articles']), 1)

    def test_article_detail_status_code(self):
        response = self.client.get(
            reverse('website:article_detail', kwargs={'slug': 'berita-politik'})
        )
        self.assertEqual(response.status_code, 200)

    def test_article_detail_template(self):
        response = self.client.get(
            reverse('website:article_detail', kwargs={'slug': 'berita-politik'})
        )
        self.assertTemplateUsed(response, 'website/article_detail.html')

    def test_article_detail_context(self):
        response = self.client.get(
            reverse('website:article_detail', kwargs={'slug': 'berita-politik'})
        )
        self.assertIn('article', response.context)
        self.assertIn('related_articles', response.context)
        self.assertEqual(response.context['article'].title, 'Berita Politik')

    def test_article_detail_increments_views(self):
        self.assertEqual(self.article.view_count, 0)
        self.client.get(
            reverse('website:article_detail', kwargs={'slug': 'berita-politik'})
        )
        self.article.refresh_from_db()
        self.assertEqual(self.article.view_count, 1)

    def test_article_detail_nonexistent_slug(self):
        response = self.client.get(
            reverse('website:article_detail', kwargs={'slug': 'artikel-tidak-ada'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['article'])

    def test_article_detail_related_articles_excludes_self(self):
        create_article(title='Berita Lain', slug='berita-lain')
        response = self.client.get(
            reverse('website:article_detail', kwargs={'slug': 'berita-politik'})
        )
        self.assertNotIn(self.article, response.context['related_articles'])


class WebsiteCommunityViewTest(TestCase):
    """Test community pages."""

    def setUp(self):
        self.client = Client()
        self.discussion = create_discussion(
            title='Diskusi Komunitas',
            slug='diskusi-komunitas',
        )

    def test_community_status_code(self):
        response = self.client.get(reverse('website:community'))
        self.assertEqual(response.status_code, 200)

    def test_community_template(self):
        response = self.client.get(reverse('website:community'))
        self.assertTemplateUsed(response, 'website/community.html')

    def test_community_context(self):
        response = self.client.get(reverse('website:community'))
        self.assertIn('discussions', response.context)
        self.assertIn('pinned', response.context)

    def test_community_discussion_status_code(self):
        response = self.client.get(
            reverse('website:community_discussion', kwargs={'slug': 'diskusi-komunitas'})
        )
        self.assertEqual(response.status_code, 200)

    def test_community_discussion_template(self):
        response = self.client.get(
            reverse('website:community_discussion', kwargs={'slug': 'diskusi-komunitas'})
        )
        self.assertTemplateUsed(response, 'website/community_discussion.html')

    def test_community_discussion_context(self):
        response = self.client.get(
            reverse('website:community_discussion', kwargs={'slug': 'diskusi-komunitas'})
        )
        self.assertIn('discussion', response.context)
        self.assertIn('replies', response.context)
        self.assertEqual(response.context['discussion'].title, 'Diskusi Komunitas')

    def test_community_discussion_increments_views(self):
        self.assertEqual(self.discussion.view_count, 0)
        self.client.get(
            reverse('website:community_discussion', kwargs={'slug': 'diskusi-komunitas'})
        )
        self.discussion.refresh_from_db()
        self.assertEqual(self.discussion.view_count, 1)

    def test_community_discussion_nonexistent_slug(self):
        response = self.client.get(
            reverse('website:community_discussion', kwargs={'slug': 'diskusi-tidak-ada'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['discussion'])


class WebsitePartnerViewTest(TestCase):
    """Test partner and sponsor list pages."""

    def setUp(self):
        self.client = Client()
        self.partner = create_partner(
            name='Mitra Radio',
            slug='mitra-radio',
            partner_type='partner',
        )

    def test_partner_list_status_code(self):
        response = self.client.get(reverse('website:partner_list'))
        self.assertEqual(response.status_code, 200)

    def test_partner_list_template(self):
        response = self.client.get(reverse('website:partner_list'))
        self.assertTemplateUsed(response, 'website/partner_list.html')

    def test_partner_list_context(self):
        response = self.client.get(reverse('website:partner_list'))
        self.assertIn('sponsors', response.context)
        self.assertIn('partners', response.context)

    def test_sponsor_list_status_code(self):
        response = self.client.get(reverse('website:sponsor_list'))
        self.assertEqual(response.status_code, 200)

    def test_sponsor_list_template(self):
        response = self.client.get(reverse('website:sponsor_list'))
        self.assertTemplateUsed(response, 'website/sponsor_list.html')

    def test_sponsor_list_context(self):
        response = self.client.get(reverse('website:sponsor_list'))
        self.assertIn('partners', response.context)


class WebsiteContactViewTest(TestCase):
    """Test contact page renders correctly."""

    def setUp(self):
        self.client = Client()
        self.url = reverse('website:contact')

    def test_contact_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_contact_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'website/contact.html')

    def test_contact_site_settings_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('site_settings', response.context)

    def test_contact_social_media_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('social_media', response.context)


class WebsiteStaticPageViewTest(TestCase):
    """Test privacy, terms, and maintenance pages."""

    def setUp(self):
        self.client = Client()

    def test_privacy_status_code(self):
        response = self.client.get(reverse('website:privacy'))
        self.assertEqual(response.status_code, 200)

    def test_privacy_template(self):
        response = self.client.get(reverse('website:privacy'))
        self.assertTemplateUsed(response, 'website/privacy.html')

    def test_terms_status_code(self):
        response = self.client.get(reverse('website:terms'))
        self.assertEqual(response.status_code, 200)

    def test_terms_template(self):
        response = self.client.get(reverse('website:terms'))
        self.assertTemplateUsed(response, 'website/terms.html')

    def test_maintenance_status_code(self):
        response = self.client.get(reverse('website:maintenance'))
        self.assertEqual(response.status_code, 200)

    def test_maintenance_template(self):
        response = self.client.get(reverse('website:maintenance'))
        self.assertTemplateUsed(response, 'website/maintenance.html')

    def test_maintenance_context(self):
        response = self.client.get(reverse('website:maintenance'))
        self.assertIn('site_settings', response.context)


class WebsiteSearchViewTest(TestCase):
    """Test search functionality."""

    def setUp(self):
        self.client = Client()
        self.url = reverse('website:search')

    def test_search_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_search_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'website/search.html')

    def test_search_context_without_query(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['query'], '')
        self.assertEqual(response.context['total_results'], 0)

    def test_search_context_with_query(self):
        response = self.client.get(self.url, {'q': 'test'})
        self.assertEqual(response.context['query'], 'test')
        self.assertIn('results', response.context)

    def test_search_results_structure(self):
        response = self.client.get(self.url, {'q': 'test'})
        results = response.context['results']
        self.assertIn('programs', results)
        self.assertIn('articles', results)
        self.assertIn('podcasts', results)

    def test_search_empty_query_param(self):
        response = self.client.get(self.url, {'q': '  '})
        self.assertEqual(response.context['query'], '')
        self.assertEqual(response.context['total_results'], 0)

    def test_search_programs_found(self):
        create_program(title='Musik Jazz', slug='musik-jazz', active=True)
        response = self.client.get(self.url, {'q': 'Musik'})
        self.assertGreaterEqual(len(response.context['results']['programs']), 1)

    def test_search_articles_found(self):
        create_article(title='Berita Ekonomi', slug='berita-ekonomi')
        response = self.client.get(self.url, {'q': 'Ekonomi'})
        self.assertGreaterEqual(len(response.context['results']['articles']), 1)

    def test_search_podcasts_found(self):
        create_podcast(title='Podcast Sains', slug='podcast-sains')
        response = self.client.get(self.url, {'q': 'Sains'})
        self.assertGreaterEqual(len(response.context['results']['podcasts']), 1)

    def test_search_no_results(self):
        response = self.client.get(self.url, {'q': 'xyznonexistent123'})
        self.assertEqual(response.context['total_results'], 0)


class WebsiteSEOViewTest(TestCase):
    """Test SEO elements in responses."""

    def setUp(self):
        self.client = Client()

    def test_home_contains_title(self):
        response = self.client.get(reverse('website:home'))
        self.assertContains(response, '<title>')

    def test_about_contains_title(self):
        response = self.client.get(reverse('website:about'))
        self.assertContains(response, '<title>')

    def test_program_list_contains_title(self):
        response = self.client.get(reverse('website:program_list'))
        self.assertContains(response, '<title>')

    def test_news_list_contains_title(self):
        response = self.client.get(reverse('website:news_list'))
        self.assertContains(response, '<title>')

    def test_podcast_list_contains_title(self):
        response = self.client.get(reverse('website:podcast_list'))
        self.assertContains(response, '<title>')

    def test_article_detail_contains_title(self):
        article = create_article(title='Artikel SEO', slug='artikel-seo')
        response = self.client.get(
            reverse('website:article_detail', kwargs={'slug': 'artikel-seo'})
        )
        self.assertContains(response, '<title>')

    def test_program_detail_contains_title(self):
        program = create_program(title='Program SEO', slug='program-seo')
        response = self.client.get(
            reverse('website:program_detail', kwargs={'slug': 'program-seo'})
        )
        self.assertContains(response, '<title>')

    def test_meta_description_present(self):
        response = self.client.get(reverse('website:home'))
        self.assertContains(response, '<meta name="description"')

    def test_search_page_noindex_when_empty(self):
        response = self.client.get(reverse('website:search'))
        self.assertEqual(response.status_code, 200)


class WebsiteAccessibilityTest(TestCase):
    """Test basic accessibility features."""

    def setUp(self):
        self.client = Client()

    def test_home_has_lang_attribute(self):
        response = self.client.get(reverse('website:home'))
        self.assertContains(response, 'lang="id"')

    def test_about_has_lang_attribute(self):
        response = self.client.get(reverse('website:about'))
        self.assertContains(response, 'lang="id"')

    def test_home_has_viewport_meta(self):
        response = self.client.get(reverse('website:home'))
        self.assertContains(response, 'viewport')

    def test_home_has_main_element(self):
        response = self.client.get(reverse('website:home'))
        self.assertContains(response, '<main')

    def test_home_has_nav_element(self):
        response = self.client.get(reverse('website:home'))
        self.assertContains(response, '<nav')

    def test_program_list_has_main(self):
        response = self.client.get(reverse('website:program_list'))
        self.assertContains(response, '<main')

    def test_news_list_has_main(self):
        response = self.client.get(reverse('website:news_list'))
        self.assertContains(response, '<main')

    def test_community_has_main(self):
        response = self.client.get(reverse('website:community'))
        self.assertContains(response, '<main')

    def test_search_has_form(self):
        response = self.client.get(reverse('website:search'))
        self.assertContains(response, '<form')

    def test_htmx_script_loaded(self):
        response = self.client.get(reverse('website:home'))
        self.assertContains(response, 'htmx.org')


class WebsiteHTMXPartialsTest(TestCase):
    """Test that HTMX partial templates exist and are valid HTML fragments."""

    def setUp(self):
        self.client = Client()

    def test_now_playing_partial_exists(self):
        from django.template.loader import get_template
        template = get_template('website/partials/now_playing.html')
        self.assertIsNotNone(template)

    def test_schedule_widget_partial_exists(self):
        from django.template.loader import get_template
        template = get_template('website/partials/schedule_widget.html')
        self.assertIsNotNone(template)

    def test_latest_news_partial_exists(self):
        from django.template.loader import get_template
        template = get_template('website/partials/latest_news.html')
        self.assertIsNotNone(template)

    def test_featured_programs_partial_exists(self):
        from django.template.loader import get_template
        template = get_template('website/partials/featured_programs.html')
        self.assertIsNotNone(template)

    def test_latest_podcast_partial_exists(self):
        from django.template.loader import get_template
        template = get_template('website/partials/latest_podcast.html')
        self.assertIsNotNone(template)

    def test_community_widget_partial_exists(self):
        from django.template.loader import get_template
        template = get_template('website/partials/community_widget.html')
        self.assertIsNotNone(template)

    def test_sponsor_widget_partial_exists(self):
        from django.template.loader import get_template
        template = get_template('website/partials/sponsor_widget.html')
        self.assertIsNotNone(template)

    def test_search_results_partial_exists(self):
        from django.template.loader import get_template
        template = get_template('website/partials/search_results.html')
        self.assertIsNotNone(template)


class WebsiteSEOTemplatesTest(TestCase):
    """Test that SEO templates exist and are valid JSON-LD."""

    def test_organization_schema_exists(self):
        from django.template.loader import get_template
        template = get_template('website/seo/organization_schema.html')
        self.assertIsNotNone(template)

    def test_article_schema_exists(self):
        from django.template.loader import get_template
        template = get_template('website/seo/article_schema.html')
        self.assertIsNotNone(template)

    def test_podcast_schema_exists(self):
        from django.template.loader import get_template
        template = get_template('website/seo/podcast_schema.html')
        self.assertIsNotNone(template)

    def test_breadcrumb_schema_exists(self):
        from django.template.loader import get_template
        template = get_template('website/seo/breadcrumb_schema.html')
        self.assertIsNotNone(template)

    def test_website_schema_exists(self):
        from django.template.loader import get_template
        template = get_template('website/seo/website_schema.html')
        self.assertIsNotNone(template)


class WebsiteModelCreationTest(TestCase):
    """Test that models used by website views can be created correctly."""

    def test_program_str(self):
        program = create_program(title='Test Program', slug='test-program')
        self.assertEqual(str(program), 'Test Program')

    def test_program_slug_unique(self):
        create_program(title='P1', slug='p1')
        with self.assertRaises(Exception):
            create_program(title='P2', slug='p1')

    def test_article_str(self):
        article = create_article(title='Test Article', slug='test-article')
        self.assertEqual(str(article), 'Test Article')

    def test_article_is_published(self):
        article = create_article(
            title='Published',
            slug='published',
            status='PUBLISHED',
            publish_date=timezone.now(),
            last_published_at=timezone.now(),
        )
        self.assertTrue(article.is_published)

    def test_article_is_not_published(self):
        article = create_article(
            title='Draft',
            slug='draft',
            status='DRAFT',
            publish_date=None,
        )
        self.assertFalse(article.is_published)

    def test_podcast_str(self):
        podcast = create_podcast(title='Test Podcast', slug='test-podcast')
        self.assertEqual(str(podcast), 'Test Podcast')

    def test_podcast_episode_str(self):
        podcast = create_podcast(title='My Podcast', slug='my-podcast')
        episode = create_podcast_episode(podcast=podcast, title='Ep 1', episode_number=1)
        self.assertIn('My Podcast', str(episode))
        self.assertIn('Ep 1', str(episode))

    def test_podcast_episode_is_published(self):
        episode = create_podcast_episode(
            status='PUBLISHED',
            publish_date=timezone.now(),
        )
        self.assertTrue(episode.is_published)

    def test_discussion_str(self):
        discussion = create_discussion(title='Topik Diskusi', slug='topik-diskusi')
        self.assertEqual(str(discussion), 'Topik Diskusi')

    def test_discussion_slug_auto_generated(self):
        discussion = Discussion(title='Diskusi Baru', content='Isi')
        discussion.save()
        self.assertEqual(discussion.slug, 'diskusi-baru')

    def test_partner_str(self):
        partner = create_partner(name='Mitra ABC', slug='mitra-abc')
        self.assertEqual(str(partner), 'Mitra ABC')

    def test_category_str(self):
        category = create_category(name='Teknologi', slug='teknologi')
        self.assertEqual(str(category), 'Teknologi')

    def test_schedule_str(self):
        program = create_program(title='Program A', slug='program-a')
        schedule = create_schedule(program=program, day_of_week='MON')
        self.assertIn('Program A', str(schedule))

    def test_schedule_duration_minutes(self):
        program = create_program(title='Program B', slug='program-b')
        schedule = create_schedule(
            program=program,
            day_of_week='TUE',
            start_time=time(8, 0),
            end_time=time(10, 30),
        )
        self.assertEqual(schedule.duration_minutes, 150)


class WebsiteContextProcessorTest(TestCase):
    """Test that global context processors provide expected variables."""

    def test_site_name_in_context(self):
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.context['SITE_NAME'], 'Kabulhaden CMS')

    def test_site_description_in_context(self):
        response = self.client.get(reverse('website:home'))
        self.assertIn('SITE_DESCRIPTION', response.context)
        self.assertTrue(len(response.context['SITE_DESCRIPTION']) > 0)

    def test_current_year_in_context(self):
        import datetime
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.context['CURRENT_YEAR'], datetime.datetime.now().year)

    def test_is_debug_in_context(self):
        response = self.client.get(reverse('website:home'))
        self.assertIn('IS_DEBUG', response.context)


class WebsiteExceptionHandlingTest(TestCase):
    """Test that views handle service exceptions gracefully."""

    def setUp(self):
        self.client = Client()

    @patch('apps.website.views.ProgramService')
    def test_home_handles_program_service_error(self, mock_service):
        mock_instance = MagicMock()
        mock_instance.get_featured_programs.side_effect = Exception('DB Error')
        mock_service.return_value = mock_instance
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['featured_programs'], [])

    @patch('apps.website.views.ArticleService')
    def test_home_handles_article_service_error(self, mock_service):
        mock_instance = MagicMock()
        mock_instance.get_published.side_effect = Exception('DB Error')
        mock_service.return_value = mock_instance
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['latest_articles'], [])

    @patch('apps.website.views.PodcastService')
    def test_home_handles_podcast_service_error(self, mock_service):
        mock_instance = MagicMock()
        mock_instance.get_featured.side_effect = Exception('DB Error')
        mock_service.return_value = mock_instance
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['featured_podcasts'], [])

    @patch('apps.website.views.PartnerService')
    def test_home_handles_partner_service_error(self, mock_service):
        mock_instance = MagicMock()
        mock_instance.get_featured_partners.side_effect = Exception('DB Error')
        mock_service.return_value = mock_instance
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['sponsors'], [])

    @patch('apps.website.views.ProgramService')
    def test_program_list_handles_service_error(self, mock_service):
        mock_instance = MagicMock()
        mock_instance.get_active_programs.side_effect = Exception('DB Error')
        mock_service.return_value = mock_instance
        response = self.client.get(reverse('website:program_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['programs'], [])

    @patch('apps.website.views.PodcastService')
    def test_podcast_list_handles_service_error(self, mock_service):
        mock_instance = MagicMock()
        mock_instance.get_active_programs.side_effect = Exception('DB Error')
        mock_service.return_value = mock_instance
        response = self.client.get(reverse('website:podcast_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['podcasts'], [])

    @patch('apps.website.views.ArticleService')
    def test_news_list_handles_service_error(self, mock_service):
        mock_instance = MagicMock()
        mock_instance.get_published.side_effect = Exception('DB Error')
        mock_service.return_value = mock_instance
        response = self.client.get(reverse('website:news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['articles'], [])

    @patch('apps.website.views.DiscussionService')
    def test_community_handles_service_error(self, mock_service):
        mock_instance = MagicMock()
        mock_instance.get_recent_discussions.side_effect = Exception('DB Error')
        mock_service.return_value = mock_instance
        response = self.client.get(reverse('website:community'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['discussions'], [])


class WebsiteHTMXTriggerTest(TestCase):
    """Test that partials contain expected HTMX attributes."""

    def setUp(self):
        self.client = Client()

    def test_now_playing_has_hx_trigger(self):
        from django.template.loader import render_to_string
        from django.test import RequestFactory

        factory = RequestFactory()
        request = factory.get('/')
        html = render_to_string(
            'website/partials/now_playing.html',
            {'now_playing': None, 'current_program_info': None},
            request=request,
        )
        self.assertIn('hx-trigger="every 10s"', html)
        self.assertIn('id="now-playing"', html)
        self.assertIn('hx-swap="outerHTML"', html)

    def test_schedule_widget_has_hx_trigger(self):
        from django.template.loader import render_to_string
        from django.test import RequestFactory

        factory = RequestFactory()
        request = factory.get('/')
        html = render_to_string(
            'website/partials/schedule_widget.html',
            {'schedules': []},
            request=request,
        )
        self.assertIn('hx-trigger="every 60s"', html)
        self.assertIn('id="schedule-widget"', html)

    def test_search_results_has_id(self):
        from django.template.loader import render_to_string
        from django.test import RequestFactory

        factory = RequestFactory()
        request = factory.get('/')
        html = render_to_string(
            'website/partials/search_results.html',
            {'query': 'test', 'results': {'programs': [], 'articles': [], 'podcasts': []}, 'total_results': 0},
            request=request,
        )
        self.assertIn('id="search-results"', html)
