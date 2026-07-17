import logging
from typing import Optional, List
from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from utils.services import BaseService
from .repositories import CategoryRepository, TagRepository, ArticleRepository
from .models import Category, Tag, Article

logger = logging.getLogger('news')


class CategoryService(BaseService[CategoryRepository]):
    def __init__(self):
        super().__init__(CategoryRepository())

    def get_active(self):
        return self.repository.get_active()

    def get_by_slug(self, slug: str) -> Optional[Category]:
        return self.repository.get_by_slug(slug)

    @transaction.atomic
    def create_category(self, **kwargs) -> Category:
        return self.repository.create(**kwargs)

    @transaction.atomic
    def update_category(self, category_id, **kwargs) -> Optional[Category]:
        category = self.repository.get_by_id(category_id)
        if category:
            return self.repository.update(category, **kwargs)
        return None


class TagService(BaseService[TagRepository]):
    def __init__(self):
        super().__init__(TagRepository())

    def get_all(self):
        return self.repository.list_all()

    def get_by_slug(self, slug: str) -> Optional[Tag]:
        return self.repository.get_by_slug(slug)

    @transaction.atomic
    def create_tag(self, **kwargs) -> Tag:
        return self.repository.create(**kwargs)


class ArticleService(BaseService[ArticleRepository]):
    def __init__(self):
        super().__init__(ArticleRepository())

    def get_published(self):
        return self.repository.get_published()

    def get_by_category(self, category_slug: str):
        return self.repository.get_by_category(category_slug)

    def get_by_tag(self, tag_slug: str):
        return self.repository.get_by_tag(tag_slug)

    def get_latest(self, limit: int = 10):
        return self.repository.get_latest(limit)

    @transaction.atomic
    def create_article(self, **kwargs) -> Article:
        return self.repository.create(**kwargs)

    @transaction.atomic
    def update_article(self, article_id, **kwargs) -> Optional[Article]:
        article = self.repository.get_by_id(article_id)
        if article:
            return self.repository.update(article, **kwargs)
        return None

    @transaction.atomic
    def publish(self, article_id) -> Optional[Article]:
        article = self.repository.get_by_id(article_id)
        if article:
            article.status = 'published'
            if not article.publish_date:
                article.publish_date = timezone.now()
            article.save(update_fields=['status', 'publish_date'])
            return article
        return None

    @transaction.atomic
    def unpublish(self, article_id) -> Optional[Article]:
        article = self.repository.get_by_id(article_id)
        if article:
            article.status = 'draft'
            article.save(update_fields=['status'])
            return article
        return None

    def increment_views(self, article_id):
        self.repository.increment_views(article_id)

    def search_articles(self, query: str):
        return self.repository.search(query)
