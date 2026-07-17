from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from apps.content.models import (
    ContentCategory, ContentTag, Author, SEOModel,
    ContentVersion, PublishingQueue, ContentHighlight
)


class ContentCategoryTest(TestCase):
    def test_create_category(self):
        cat = ContentCategory.objects.create(
            name='Teknologi', slug='teknologi', content_type='ARTICLE'
        )
        self.assertEqual(str(cat), '[Artikel] Teknologi')
        self.assertTrue(cat.active)

    def test_auto_slug(self):
        cat = ContentCategory.objects.create(name='Olahraga', content_type='ARTICLE')
        self.assertEqual(cat.slug, 'olahraga')

    def test_unique_together(self):
        cat1 = ContentCategory.objects.create(name='Tech', slug='tech', content_type='ARTICLE')
        cat2 = ContentCategory(name='Tech', slug='tech-2', content_type='PODCAST')
        cat2.save()
        self.assertNotEqual(cat1.slug, cat2.slug)


class ContentTagTest(TestCase):
    def test_create_tag(self):
        tag = ContentTag.objects.create(name='python', slug='python')
        self.assertEqual(str(tag), 'python')
        self.assertEqual(tag.usage_count, 0)

    def test_auto_slug(self):
        tag = ContentTag.objects.create(name='django-web')
        self.assertEqual(tag.slug, 'django-web')


class AuthorTest(TestCase):
    def test_create_author(self):
        author = Author.objects.create(name='Budi', slug='budi')
        self.assertEqual(str(author), 'Budi')
        self.assertTrue(author.active)

    def test_display_name(self):
        author = Author.objects.create(name='Budi Santoso', slug='budi-santoso')
        self.assertEqual(author.name, 'Budi Santoso')


class SEOModelTest(TestCase):
    def setUp(self):
        self.ct = ContentType.objects.get_for_model(ContentCategory)

    def test_create_seo(self):
        seo = SEOModel.objects.create(
            content_type=self.ct,
            object_id='12345678-1234-5678-1234-567812345678',
            title='Test SEO',
            description='Description for SEO',
        )
        self.assertIn('SEO for', str(seo))

    def test_seo_score_empty(self):
        seo = SEOModel(
            content_type=self.ct,
            object_id='12345678-1234-5678-1234-567812345678',
        )
        self.assertEqual(seo.seo_score, 0)
        self.assertEqual(seo.seo_grade, 'F')

    def test_seo_score_full(self):
        seo = SEOModel(
            content_type=self.ct,
            object_id='12345678-1234-5678-1234-567812345678',
            title='Perfect SEO Title That Is Exactly Right Length',
            description='A' * 140,
            og_title='OG Title',
            og_description='OG Desc',
            og_image='test.jpg',
            keywords='test, seo',
        )
        self.assertEqual(seo.seo_score, 100)
        self.assertEqual(seo.seo_grade, 'A')


class ContentVersionTest(TestCase):
    def test_create_version(self):
        v = ContentVersion.create_version(
            content_type='ARTICLE',
            content_id='12345678-1234-5678-1234-567812345678',
            data={'title': 'Test'},
            summary='Initial'
        )
        self.assertEqual(v.version_number, 1)
        self.assertTrue(v.is_current)

    def test_version_increment(self):
        cid = '12345678-1234-5678-1234-567812345678'
        ContentVersion.create_version('ARTICLE', cid, {'title': 'v1'})
        v2 = ContentVersion.create_version('ARTICLE', cid, {'title': 'v2'})
        self.assertEqual(v2.version_number, 2)

    def test_get_current(self):
        cid = '12345678-1234-5678-1234-567812345678'
        ContentVersion.create_version('ARTICLE', cid, {'title': 'v1'})
        v2 = ContentVersion.create_version('ARTICLE', cid, {'title': 'v2'})
        current = ContentVersion.get_current('ARTICLE', cid)
        self.assertEqual(current.version_number, 2)

    def test_get_history(self):
        cid = '12345678-1234-5678-1234-567812345678'
        for i in range(5):
            ContentVersion.create_version('ARTICLE', cid, {'title': f'v{i}'})
        history = ContentVersion.get_history('ARTICLE', cid, limit=3)
        self.assertEqual(len(history), 3)


class PublishingQueueTest(TestCase):
    def test_create_queue(self):
        from django.utils import timezone
        q = PublishingQueue.objects.create(
            content_type='ARTICLE',
            content_id='12345678-1234-5678-1234-567812345678',
            scheduled_at=timezone.now(),
        )
        self.assertEqual(q.status, 'PENDING')
        self.assertEqual(q.retry_count, 0)


class ContentHighlightTest(TestCase):
    def test_create_highlight(self):
        h = ContentHighlight.objects.create(
            highlight_type='HERO',
            content_type='ARTICLE',
            content_id='12345678-1234-5678-1234-567812345678',
            display_order=1,
        )
        self.assertTrue(h.active)
        self.assertIn('Hero', str(h))

    def test_is_active_now(self):
        from django.utils import timezone
        from datetime import timedelta
        h = ContentHighlight.objects.create(
            highlight_type='FEATURED',
            content_type='ARTICLE',
            content_id='12345678-1234-5678-1234-567812345678',
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1),
        )
        self.assertTrue(h.is_active_now)

    def test_is_not_active_expired(self):
        from django.utils import timezone
        from datetime import timedelta
        h = ContentHighlight.objects.create(
            highlight_type='FEATURED',
            content_type='ARTICLE',
            content_id='12345678-1234-5678-1234-567812345678',
            start_date=timezone.now() - timedelta(days=10),
            end_date=timezone.now() - timedelta(days=1),
        )
        self.assertFalse(h.is_active_now)
