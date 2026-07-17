from typing import Optional, List
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from utils.repositories import BaseRepository
from .models import (
    ContentCategory, ContentTag, Author, SEOModel,
    ContentVersion, PublishingQueue, ContentHighlight
)


class ContentCategoryRepository(BaseRepository):
    model = ContentCategory

    def get_active(self, content_type=None):
        qs = self.model.objects.filter(active=True)
        if content_type:
            qs = qs.filter(content_type=content_type)
        return qs.order_by('display_order', 'name')

    def get_roots(self, content_type=None):
        qs = self.model.objects.filter(parent=None, active=True)
        if content_type:
            qs = qs.filter(content_type=content_type)
        return qs.order_by('display_order', 'name')

    def get_children(self, parent_id):
        return self.model.objects.filter(parent_id=parent_id, active=True).order_by('display_order', 'name')

    def search(self, query, content_type=None):
        qs = self.model.objects.filter(
            models.Q(name__icontains=query) | models.Q(description__icontains=query)
        )
        if content_type:
            qs = qs.filter(content_type=content_type)
        return qs.order_by('display_order', 'name')


class ContentTagRepository(BaseRepository):
    model = ContentTag

    def get_popular(self, limit=20):
        return self.model.objects.order_by('-usage_count')[:limit]

    def search(self, query):
        return self.model.objects.filter(
            models.Q(name__icontains=query)
        ).order_by('-usage_count', 'name')

    def get_or_create_by_name(self, name):
        tag, _ = self.model.objects.get_or_create(
            name=name,
            defaults={'slug': slugify(name)}
        )
        return tag


class AuthorRepository(BaseRepository):
    model = Author

    def get_active(self):
        return self.model.objects.filter(active=True).order_by('name')

    def get_by_user(self, user_id):
        return self.model.objects.filter(user_id=user_id).first()

    def search(self, query):
        return self.model.objects.filter(
            models.Q(name__icontains=query) | models.Q(email__icontains=query)
        ).order_by('name')


class SEORepository(BaseRepository):
    model = SEOModel

    def get_for_content(self, content_type_id, object_id):
        return self.model.objects.filter(
            content_type_id=content_type_id,
            object_id=object_id,
        ).first()

    def get_low_score(self, threshold=50):
        all_seo = self.model.objects.all()
        return [s for s in all_seo if s.seo_score < threshold]


class ContentVersionRepository(BaseRepository):
    model = ContentVersion

    def get_current(self, content_type, content_id):
        return self.model.objects.filter(
            content_type=content_type,
            content_id=content_id,
            is_current=True,
        ).first()

    def get_history(self, content_type, content_id, limit=20):
        return self.model.objects.filter(
            content_type=content_type,
            content_id=content_id,
        ).order_by('-version_number')[:limit]

    def get_by_version(self, content_type, content_id, version_number):
        return self.model.objects.filter(
            content_type=content_type,
            content_id=content_id,
            version_number=version_number,
        ).first()


class PublishingQueueRepository(BaseRepository):
    model = PublishingQueue

    def get_pending(self):
        return self.model.objects.filter(status='PENDING').order_by('scheduled_at')

    def get_due(self):
        return self.model.objects.filter(
            status='PENDING',
            scheduled_at__lte=timezone.now(),
        ).order_by('scheduled_at')

    def get_by_content(self, content_type, content_id):
        return self.model.objects.filter(
            content_type=content_type,
            content_id=content_id,
        ).order_by('-scheduled_at')


class ContentHighlightRepository(BaseRepository):
    model = ContentHighlight

    def get_active_highlights(self, highlight_type=None):
        now = timezone.now()
        qs = self.model.objects.filter(
            active=True,
        ).filter(
            models.Q(start_date__isnull=True) | models.Q(start_date__lte=now)
        ).filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=now)
        )
        if highlight_type:
            qs = qs.filter(highlight_type=highlight_type)
        return qs.order_by('display_order')

    def get_for_homepage(self):
        return self.get_active_highlights().filter(
            highlight_type__in=['HERO', 'FEATURED', 'TRENDING', 'EDITORS_PICK']
        )
