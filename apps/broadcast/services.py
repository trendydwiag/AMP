import logging
from typing import Optional, List, Dict, Any
from datetime import date, time, datetime, timedelta
from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from utils.services import BaseService
from .repositories import (
    ProgramRepository, HostRepository, HostMemberRepository,
    ScheduleRepository, BroadcastSessionRepository, EpisodeRepository,
    GuestStarRepository, EpisodeGuestRepository, PlaylistRepository,
    PlaylistItemRepository, AnnouncementRepository
)
from .models import (
    Program, Host, HostMember, Schedule, BroadcastSession,
    Episode, GuestStar, EpisodeGuest, Playlist, PlaylistItem, Announcement
)
from utils.choices import BroadcastStatus, DayOfWeek

logger = logging.getLogger('broadcast')


class ProgramService(BaseService[ProgramRepository]):
    def __init__(self):
        super().__init__(ProgramRepository())

    def get_active_programs(self):
        return Program.objects.filter(active=True)

    def get_featured_programs(self):
        return Program.objects.filter(featured=True, active=True)

    def get_by_slug(self, slug: str) -> Optional[Program]:
        try:
            return Program.objects.get(slug=slug)
        except Program.DoesNotExist:
            return None

    @transaction.atomic
    def create_program(self, **kwargs) -> Program:
        return self.repository.create(**kwargs)

    @transaction.atomic
    def update_program(self, program_id, **kwargs) -> Optional[Program]:
        program = self.repository.get_by_id(program_id)
        if program:
            return self.repository.update(program, **kwargs)
        return None

    @transaction.atomic
    def toggle_active(self, program_id) -> Optional[Program]:
        program = self.repository.get_by_id(program_id)
        if program:
            program.active = not program.active
            program.save(update_fields=['active'])
            return program
        return None

    @transaction.atomic
    def toggle_featured(self, program_id) -> Optional[Program]:
        program = self.repository.get_by_id(program_id)
        if program:
            program.featured = not program.featured
            program.save(update_fields=['featured'])
            return program
        return None

    def search_programs(self, query: str):
        return Program.objects.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(category__icontains=query) |
            Q(genre__icontains=query)
        )

    def get_by_category(self, category: str):
        return Program.objects.filter(category__iexact=category, active=True)

    def get_by_genre(self, genre: str):
        return Program.objects.filter(genre__iexact=genre, active=True)


class HostService(BaseService[HostRepository]):
    def __init__(self):
        super().__init__(HostRepository())

    def get_active_hosts(self):
        return Host.objects.filter(active=True)

    @transaction.atomic
    def create_host(self, **kwargs) -> Host:
        return self.repository.create(**kwargs)

    @transaction.atomic
    def update_host(self, host_id, **kwargs) -> Optional[Host]:
        host = self.repository.get_by_id(host_id)
        if host:
            return self.repository.update(host, **kwargs)
        return None

    @transaction.atomic
    def toggle_active(self, host_id) -> Optional[Host]:
        host = self.repository.get_by_id(host_id)
        if host:
            host.active = not host.active
            host.save(update_fields=['active'])
            return host
        return None

    def search_hosts(self, query: str):
        return Host.objects.filter(
            Q(full_name__icontains=query) |
            Q(stage_name__icontains=query) |
            Q(nickname__icontains=query) |
            Q(biography__icontains=query)
        )

    def get_with_programs(self, host_id) -> Optional[Host]:
        host = self.repository.get_by_id(host_id)
        if host:
            return host.host_members.select_related('program')
        return None


class ScheduleService(BaseService[ScheduleRepository]):
    def __init__(self):
        super().__init__(ScheduleRepository())

    def get_for_program(self, program_id):
        return Schedule.objects.filter(program_id=program_id, active=True)

    def get_for_day(self, day_of_week: str):
        return Schedule.objects.filter(day_of_week=day_of_week, active=True)

    def get_active_schedules(self):
        return Schedule.objects.filter(active=True)

    @transaction.atomic
    def create_schedule(self, **kwargs) -> Schedule:
        return self.repository.create(**kwargs)

    @transaction.atomic
    def update_schedule(self, schedule_id, **kwargs) -> Optional[Schedule]:
        schedule = self.repository.get_by_id(schedule_id)
        if schedule:
            return self.repository.update(schedule, **kwargs)
        return None

    def check_overlap(self, day: str, start: time, end: time, exclude_id=None) -> List[Schedule]:
        qs = Schedule.objects.filter(day_of_week=day, active=True)
        if exclude_id:
            qs = qs.exclude(pk=exclude_id)
        if end > start:
            return list(qs.filter(start_time__lt=end, end_time__gt=start))
        else:
            return list(qs.filter(
                Q(start_time__lt=end, end_time__gt=start) |
                Q(start_time__gte=start) |
                Q(end_time__lte=end)
            ))

    def check_host_availability(self, host_id, day: str, start: time, end: time, exclude_id=None) -> List[Schedule]:
        program_ids = HostMember.objects.filter(host_id=host_id).values_list('program_id', flat=True)
        qs = Schedule.objects.filter(
            program_id__in=program_ids,
            day_of_week=day,
            active=True
        )
        if exclude_id:
            qs = qs.exclude(pk=exclude_id)
        if end > start:
            return list(qs.filter(start_time__lt=end, end_time__gt=start))
        else:
            return list(qs.filter(
                Q(start_time__lt=end, end_time__gt=start) |
                Q(start_time__gte=start) |
                Q(end_time__lte=end)
            ))


