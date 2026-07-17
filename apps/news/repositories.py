from typing import Optional, List
from django.db.models import Q, F
from django.utils import timezone
from utils.repositories import BaseRepository
from .models import Category, Tag, Article


class CategoryRepository(BaseRepository):
    model = Category

    def get_active(self):
        return self.model.objects.filter(active=True)

    def get_by_slug(self, slug: str) -> Optional[Category]:
        try:
            return self.model.objects.get(slug=slug)
        except self.model.DoesNotExist:
            return None


class TagRepository(BaseRepository):
    model = Tag

    def get_by_slug(self, slug: str) -> Optional[Tag]:
        try:
            return self.model.objects.get(slug=slug)
        except self.model.DoesNotExist:
            return None


class ArticleRepository(BaseRepository):
    model = Article

    def get_published(self):
        now = timezone.now()
        return self.model.objects.filter(
            status='published',
            publish_date__lte=now
        ).select_related('category')

    def get_by_slug(self, slug: str):
        try:
            return self.model.objects.select_related('category').get(slug=slug)
        except self.model.DoesNotExist:
            return None

    def get_by_category(self, category_slug: str):
        now = timezone.now()
        return self.model.objects.filter(
            status='published',
            publish_date__lte=now,
            category__slug=category_slug
        ).select_related('category')

    def get_by_tag(self, tag_slug: str):
        now = timezone.now()
        return self.model.objects.filter(
            status='published',
            publish_date__lte=now,
            tags__slug=tag_slug
        ).select_related('category').distinct()

    def get_latest(self, limit: int = 10):
        now = timezone.now()
        return self.model.objects.filter(
            status='published',
            publish_date__lte=now
        ).select_related('category')[:limit]

    def search(self, query: str):
        now = timezone.now()
        return self.model.objects.filter(
            status='published',
            publish_date__lte=now
        ).filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query) |
            Q(author_name__icontains=query)
        ).select_related('category')

    def increment_views(self, article_id):
        self.model.objects.filter(pk=article_id).update(view_count=F('view_count') + 1)
