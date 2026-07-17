from typing import Optional, List
from django.db.models import Q
from utils.repositories import BaseRepository
from .models import Podcast, PodcastEpisode


class PodcastRepository(BaseRepository):
    model = Podcast

    def get_active(self):
        return self.model.objects.filter(active=True)

    def get_featured(self):
        return self.model.objects.filter(active=True, featured=True)

    def get_by_slug(self, slug: str) -> Optional[Podcast]:
        try:
            return self.model.objects.get(slug=slug)
        except self.model.DoesNotExist:
            return None

    def search(self, query: str):
        return self.model.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(author_name__icontains=query)
        )


class PodcastEpisodeRepository(BaseRepository):
    model = PodcastEpisode

    def get_published(self):
        from django.utils import timezone
        now = timezone.now()
        return self.model.objects.filter(
            published=True,
            publish_date__lte=now
        ).select_related('podcast')

    def get_for_podcast(self, podcast_id):
        return self.model.objects.filter(podcast_id=podcast_id)

    def get_latest(self, limit: int = 10):
        from django.utils import timezone
        now = timezone.now()
        return self.model.objects.filter(
            published=True,
            publish_date__lte=now
        ).select_related('podcast')[:limit]
