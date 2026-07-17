from django.test import TestCase
from apps.content.services import (
    ContentCategoryService, ContentTagService, AuthorService,
    SEOService, ContentVersionService, PublishingQueueService,
    ContentHighlightService
)
from apps.content.models import (
    ContentCategory, ContentTag, Author, SEOModel,
    ContentVersion, PublishingQueue, ContentHighlight
)
from django.contrib.contenttypes.models import ContentType


class ContentCategoryServiceTest(TestCase):
    def setUp(self):
        self.service = ContentCategoryService()

    def test_create_category(self):
        cat = self.service.create_category({
            'name': 'Sains', 'slug': 'sains', 'content_type': 'ARTICLE'
        })
        self.assertEqual(cat.name, 'Sains')

    def test_get_active(self):
        self.service.create_category({'name': 'A', 'slug': 'a', 'content_type': 'ARTICLE', 'active': True})
        self.service.create_category({'name': 'B', 'slug': 'b', 'content_type': 'ARTICLE', 'active': False})
        self.assertEqual(self.service.get_active('ARTICLE').count(), 1)

    def test_search(self):
        self.service.create_category({'name': 'Python Tips', 'slug': 'python-tips', 'content_type': 'ARTICLE'})
        self.assertEqual(self.service.search('python').count(), 1)

    def test_toggle_active(self):
        cat = self.service.create_category({'name': 'Test', 'slug': 'test', 'content_type': 'ARTICLE'})
        toggled = self.service.toggle_active(cat.id)
        self.assertFalse(toggled.active)


class ContentTagServiceTest(TestCase):
    def setUp(self):
        self.service = ContentTagService()

    def test_get_or_create(self):
        tag = self.service.get_or_create('Django')
        self.assertEqual(tag.name, 'Django')
        tag2 = self.service.get_or_create('Django')
        self.assertEqual(tag.id, tag2.id)

    def test_bulk_create(self):
        tags = self.service.bulk_create(['Python', 'Django', 'REST'])
        self.assertEqual(len(tags), 3)


class AuthorServiceTest(TestCase):
    def setUp(self):
        self.service = AuthorService()

    def test_create_author(self):
        author = self.service.create_author({'name': 'Andi', 'slug': 'andi'})
        self.assertEqual(author.name, 'Andi')

    def test_search(self):
        self.service.create_author({'name': 'Budi Santoso', 'slug': 'budi'})
        self.assertEqual(self.service.search('Budi').count(), 1)


class ContentVersionServiceTest(TestCase):
    def setUp(self):
        self.service = ContentVersionService()

    def test_create_version(self):
        v = self.service.create_version(
            'ARTICLE', '12345678-1234-5678-1234-567812345678', {'title': 'Test'}
        )
        self.assertEqual(v.version_number, 1)

    def test_rollback(self):
        cid = '12345678-1234-5678-1234-567812345678'
        self.service.create_version('ARTICLE', cid, {'title': 'v1'})
        self.service.create_version('ARTICLE', cid, {'title': 'v2'})
        rolled = self.service.rollback_to('ARTICLE', cid, 1)
        self.assertIsNotNone(rolled)
        self.assertEqual(rolled.data_snapshot['title'], 'v1')


class PublishingQueueServiceTest(TestCase):
    def setUp(self):
        self.service = PublishingQueueService()

    def test_schedule(self):
        from django.utils import timezone
        q = self.service.schedule(
            'ARTICLE', '12345678-1234-5678-1234-567812345678', timezone.now()
        )
        self.assertEqual(q.status, 'PENDING')

    def test_cancel(self):
        from django.utils import timezone
        q = self.service.schedule(
            'ARTICLE', '12345678-1234-5678-1234-567812345678', timezone.now()
        )
        self.service.cancel(q.id)
        q.refresh_from_db()
        self.assertEqual(q.status, 'CANCELLED')


class ContentHighlightServiceTest(TestCase):
    def setUp(self):
        self.service = ContentHighlightService()

    def test_create_highlight(self):
        h = self.service.create_highlight({
            'highlight_type': 'HERO',
            'content_type': 'ARTICLE',
            'content_id': '12345678-1234-5678-1234-567812345678',
            'display_order': 1,
        })
        self.assertTrue(h.active)