class BroadcastService(BaseService[BroadcastSessionRepository]):
    def __init__(self):
        super().__init__(BroadcastSessionRepository())

    def get_upcoming(self):
        now = timezone.now()
        return BroadcastSession.objects.filter(
            start_datetime__gt=now,
            status__in=[BroadcastStatus.SCHEDULED, BroadcastStatus.DELAYED]
        )

    def get_live_sessions(self):
        return BroadcastSession.objects.filter(status=BroadcastStatus.LIVE)

    def get_finished(self):
        return BroadcastSession.objects.filter(status=BroadcastStatus.FINISHED)

    def get_for_program(self, program_id):
        return BroadcastSession.objects.filter(program_id=program_id)

    def get_current_broadcast(self) -> Optional[BroadcastSession]:
        now = timezone.now()
        return BroadcastSession.objects.filter(
            status=BroadcastStatus.LIVE
        ).order_by('-start_datetime').first() or BroadcastSession.objects.filter(
            start_datetime__lte=now,
            end_datetime__gte=now,
            status__in=[BroadcastStatus.SCHEDULED, BroadcastStatus.LIVE]
        ).order_by('-start_datetime').first()

    def get_next_broadcast(self) -> Optional[BroadcastSession]:
        now = timezone.now()
        return BroadcastSession.objects.filter(
            start_datetime__gt=now,
            status__in=[BroadcastStatus.SCHEDULED, BroadcastStatus.DELAYED]
        ).order_by('start_datetime').first()

    def get_previous_broadcast(self) -> Optional[BroadcastSession]:
        now = timezone.now()
        return BroadcastSession.objects.filter(
            status=BroadcastStatus.FINISHED
        ).order_by('-end_datetime').first()

    def get_today_schedule(self):
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        return BroadcastSession.objects.filter(
            start_datetime__gte=today_start,
            start_datetime__lt=today_end
        ).order_by('start_datetime')

    @transaction.atomic
    def create_session(self, **kwargs) -> BroadcastSession:
        return self.repository.create(**kwargs)

    @transaction.atomic
    def update_session(self, session_id, **kwargs) -> Optional[BroadcastSession]:
        session = self.repository.get_by_id(session_id)
        if session:
            return self.repository.update(session, **kwargs)
        return None

    @transaction.atomic
    def update_status(self, session_id, status: str) -> Optional[BroadcastSession]:
        session = self.repository.get_by_id(session_id)
        if session:
            session.status = status
            if status == BroadcastStatus.FINISHED and not session.end_datetime:
                session.end_datetime = timezone.now()
            session.save(update_fields=['status', 'end_datetime'])
            return session
        return None

    @transaction.atomic
    def cancel_session(self, session_id) -> Optional[BroadcastSession]:
        return self.update_status(session_id, BroadcastStatus.CANCELLED)


class EpisodeService(BaseService[EpisodeRepository]):
    def __init__(self):
        super().__init__(EpisodeRepository())

    def get_published(self):
        return Episode.objects.filter(published=True)

    def get_for_program(self, program_id):
        return Episode.objects.filter(program_id=program_id)

    @transaction.atomic
    def create_episode(self, **kwargs) -> Episode:
        return self.repository.create(**kwargs)

    @transaction.atomic
    def update_episode(self, episode_id, **kwargs) -> Optional[Episode]:
        episode = self.repository.get_by_id(episode_id)
        if episode:
            return self.repository.update(episode, **kwargs)
        return None

    @transaction.atomic
    def publish(self, episode_id) -> Optional[Episode]:
        episode = self.repository.get_by_id(episode_id)
        if episode:
            episode.published = True
            episode.publish_date = timezone.now()
            episode.save(update_fields=['published', 'publish_date'])
            return episode
        return None

    @transaction.atomic
    def unpublish(self, episode_id) -> Optional[Episode]:
        episode = self.repository.get_by_id(episode_id)
        if episode:
            episode.published = False
            episode.save(update_fields=['published'])
            return episode
        return None

    def search_episodes(self, query: str):
        return Episode.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )


