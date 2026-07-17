from django.test import TestCase, Client, override_settings
from django.urls import reverse
from apps.users.models import User
from apps.content.models import (
    ContentCategory, ContentTag, Author, SEOModel,
    ContentVersion, PublishingQueue, ContentHighlight
)
from django.contrib.contenttypes.models import ContentType


class ContentViewTestMixin:
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testadmin',
            email='admin@test.com',
            password='TestPass123!@#',
            is_staff=True,
            is_superuser=True,
        )
        self.client.login(username='testadmin', password='TestPass123!@#')


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class ContentDashboardTest(ContentViewTestMixin, TestCase):
    def test_dashboard_loads(self):
        response = self.client.get(reverse('content:dashboard'))
        self.assertEqual(response.status_code, 200)


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class ContentCategoryViewTest(ContentViewTestMixin, TestCase):
    def test_category_list(self):
        response = self.client.get(reverse('content:category_list'))
        self.assertEqual(response.status_code, 200)

    def test_category_create(self):
        response = self.client.post(reverse('content:category_create'), {
            'name': 'Test Category',
            'slug': 'test-category',
            'content_type': 'ARTICLE',
            'display_order': 0,
        })
        self.assertEqual(response.status_code, 302)

    def test_category_list_search(self):
        ContentCategory.objects.create(name='Tech', slug='tech', content_type='ARTICLE')
        response = self.client.get(reverse('content:category_list') + '?q=tech')
        self.assertEqual(response.status_code, 200)


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class ContentTagViewTest(ContentViewTestMixin, TestCase):
    def test_tag_list(self):
        response = self.client.get(reverse('content:tag_list'))
        self.assertEqual(response.status_code, 200)

    def test_tag_create(self):
        response = self.client.post(reverse('content:tag_create'), {
            'name': 'Test Tag',
            'slug': 'test-tag',
            'color': '#6B4226',
        })
        self.assertEqual(response.status_code, 302)


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class AuthorViewTest(ContentViewTestMixin, TestCase):
    def test_author_list(self):
        response = self.client.get(reverse('content:author_list'))
        self.assertEqual(response.status_code, 200)

    def test_author_create(self):
        response = self.client.post(reverse('content:author_create'), {
            'name': 'Test Author',
            'slug': 'test-author',
        })
        self.assertEqual(response.status_code, 302)


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class SEOViewTest(ContentViewTestMixin, TestCase):
    def test_seo_list(self):
        response = self.client.get(reverse('content:seo_list'))
        self.assertEqual(response.status_code, 200)


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class VersionViewTest(ContentViewTestMixin, TestCase):
    def test_version_list(self):
        response = self.client.get(reverse('content:version_list'))
        self.assertEqual(response.status_code, 200)


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class PublishingQueueViewTest(ContentViewTestMixin, TestCase):
    def test_queue_list(self):
        response = self.client.get(reverse('content:publishing_queue'))
        self.assertEqual(response.status_code, 200)


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class HighlightViewTest(ContentViewTestMixin, TestCase):
    def test_highlight_list(self):
        response = self.client.get(reverse('content:highlight_list'))
        self.assertEqual(response.status_code, 200)


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class GlobalSearchViewTest(ContentViewTestMixin, TestCase):
    def test_search_empty(self):
        response = self.client.get(reverse('content:search'))
        self.assertEqual(response.status_code, 200)

    def test_search_with_query(self):
        response = self.client.get(reverse('content:search') + '?q=test')
        self.assertEqual(response.status_code, 200)
