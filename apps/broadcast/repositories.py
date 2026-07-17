from typing import Optional, List
from django.db.models import Q
from django.utils import timezone
from utils.repositories import BaseRepository
from .models import (
    Program, Host, HostMember, Schedule, BroadcastSession,
    Episode, GuestStar, EpisodeGuest, Playlist, PlaylistItem, Announcement
)
from utils.choices import BroadcastStatus


class ProgramRepository(BaseRepository):
    model = Program

    def get_active(self):
        return self.model.objects.filter(active=True)

    def get_featured(self):
        return self.model.objects.filter(featured=True, active=True)

    def get_by_slug(self, slug: str) -> Optional[Program]:
        try:
            return self.model.objects.get(slug=slug)
        except self.model.DoesNotExist:
            return None

    def search(self, query: str):
        return self.model.objects.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(category__icontains=query) |
            Q(genre__icontains=query)
        )

    def get_by_category(self, category: str):
        return self.model.objects.filter(category__iexact=category, active=True)

    def get_by_genre(self, genre: str):
        return self.model.objects.filter(genre__iexact=genre, active=True)


class HostRepository(BaseRepository):
    model = Host

    def get_active(self):
        return self.model.objects.filter(active=True)

    def search(self, query: str):
        return self.model.objects.filter(
            Q(full_name__icontains=query) |
            Q(stage_name__icontains=query) |
            Q(nickname__icontains=query) |
            Q(biography__icontains=query)
        )

    def get_with_programs(self, host_id):
        host = self.get_by_id(host_id)
        if host:
            return host.host_members.select_related('program')
        return None


class HostMemberRepository(BaseRepository):
    model = HostMember

    def get_for_program(self, program_id):
        return self.model.objects.filter(program_id=program_id).select_related('host')

    def get_for_host(self, host_id):
        return self.model.objects.filter(host_id=host_id).select_related('program')

    def get_lead_hosts(self, program_id):
        return self.model.objects.filter(program_id=program_id, is_lead=True).select_related('host')


class ScheduleRepository(BaseRepository):
    model = Schedule

    def get_for_program(self, program_id):
        return self.model.objects.filter(program_id=program_id, active=True)

    def get_for_day(self, day_of_week: str):
        return self.model.objects.filter(day_of_week=day_of_week, active=True).select_related('program')

    def get_active(self):
        return self.model.objects.filter(active=True).select_related('program')

    def get_overlapping(self, day: str, start, end, exclude_id=None):
        qs = self.model.objects.filter(day_of_week=day, active=True)
        if exclude_id:
            qs = qs.exclude(pk=exclude_id)
        return list(qs.filter(start_time__lt=end, end_time__gt=start))

    def check_host_overlap(self, host_id, day: str, start, end, exclude_id=None):
        from .models import HostMember
        program_ids = HostMember.objects.filter(host_id=host_id).values_list('program_id', flat=True)
        qs = self.model.objects.filter(
            program_id__in=program_ids,
            day_of_week=day,
            active=True
        )
        if exclude_id:
            qs = qs.exclude(pk=exclude_id)
        return list(qs.filter(start_time__lt=end, end_time__gt=start))


class BroadcastSessionRepository(BaseRepository):
    model = BroadcastSession

    def get_upcoming(self):
        now = timezone.now()
        return self.model.objects.filter(
            start_datetime__gt=now,
            status__in=[BroadcastStatus.SCHEDULED, BroadcastStatus.DELAYED]
        ).select_related('program', 'schedule')

    def get_live(self):
        return self.model.objects.filter(
            status=BroadcastStatus.LIVE
        ).select_related('program')

    def get_finished(self):
        return self.model.objects.filter(
            status=BroadcastStatus.FINISHED
        ).select_related('program')

    def get_for_program(self, program_id):
        return self.model.objects.filter(program_id=program_id).select_related('program')

    def get_for_date(self, target_date):
        day_start = timezone.make_timezone_aware(
            timezone.datetime.combine(target_date, timezone.datetime.min.time())
        )
        day_end = day_start + timezone.timedelta(days=1)
        return self.model.objects.filter(
            start_datetime__gte=day_start,
            start_datetime__lt=day_end
        ).select_related('program', 'schedule')

    def get_current(self):
        now = timezone.now()
        return self.model.objects.filter(
            start_datetime__lte=now,
            end_datetime__gte=now,
            status__in=[BroadcastStatus.SCHEDULED, BroadcastStatus.LIVE]
        ).order_by('-start_datetime').first()

    def get_next(self):
        now = timezone.now()
        return self.model.objects.filter(
            start_datetime__gt=now,
            status__in=[BroadcastStatus.SCHEDULED, BroadcastStatus.DELAYED]
        ).order_by('start_datetime').first()

    def get_previous(self):
        return self.model.objects.filter(
            status=BroadcastStatus.FINISHED
        ).order_by('-end_datetime').first()


class EpisodeRepository(BaseRepository):
    model = Episode

    def get_published(self):
        return self.model.objects.filter(published=True).select_related('program')

    def get_for_program(self, program_id):
        return self.model.objects.filter(program_id=program_id).select_related('program')

    def search(self, query: str):
        return self.model.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).select_related('program')

    def get_recent(self, limit: int = 10):
        return self.model.objects.all().order_by('-created_at')[:limit]


class GuestStarRepository(BaseRepository):
    model = GuestStar

    def search(self, query: str):
        return self.model.objects.filter(
            Q(full_name__icontains=query) |
            Q(biography__icontains=query) |
            Q(organization__icontains=query)
        )


class EpisodeGuestRepository(BaseRepository):
    model = EpisodeGuest

    def get_for_episode(self, episode_id):
        return self.model.objects.filter(episode_id=episode_id).select_related('guest')

    def get_for_guest(self, guest_id):
        return self.model.objects.filter(guest_id=guest_id).select_related('episode')


class PlaylistRepository(BaseRepository):
    model = Playlist

    def get_active(self):
        return self.model.objects.filter(active=True).select_related('program')

    def get_for_program(self, program_id):
        return self.model.objects.filter(program_id=program_id)


class PlaylistItemRepository(BaseRepository):
    model = PlaylistItem

    def get_for_playlist(self, playlist_id):
        return self.model.objects.filter(playlist_id=playlist_id).order_by('sequence')


class AnnouncementRepository(BaseRepository):
    model = Announcement

    def get_active(self):
        return self.model.objects.filter(active=True)

    def get_current(self):
        now = timezone.now()
        return self.model.objects.filter(
            active=True,
            publish_start__lte=now
        ).filter(
            Q(publish_end__isnull=True) | Q(publish_end__gte=now)
        )