class PlaylistService(BaseService[PlaylistRepository]):
    def __init__(self):
        super().__init__(PlaylistRepository())

    def get_active_playlists(self):
        return Playlist.objects.filter(active=True)

    def get_for_program(self, program_id):
        return Playlist.objects.filter(program_id=program_id)

    @transaction.atomic
    def create_playlist(self, **kwargs) -> Playlist:
        return self.repository.create(**kwargs)

    @transaction.atomic
    def update_playlist(self, playlist_id, **kwargs) -> Optional[Playlist]:
        playlist = self.repository.get_by_id(playlist_id)
        if playlist:
            return self.repository.update(playlist, **kwargs)
        return None

    @transaction.atomic
    def add_item(self, playlist_id, **kwargs) -> Optional[PlaylistItem]:
        playlist = self.repository.get_by_id(playlist_id)
        if not playlist:
            return None
        last_seq = PlaylistItem.objects.filter(playlist=playlist).order_by('-sequence').values_list('sequence', flat=True).first()
        sequence = (last_seq or 0) + 1
        kwargs.setdefault('playlist', playlist)
        kwargs.setdefault('sequence', sequence)
        return PlaylistItem.objects.create(**kwargs)

    @transaction.atomic
    def remove_item(self, item_id) -> bool:
        try:
            item = PlaylistItem.objects.get(pk=item_id)
            playlist = item.playlist
            item.delete()
            remaining = PlaylistItem.objects.filter(playlist=playlist).order_by('sequence')
            for i, obj in enumerate(remaining, start=1):
                if obj.sequence != i:
                    obj.sequence = i
                    obj.save(update_fields=['sequence'])
            return True
        except PlaylistItem.DoesNotExist:
            return False

    @transaction.atomic
    def reorder_items(self, playlist_id, item_ids: List) -> bool:
        playlist = self.repository.get_by_id(playlist_id)
        if not playlist:
            return False
        for i, item_id in enumerate(item_ids, start=1):
            try:
                item = PlaylistItem.objects.get(pk=item_id, playlist=playlist)
                item.sequence = i
                item.save(update_fields=['sequence'])
            except PlaylistItem.DoesNotExist:
                continue
        return True


class AnnouncementService(BaseService[AnnouncementRepository]):
    def __init__(self):
        super().__init__(AnnouncementRepository())

    def get_active_announcements(self):
        return Announcement.objects.filter(active=True)

    def get_current_announcements(self):
        now = timezone.now()
        return Announcement.objects.filter(
            active=True,
            publish_start__lte=now
        ).filter(
            Q(publish_end__isnull=True) | Q(publish_end__gte=now)
        )

    @transaction.atomic
    def create_announcement(self, **kwargs) -> Announcement:
        return self.repository.create(**kwargs)

    @transaction.atomic
    def update_announcement(self, announcement_id, **kwargs) -> Optional[Announcement]:
        announcement = self.repository.get_by_id(announcement_id)
        if announcement:
            return self.repository.update(announcement, **kwargs)
        return None

    @transaction.atomic
    def toggle_active(self, announcement_id) -> Optional[Announcement]:
        announcement = self.repository.get_by_id(announcement_id)
        if announcement:
            announcement.active = not announcement.active
            announcement.save(update_fields=['active'])
            return announcement
        return None


