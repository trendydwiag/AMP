from typing import Optional, Dict, Any, List
from django.db.models import F
from django.db import transaction
from django.utils.text import slugify
from utils.services import BaseService
from .repos import (
    ContentCategoryRepository, ContentTagRepository, AuthorRepository,
    SEORepository, ContentVersionRepository, PublishingQueueRepository,
    ContentHighlightRepository
)
from .models import ContentVersion


class ContentCategoryService(BaseService[ContentCategoryRepository]):
    def __init__(self):
        super().__init__(ContentCategoryRepository())

    def get_active(self, content_type=None):
        return self.repository.get_active(content_type)

    def get_roots(self, content_type=None):
        return self.repository.get_roots(content_type)

    def get_children(self, parent_id):
        return self.repository.get_children(parent_id)

    def search(self, query, content_type=None):
        return self.repository.search(query, content_type)

    @transaction.atomic
    def create_category(self, data: Dict[str, Any]):
        return self.repository.create(**data)

    @transaction.atomic
    def update_category(self, category_id, data: Dict[str, Any]):
        cat = self.repository.get_by_id(category_id)
        if cat:
            return self.repository.update(cat, **data)
        return None

    def toggle_active(self, category_id):
        cat = self.repository.get_by_id(category_id)
        if cat:
            cat.active = not cat.active
            cat.save(update_fields=['active'])
        return cat

    def reorder(self, category_ids: List):
        for idx, cat_id in enumerate(category_ids):
            cat = self.repository.get_by_id(cat_id)
            if cat:
                self.repository.update(cat, display_order=idx)


class ContentTagService(BaseService[ContentTagRepository]):
    def __init__(self):
        super().__init__(ContentTagRepository())

    def get_popular(self, limit=20):
        return self.repository.get_popular(limit)

    def search(self, query):
        return self.repository.search(query)

    def get_or_create(self, name):
        return self.repository.get_or_create_by_name(name)

    def bulk_create(self, names: List[str]):
        tags = []
        for name in names:
            tag, _ = self.repository.model.objects.get_or_create(
                name=name.strip(),
                defaults={'slug': slugify(name.strip())}
            )
            tags.append(tag)
        return tags

    def increment_usage(self, tag_id):
        self.repository.model.objects.filter(id=tag_id).update(usage_count=F('usage_count') + 1)


class AuthorService(BaseService[AuthorRepository]):
    def __init__(self):
        super().__init__(AuthorRepository())

    def get_active(self):
        return self.repository.get_active()

    def get_by_user(self, user_id):
        return self.repository.get_by_user(user_id)

    def search(self, query):
        return self.repository.search(query)

    @transaction.atomic
    def create_author(self, data: Dict[str, Any]):
        return self.repository.create(**data)

    @transaction.atomic
    def update_author(self, author_id, data: Dict[str, Any]):
        author = self.repository.get_by_id(author_id)
        if author:
            return self.repository.update(author, **data)
        return None


class SEOService(BaseService[SEORepository]):
    def __init__(self):
        super().__init__(SEORepository())

    def get_for_content(self, content_type_label: str, object_id):
        from django.contrib.contenttypes.models import ContentType
        if '.' in content_type_label:
            parts = content_type_label.split('.')
            ct = ContentType.objects.get(app_label=parts[0], model=parts[1])
            return self.repository.get_for_content(ct.id, object_id)
        return None

    def get_or_create(self, content_type_label: str, object_id, data: Dict[str, Any]):
        from django.contrib.contenttypes.models import ContentType
        parts = content_type_label.split('.')
        if len(parts) == 2:
            app_label, model_name = parts
            ct = ContentType.objects.get(app_label=app_label, model=model_name)
        else:
            return None

        seo, created = self.repository.model.objects.get_or_create(
            content_type=ct,
            object_id=object_id,
            defaults=data
        )
        if not created:
            for key, value in data.items():
                if hasattr(seo, key):
                    setattr(seo, key, value)
            seo.save()
        return seo

    def get_low_score(self, threshold=50):
        return self.repository.get_low_score(threshold)

    def calculate_score(self, content_type_label, object_id):
        seo = self.get_for_content(content_type_label, object_id)
        return seo.seo_score if seo else 0


class ContentVersionService(BaseService[ContentVersionRepository]):
    def __init__(self):
        super().__init__(ContentVersionRepository())

    def create_version(self, content_type: str, content_id, data: Dict[str, Any], author=None, summary=''):
        return ContentVersion.create_version(
            content_type=content_type,
            content_id=content_id,
            data=data,
            author=author,
            summary=summary,
        )

    def get_current(self, content_type, content_id):
        return self.repository.get_current(content_type, content_id)

    def get_history(self, content_type, content_id, limit=20):
        return self.repository.get_history(content_type, content_id, limit)

    def get_by_version(self, content_type, content_id, version_number):
        return self.repository.get_by_version(content_type, content_id, version_number)

    def rollback_to(self, content_type, content_id, version_number, author=None):
        version = self.get_by_version(content_type, content_id, version_number)
        if not version:
            return None
        return self.create_version(
            content_type=content_type,
            content_id=content_id,
            data=version.data_snapshot,
            author=author,
            summary=f"Rollback to v{version_number}",
        )


class PublishingQueueService(BaseService[PublishingQueueRepository]):
    def __init__(self):
        super().__init__(PublishingQueueRepository())

    def schedule(self, content_type, content_id, scheduled_at, user=None):
        return self.repository.create(
            content_type=content_type,
            content_id=content_id,
            scheduled_at=scheduled_at,
            status='PENDING',
            created_by=user,
        )

    def get_due(self):
        return self.repository.get_due()

    def get_pending(self):
        return self.repository.get_pending()

    def mark_published(self, queue_id):
        from django.utils import timezone
        queue = self.repository.get_by_id(queue_id)
        if queue:
            return self.repository.update(queue, status='PUBLISHED', published_at=timezone.now())
        return None

    def mark_failed(self, queue_id, error_message):
        queue = self.repository.get_by_id(queue_id)
        if queue:
            return self.repository.update(queue, status='FAILED', error_message=error_message)
        return None

    def cancel(self, queue_id):
        queue = self.repository.get_by_id(queue_id)
        if queue:
            return self.repository.update(queue, status='CANCELLED')
        return None

    def retry(self, queue_id):
        queue = self.repository.get_by_id(queue_id)
        if queue:
            self.repository.model.objects.filter(id=queue_id).update(retry_count=F('retry_count') + 1)
            return self.repository.update(queue, status='PENDING', error_message='')
        return None


class ContentHighlightService(BaseService[ContentHighlightRepository]):
    def __init__(self):
        super().__init__(ContentHighlightRepository())

    def get_active(self, highlight_type=None):
        return self.repository.get_active_highlights(highlight_type)

    def get_for_homepage(self):
        return self.repository.get_for_homepage()

    @transaction.atomic
    def create_highlight(self, data: Dict[str, Any]):
        return self.repository.create(**data)

    @transaction.atomic
    def update_highlight(self, highlight_id, data: Dict[str, Any]):
        h = self.repository.get_by_id(highlight_id)
        if h:
            return self.repository.update(h, **data)
        return None

    def toggle_active(self, highlight_id):
        h = self.repository.get_by_id(highlight_id)
        if h:
            h.active = not h.active
            h.save(update_fields=['active'])
        return h
