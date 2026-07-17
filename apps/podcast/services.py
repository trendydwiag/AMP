import logging
from typing import Optional
from django.utils import timezone
from django.db import transaction
from django.db.models import F
from utils.services import BaseService
from .repositories import PodcastRepository, PodcastEpisodeRepository
from .models import Podcast, PodcastEpisode

logger = logging.getLogger('podcast')


class PodcastService(BaseService[PodcastRepository]):
    def __init__(self):
        super().__init__(PodcastRepository())

    def get_active_programs(self):
        return self.repository.get_active()

    def get_featured(self):
        return self.repository.get_featured()

    def get_by_slug(self, slug: str) -> Optional[Podcast]:
        return self.repository.get_by_slug(slug)

    @transaction.atomic
    def create_podcast(self, **kwargs) -> Podcast:
        return self.repository.create(**kwargs)

    @transaction.atomic
    def update_podcast(self, podcast_id, **kwargs) -> Optional[Podcast]:
        podcast = self.repository.get_by_id(podcast_id)
        if podcast:
            return self.repository.update(podcast, **kwargs)
        return None

    @transaction.atomic
    def toggle_active(self, podcast_id) -> Optional[Podcast]:
        podcast = self.repository.get_by_id(podcast_id)
        if podcast:
            podcast.active = not podcast.active
            podcast.save(update_fields=['active'])
            return podcast
        return None

    @transaction.atomic
    def toggle_featured(self, podcast_id) -> Optional[Podcast]:
        podcast = self.repository.get_by_id(podcast_id)
        if podcast:
            podcast.featured = not podcast.featured
            podcast.save(update_fields=['featured'])
            return podcast
        return None

    def search_podcasts(self, query: str):
        return self.repository.search(query)


class PodcastEpisodeService(BaseService[PodcastEpisodeRepository]):
    def __init__(self):
        super().__init__(PodcastEpisodeRepository())

    def get_published(self):
        return self.repository.get_published()

    def get_for_podcast(self, podcast_id):
        return self.repository.get_for_podcast(podcast_id)

    @transaction.atomic
    def create_episode(self, **kwargs) -> PodcastEpisode:
        return self.repository.create(**kwargs)

    @transaction.atomic
    def update_episode(self, episode_id, **kwargs) -> Optional[PodcastEpisode]:
        episode = self.repository.get_by_id(episode_id)
        if episode:
            return self.repository.update(episode, **kwargs)
        return None

    @transaction.atomic
    def publish(self, episode_id) -> Optional[PodcastEpisode]:
        episode = self.repository.get_by_id(episode_id)
        if episode:
            episode.published = True
            if not episode.publish_date:
                episode.publish_date = timezone.now()
            episode.save(update_fields=['published', 'publish_date'])
            return episode
        return None

    @transaction.atomic
    def unpublish(self, episode_id) -> Optional[PodcastEpisode]:
        episode = self.repository.get_by_id(episode_id)
        if episode:
            episode.published = False
            episode.save(update_fields=['published'])
            return episode
        return None

    @transaction.atomic
    def increment_download(self, episode_id) -> Optional[PodcastEpisode]:
        episode = self.repository.get_by_id(episode_id)
        if episode:
            episode.download_count = F('download_count') + 1
            episode.save(update_fields=['download_count'])
            episode.refresh_from_db()
            return episode
        return None