class CurrentProgramResolver:
    """Resolves the currently airing program from the broadcast schedule.

    Business rule: Broadcast Schedule → current datetime → current program.
    This is schedule-based resolution — no stream metadata dependency.
    Returns a dict with program name, host, schedule times, remaining minutes,
    and next program info. All fields are nullable/empty-safe.
    """

    DAY_MAP = {
        0: DayOfWeek.MONDAY,
        1: DayOfWeek.TUESDAY,
        2: DayOfWeek.WEDNESDAY,
        3: DayOfWeek.THURSDAY,
        4: DayOfWeek.FRIDAY,
        5: DayOfWeek.SATURDAY,
        6: DayOfWeek.SUNDAY,
    }

    def __init__(self):
        self.schedule_repo = ScheduleRepository()
        self.host_member_repo = HostMemberRepository()

    def resolve(self) -> Dict[str, Any]:
        """Return current program info dict, empty-safe."""
        now = timezone.now()
        # Convert to server's configured timezone (Asia/Jakarta) so that
        # schedule times — which are stored in WIB — are compared correctly.
        local_now = timezone.localtime(now)
        current_time = local_now.time()
        current_day = self.DAY_MAP[local_now.weekday()]

        schedules = self.schedule_repo.get_for_day(current_day)

        # Find the schedule that covers now
        current_schedule = None
        for sched in schedules:
            if sched.start_time <= current_time < sched.end_time:
                current_schedule = sched
                break

        if not current_schedule:
            return self._empty_response()

        # Resolve host
        host_member = self.host_member_repo.get_lead_hosts(
            current_schedule.program_id
        ).first()
        host_name = host_member.host.display_name if host_member else ''

        # Calculate remaining minutes using local time (WIB) for accuracy
        now_dt = local_now.replace(tzinfo=None)
        end_dt = local_now.replace(
            hour=current_schedule.end_time.hour,
            minute=current_schedule.end_time.minute,
            second=0, microsecond=0, tzinfo=None
        )
        remaining_minutes = max(0, int((end_dt - now_dt).total_seconds() / 60))

        # Find next schedule
        next_schedule = self._get_next_schedule(schedules, current_time, current_day)
        next_program = ''
        next_start = ''
        if next_schedule:
            next_program = next_schedule.program.title
            next_start = next_schedule.start_time.strftime('%H:%M')

        return {
            'current_program': current_schedule.program.title,
            'host': host_name,
            'start_time': current_schedule.start_time.strftime('%H:%M'),
            'end_time': current_schedule.end_time.strftime('%H:%M'),
            'remaining_minutes': remaining_minutes,
            'next_program': next_program,
            'next_start_time': next_start,
        }

    def _get_next_schedule(self, schedules, current_time, current_day):
        """Find the next schedule after current time, or first of tomorrow."""
        future = [
            s for s in schedules
            if s.start_time > current_time
        ]
        if future:
            return min(future, key=lambda s: s.start_time)
        return None

    def _empty_response(self) -> Dict[str, Any]:
        return {
            'current_program': '',
            'host': '',
            'start_time': '',
            'end_time': '',
            'remaining_minutes': 0,
            'next_program': '',
            'next_start_time': '',
        }


class CalendarService:
    def __init__(self):
        self.schedule_svc = ScheduleService()

    def get_weekly_calendar(self, target_date: date = None) -> Dict[str, List[Schedule]]:
        if target_date is None:
            target_date = timezone.now().date()
        weekday = target_date.weekday()
        day_mapping = {
            0: DayOfWeek.MONDAY,
            1: DayOfWeek.TUESDAY,
            2: DayOfWeek.WEDNESDAY,
            3: DayOfWeek.THURSDAY,
            4: DayOfWeek.FRIDAY,
            5: DayOfWeek.SATURDAY,
            6: DayOfWeek.SUNDAY,
        }
        result: Dict[str, List[Schedule]] = {}
        for day_num, day_code in day_mapping.items():
            schedules = Schedule.objects.filter(
                day_of_week=day_code, active=True
            ).select_related('program')
            result[day_code] = list(schedules)
        return result

    def get_monthly_calendar(self, year: int, month: int) -> Dict[date, List[Schedule]]:
        first_day = date(year, month, 1)
        if month == 12:
            last_day = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(year, month + 1, 1) - timedelta(days=1
)
        day_mapping = {
            0: DayOfWeek.MONDAY,
            1: DayOfWeek.TUESDAY,
            2: DayOfWeek.WEDNESDAY,
            3: DayOfWeek.THURSDAY,
            4: DayOfWeek.FRIDAY,
            5: DayOfWeek.SATURDAY,
            6: DayOfWeek.SUNDAY,
        }
        schedules_by_day: Dict[str, List[Schedule]] = {}
        for day_code in day_mapping.values():
            schedules = list(Schedule.objects.filter(
                day_of_week=day_code, active=True
            ).select_related('program'))
            schedules_by_day[day_code] = schedules
        result: Dict[date, List[Schedule]] = {}
        current = first_day
        while current <= last_day:
            day_code = day_mapping[current.weekday()]
            result[current] = schedules_by_day.get(day_code, [])
            current += timedelta(days=1)
        return result

    def get_programs_for_date(self, target_date: date) -> List[Program]:
        day_mapping = {
            0: DayOfWeek.MONDAY,
            1: DayOfWeek.TUESDAY,
            2: DayOfWeek.WEDNESDAY,
            3: DayOfWeek.THURSDAY,
            4: DayOfWeek.FRIDAY,
            5: DayOfWeek.SATURDAY,
            6: DayOfWeek.SUNDAY,
        }
        day_code = day_mapping[target_date.weekday()]
        program_ids = Schedule.objects.filter(
            day_of_week=day_code, active=True
        ).values_list('program_id', flat=True)
        return list(Program.objects.filter(pk__in=program_ids, active=True))
