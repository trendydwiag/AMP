from typing import Optional, List
from django.db.models import Q
from utils.repositories import BaseRepository
from .models import Discussion, Reply


class DiscussionRepository(BaseRepository):
    model = Discussion

    def get_recent(self, limit: int = 20):
        return self.model.objects.all().order_by('-created_at')[:limit]

    def get_pinned(self):
        return self.model.objects.filter(is_pinned=True).order_by('-created_at')

    def get_by_category(self, category: str):
        return self.model.objects.filter(category__iexact=category).order_by('-created_at')

    def search(self, query: str):
        return self.model.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author_name__icontains=query) |
            Q(category__icontains=query)
        )

    def get_by_slug(self, slug: str) -> Optional[Discussion]:
        try:
            return self.model.objects.get(slug=slug)
        except self.model.DoesNotExist:
            return None

    def increment_views(self, discussion_id) -> Optional[Discussion]:
        from django.db.models import F
        updated = self.model.objects.filter(pk=discussion_id).update(view_count=F('view_count') + 1)
        if updated:
            return self.model.objects.get(pk=discussion_id)
        return None

    def increment_replies(self, discussion_id) -> Optional[Discussion]:
        from django.db.models import F
        updated = self.model.objects.filter(pk=discussion_id).update(reply_count=F('reply_count') + 1)
        if updated:
            return self.model.objects.get(pk=discussion_id)
        return None


class ReplyRepository(BaseRepository):
    model = Reply

    def get_for_discussion(self, discussion_id):
        return self.model.objects.filter(discussion_id=discussion_id).order_by('created_at')
