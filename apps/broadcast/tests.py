from django.test import TestCase, RequestFactory, override_settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import time, timedelta

from .models import (
    Program, Host, HostMember, Schedule, BroadcastSession,
    Episode, GuestStar, EpisodeGuest, Playlist, PlaylistItem, Announcement
)
from .repositories import (
    ProgramRepository, HostRepository, HostMemberRepository,
    ScheduleRepository, BroadcastSessionRepository, EpisodeRepository,
    GuestStarRepository, EpisodeGuestRepository, PlaylistRepository,
    PlaylistItemRepository, AnnouncementRepository
)
from .services import (
    ProgramService, HostService, ScheduleService, BroadcastService,
    EpisodeService, PlaylistService, AnnouncementService, CalendarService
)
from .forms import ProgramForm, HostForm, ScheduleForm, EpisodeForm, AnnouncementForm

User = get_user_model()


def create_admin_user():
    return User.objects.create_user(
        username='admin', email='admin@test.com',
        password='testpass123!', is_staff=True, is_superuser=True
    )


class ProgramRepositoryTest(TestCase):
    def setUp(self):
        self.repo = ProgramRepository()
        self.program = Program.objects.create(
            title='Morning Show', slug='morning-show',
            category='Talk', genre='News', active=True
        )

    def test_get_active(self):
        Program.objects.create(title='Inactive', slug='inactive', active=False)
        active = self.repo.get_active()
        self.assertEqual(active.count(), 1)

    def test_get_featured(self):
        Program.objects.create(title='Featured', slug='featured', featured=True, active=True)
        featured = self.repo.get_featured()
        self.assertEqual(featured.count(), 1)
        self.assertEqual(featured.first().slug, 'featured')

    def test_get_by_slug(self):
        result = self.repo.get_by_slug('morning-show')
        self.assertEqual(result.title, 'Morning Show')

    def test_get_by_slug_none(self):
        result = self.repo.get_by_slug('nonexistent')
        self.assertIsNone(result)

    def test_search(self):
        results = self.repo.search('Morning')
        self.assertEqual(results.count(), 1)

    def test_get_by_category(self):
        results = self.repo.get_by_category('Talk')
        self.assertEqual(results.count(), 1)

    def test_get_by_genre(self):
        results = self.repo.get_by_genre('News')
        self.assertEqual(results.count(), 1)


class HostRepositoryTest(TestCase):
    def setUp(self):
        self.repo = HostRepository()
        self.host = Host.objects.create(full_name='Budi Santoso', stage_name='Budi', active=True)

    def test_get_active(self):
        Host.objects.create(full_name='Inactive Host', active=False)
        active = self.repo.get_active()
        self.assertEqual(active.count(), 1)

    def test_search(self):
        results = self.repo.search('Budi')
        self.assertEqual(results.count(), 1)

    def test_get_with_programs(self):
        program = Program.objects.create(title='P1', slug='p1')
        HostMember.objects.create(host=self.host, program=program)
        members = self.repo.get_with_programs(self.host.pk)
        self.assertEqual(members.count(), 1)


class ScheduleRepositoryTest(TestCase):
    def setUp(self):
        self.repo = ScheduleRepository()
        self.program = Program.objects.create(title='P1', slug='p1', active=True)
        self.schedule = Schedule.objects.create(
            program=self.program, day_of_week='MON',
            start_time=time(8, 0), end_time=time(10, 0), active=True
        )

    def test_get_active(self):
        active = self.repo.get_active()
        self.assertEqual(active.count(), 1)

    def test_get_for_program(self):
        results = self.repo.get_for_program(self.program.pk)
        self.assertEqual(results.count(), 1)

    def test_get_for_day(self):
        results = self.repo.get_for_day('MON')
        self.assertEqual(results.count(), 1)

    def test_get_overlapping(self):
        overlaps = self.repo.get_overlapping('MON', time(9, 0), time(11, 0))
        self.assertEqual(len(overlaps), 1)

    def test_get_no_overlap(self):
        overlaps = self.repo.get_overlapping('MON', time(10, 0), time(12, 0))
        self.assertEqual(len(overlaps), 0)


class BroadcastSessionRepositoryTest(TestCase):
    def setUp(self):
        self.repo = BroadcastSessionRepository()
        self.program = Program.objects.create(title='P1', slug='p1', active=True)

    def test_get_upcoming(self):
        future = timezone.now() + timedelta(days=1)
        BroadcastSession.objects.create(
            program=self.program, start_datetime=future, status='SCHEDULED'
        )
        upcoming = self.repo.get_upcoming()
        self.assertEqual(upcoming.count(), 1)

    def test_get_live(self):
        BroadcastSession.objects.create(
            program=self.program, start_datetime=timezone.now(), status='LIVE'
        )
        live = self.repo.get_live()
        self.assertEqual(live.count(), 1)

    def test_get_finished(self):
        BroadcastSession.objects.create(
            program=self.program, start_datetime=timezone.now(), status='FINISHED'
        )
        finished = self.repo.get_finished()
        self.assertEqual(finished.count(), 1)


class EpisodeRepositoryTest(TestCase):
    def setUp(self):
        self.repo = EpisodeRepository()
        self.program = Program.objects.create(title='P1', slug='p1', active=True)

    def test_get_published(self):
        Episode.objects.create(program=self.program, title='Ep1', published=True, status='PUBLISHED')
        Episode.objects.create(program=self.program, title='Ep2', published=False)
        published = self.repo.get_published()
        self.assertEqual(published.count(), 1)

    def test_get_for_program(self):
        Episode.objects.create(program=self.program, title='Ep1', published=True, status='PUBLISHED')
        results = self.repo.get_for_program(self.program.pk)
        self.assertEqual(results.count(), 1)

    def test_search(self):
        Episode.objects.create(program=self.program, title='Unique Title', published=True, status='PUBLISHED')
        results = self.repo.search('Unique')
        self.assertEqual(results.count(), 1)


class AnnouncementRepositoryTest(TestCase):
    def setUp(self):
        self.repo = AnnouncementRepository()

    def test_get_active(self):
        Announcement.objects.create(
            title='Ann', content='Content',
            publish_start=timezone.now() - timedelta(days=1), active=True
        )
        Announcement.objects.create(
            title='Inactive', content='Content',
            publish_start=timezone.now() - timedelta(days=1), active=False
        )
        active = self.repo.get_active()
        self.assertEqual(active.count(), 1)

    def test_get_current(self):
        now = timezone.now()
        Announcement.objects.create(
            title='Current', content='Content',
            publish_start=now - timedelta(days=1),
            publish_end=now + timedelta(days=1), active=True
        )
        current = self.repo.get_current()
        self.assertEqual(current.count(), 1)

    def test_get_current_expired(self):
        now = timezone.now()
        Announcement.objects.create(
            title='Expired', content='Content',
            publish_start=now - timedelta(days=10),
            publish_end=now - timedelta(days=5), active=True
        )
        current = self.repo.get_current()
        self.assertEqual(current.count(), 0)


class ProgramServiceTest(TestCase):
    def setUp(self):
        self.svc = ProgramService()
        self.program = Program.objects.create(
            title='Morning Show', slug='morning-show', active=True
        )

    def test_get_active_programs(self):
        Program.objects.create(title='Inactive', slug='inactive', active=False)
        active = self.svc.get_active_programs()
        self.assertEqual(active.count(), 1)

    def test_get_featured_programs(self):
        Program.objects.create(title='Featured', slug='featured', featured=True, active=True)
        featured = self.svc.get_featured_programs()
        self.assertEqual(featured.count(), 1)

    def test_get_by_slug(self):
        result = self.svc.get_by_slug('morning-show')
        self.assertEqual(result.title, 'Morning Show')

    def test_toggle_active(self):
        self.svc.toggle_active(self.program.pk)
        self.program.refresh_from_db()
        self.assertFalse(self.program.active)

    def test_toggle_featured(self):
        self.svc.toggle_featured(self.program.pk)
        self.program.refresh_from_db()
        self.assertTrue(self.program.featured)

    def test_search_programs(self):
        results = self.svc.search_programs('Morning')
        self.assertEqual(results.count(), 1)


class HostServiceTest(TestCase):
    def setUp(self):
        self.svc = HostService()
        self.host = Host.objects.create(full_name='Budi Santoso', active=True)

    def test_get_active_hosts(self):
        Host.objects.create(full_name='Inactive', active=False)
        active = self.svc.get_active_hosts()
        self.assertEqual(active.count(), 1)

    def test_toggle_active(self):
        self.svc.toggle_active(self.host.pk)
        self.host.refresh_from_db()
        self.assertFalse(self.host.active)

    def test_search_hosts(self):
        results = self.svc.search_hosts('Budi')
        self.assertEqual(results.count(), 1)

    def test_get_with_programs(self):
        program = Program.objects.create(title='P1', slug='p1', active=True)
        HostMember.objects.create(host=self.host, program=program)
        result = self.svc.get_with_programs(self.host.pk)
        self.assertEqual(result.count(), 1)


class ScheduleServiceTest(TestCase):
    def setUp(self):
        self.svc = ScheduleService()
        self.program = Program.objects.create(title='P1', slug='p1', active=True)

    def test_get_for_day(self):
        Schedule.objects.create(
            program=self.program, day_of_week='MON',
            start_time=time(8, 0), end_time=time(10, 0), active=True
        )
        results = self.svc.get_for_day('MON')
        self.assertEqual(results.count(), 1)

    def test_check_overlap(self):
        Schedule.objects.create(
            program=self.program, day_of_week='MON',
            start_time=time(8, 0), end_time=time(10, 0), active=True
        )
        overlaps = self.svc.check_overlap('MON', time(9, 0), time(11, 0))
        self.assertEqual(len(overlaps), 1)

    def test_check_no_overlap(self):
        overlaps = self.svc.check_overlap('MON', time(10, 0), time(12, 0))
        self.assertEqual(len(overlaps), 0)


class BroadcastServiceTest(TestCase):
    def setUp(self):
        self.svc = BroadcastService()
        self.program = Program.objects.create(title='P1', slug='p1', active=True)

    def test_get_upcoming(self):
        future = timezone.now() + timedelta(days=1)
        BroadcastSession.objects.create(
            program=self.program, start_datetime=future, status='SCHEDULED'
        )
        upcoming = self.svc.get_upcoming()
        self.assertEqual(upcoming.count(), 1)

    def test_get_live_sessions(self):
        BroadcastSession.objects.create(
            program=self.program, start_datetime=timezone.now(), status='LIVE'
        )
        live = self.svc.get_live_sessions()
        self.assertEqual(live.count(), 1)

    def test_get_finished(self):
        BroadcastSession.objects.create(
            program=self.program, start_datetime=timezone.now(), status='FINISHED'
        )
        finished = self.svc.get_finished()
        self.assertEqual(finished.count(), 1)

    def test_get_current_broadcast_none(self):
        result = self.svc.get_current_broadcast()
        self.assertIsNone(result)

    def test_get_next_broadcast_none(self):
        result = self.svc.get_next_broadcast()
        self.assertIsNone(result)

    def test_update_status(self):
        session = BroadcastSession.objects.create(
            program=self.program, start_datetime=timezone.now(), status='SCHEDULED'
        )
        updated = self.svc.update_status(session.pk, 'LIVE')
        self.assertEqual(updated.status, 'LIVE')

    def test_cancel_session(self):
        session = BroadcastSession.objects.create(
            program=self.program, start_datetime=timezone.now(), status='SCHEDULED'
        )
        cancelled = self.svc.cancel_session(session.pk)
        self.assertEqual(cancelled.status, 'CANCELLED')


class EpisodeServiceTest(TestCase):
    def setUp(self):
        self.svc = EpisodeService()
        self.program = Program.objects.create(title='P1', slug='p1', active=True)

    def test_get_published(self):
        Episode.objects.create(program=self.program, title='Ep1', published=True, status='PUBLISHED')
        Episode.objects.create(program=self.program, title='Ep2', published=False)
        published = self.svc.get_published()
        self.assertEqual(published.count(), 1)

    def test_publish(self):
        ep = Episode.objects.create(program=self.program, title='Ep1', published=False)
        result = self.svc.publish(ep.pk)
        self.assertTrue(result.published)
        self.assertIsNotNone(result.publish_date)

    def test_unpublish(self):
        ep = Episode.objects.create(program=self.program, title='Ep1', published=True, status='PUBLISHED')
        result = self.svc.unpublish(ep.pk)
        self.assertFalse(result.published)

    def test_search_episodes(self):
        Episode.objects.create(program=self.program, title='Unique Title', published=True, status='PUBLISHED')
        results = self.svc.search_episodes('Unique')
        self.assertEqual(results.count(), 1)


class PlaylistServiceTest(TestCase):
    def setUp(self):
        self.svc = PlaylistService()
        self.program = Program.objects.create(title='P1', slug='p1', active=True)

    def test_get_active_playlists(self):
        Playlist.objects.create(program=self.program, title='PL1', active=True)
        Playlist.objects.create(program=self.program, title='PL2', active=False)
        active = self.svc.get_active_playlists()
        self.assertEqual(active.count(), 1)

    def test_add_item(self):
        playlist = Playlist.objects.create(program=self.program, title='PL1')
        item = self.svc.add_item(playlist.pk, title='Song 1', artist='Artist 1')
        self.assertEqual(item.sequence, 1)
        self.assertEqual(item.title, 'Song 1')

    def test_remove_item(self):
        playlist = Playlist.objects.create(program=self.program, title='PL1')
        item = PlaylistItem.objects.create(playlist=playlist, title='Song 1', sequence=1)
        result = self.svc.remove_item(item.pk)
        self.assertTrue(result)
        self.assertEqual(PlaylistItem.objects.count(), 0)


class AnnouncementServiceTest(TestCase):
    def setUp(self):
        self.svc = AnnouncementService()

    def test_get_active_announcements(self):
        now = timezone.now()
        Announcement.objects.create(
            title='Active', content='Content',
            publish_start=now - timedelta(days=1), active=True
        )
        Announcement.objects.create(
            title='Inactive', content='Content',
            publish_start=now - timedelta(days=1), active=False
        )
        active = self.svc.get_active_announcements()
        self.assertEqual(active.count(), 1)

    def test_get_current_announcements(self):
        now = timezone.now()
        Announcement.objects.create(
            title='Current', content='Content',
            publish_start=now - timedelta(days=1),
            publish_end=now + timedelta(days=1), active=True
        )
        current = self.svc.get_current_announcements()
        self.assertEqual(current.count(), 1)

    def test_toggle_active(self):
        ann = Announcement.objects.create(
            title='Ann', content='Content',
            publish_start=timezone.now(), active=True
        )
        self.svc.toggle_active(ann.pk)
        ann.refresh_from_db()
        self.assertFalse(ann.active)


class CalendarServiceTest(TestCase):
    def setUp(self):
        self.svc = CalendarService()
        self.program = Program.objects.create(title='P1', slug='p1', active=True)

    def test_get_weekly_calendar(self):
        Schedule.objects.create(
            program=self.program, day_of_week='MON',
            start_time=time(8, 0), end_time=time(10, 0), active=True
        )
        result = self.svc.get_weekly_calendar()
        self.assertIn('MON', result)
        self.assertEqual(len(result['MON']), 1)

    def test_get_monthly_calendar(self):
        Schedule.objects.create(
            program=self.program, day_of_week='MON',
            start_time=time(8, 0), end_time=time(10, 0), active=True
        )
        result = self.svc.get_monthly_calendar(2026, 1)
        self.assertIsInstance(result, dict)


class ProgramFormTest(TestCase):
    def test_valid_form(self):
        form = ProgramForm(data={
            'title': 'Morning Show',
            'slug': 'morning-show',
            'short_description': 'A morning talk show',
            'full_description': 'Full description here',
            'category': 'Talk',
            'genre': 'News',
            'language': 'id',
            'content_rating': 'G',
            'active': True,
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_empty_slug_auto(self):
        form = ProgramForm(data={
            'title': 'My Program',
            'short_description': 'Desc',
            'full_description': 'Full desc',
            'category': 'Talk',
            'genre': 'News',
            'language': 'id',
            'content_rating': 'G',
            'active': True,
        })
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['slug'], 'my-program')


class HostFormTest(TestCase):
    def test_valid_form(self):
        form = HostForm(data={
            'full_name': 'Budi Santoso',
            'stage_name': 'Budi',
            'active': True,
        })
        self.assertTrue(form.is_valid(), form.errors)


class ScheduleFormTest(TestCase):
    def setUp(self):
        self.program = Program.objects.create(title='P1', slug='p1', active=True)

    def test_valid_form(self):
        form = ScheduleForm(data={
            'program': self.program.pk,
            'day_of_week': 'MON',
            'start_time': '08:00',
            'end_time': '10:00',
            'timezone': 'Asia/Jakarta',
            'repeat_weekly': True,
            'active': True,
        })
        self.assertTrue(form.is_valid(), form.errors)


class EpisodeFormTest(TestCase):
    def setUp(self):
        self.program = Program.objects.create(title='P1', slug='p1', active=True)

    def test_valid_form(self):
        form = EpisodeForm(data={
            'program': self.program.pk,
            'episode_number': 1,
            'title': 'Episode 1',
            'description': 'A great episode',
        })
        self.assertTrue(form.is_valid(), form.errors)


class AnnouncementFormTest(TestCase):
    def test_valid_form(self):
        now = timezone.now()
        form = AnnouncementForm(data={
            'title': 'Breaking News',
            'content': 'Something important',
            'publish_start': now.strftime('%Y-%m-%dT%H:%M'),
            'active': True,
        })
        self.assertTrue(form.is_valid(), form.errors)


class ProgramModelTest(TestCase):
    def test_str(self):
        p = Program.objects.create(title='Morning Show', slug='morning-show')
        self.assertEqual(str(p), 'Morning Show')

    def test_host_property(self):
        p = Program.objects.create(title='P1', slug='p1')
        h = Host.objects.create(full_name='Host 1')
        HostMember.objects.create(host=h, program=p)
        self.assertEqual(p.hosts.count(), 1)


class HostModelTest(TestCase):
    def test_str_with_stage_name(self):
        h = Host.objects.create(full_name='Budi Santoso', stage_name='Budi')
        self.assertEqual(str(h), 'Budi')

    def test_str_without_stage_name(self):
        h = Host.objects.create(full_name='Budi Santoso')
        self.assertEqual(str(h), 'Budi Santoso')

    def test_programs_property(self):
        h = Host.objects.create(full_name='Budi')
        p = Program.objects.create(title='P1', slug='p1')
        HostMember.objects.create(host=h, program=p)
        self.assertEqual(h.programs.count(), 1)


class HostMemberModelTest(TestCase):
    def test_str(self):
        h = Host.objects.create(full_name='Budi')
        p = Program.objects.create(title='P1', slug='p1')
        hm = HostMember.objects.create(host=h, program=p)
        self.assertEqual(str(hm), 'Budi - P1')


class ScheduleModelTest(TestCase):
    def test_str(self):
        p = Program.objects.create(title='P1', slug='p1')
        s = Schedule.objects.create(program=p, day_of_week='MON', start_time=time(8, 0), end_time=time(10, 0))
        self.assertIn('P1', str(s))

    def test_duration_minutes(self):
        p = Program.objects.create(title='P1', slug='p1')
        s = Schedule.objects.create(program=p, day_of_week='MON', start_time=time(8, 0), end_time=time(10, 0))
        self.assertEqual(s.duration_minutes, 120)


class BroadcastSessionModelTest(TestCase):
    def test_str(self):
        p = Program.objects.create(title='P1', slug='p1')
        s = BroadcastSession.objects.create(program=p, start_datetime=timezone.now(), status='LIVE')
        self.assertIn('P1', str(s))

    def test_is_live(self):
        p = Program.objects.create(title='P1', slug='p1')
        s = BroadcastSession.objects.create(program=p, start_datetime=timezone.now(), status='LIVE')
        self.assertTrue(s.is_live)

    def test_is_finished(self):
        p = Program.objects.create(title='P1', slug='p1')
        s = BroadcastSession.objects.create(program=p, start_datetime=timezone.now(), status='FINISHED')
        self.assertTrue(s.is_finished)

    def test_duration_display(self):
        p = Program.objects.create(title='P1', slug='p1')
        start = timezone.now()
        end = start + timedelta(hours=1, minutes=30)
        s = BroadcastSession.objects.create(program=p, start_datetime=start, end_datetime=end, status='FINISHED')
        self.assertEqual(s.duration_display, '1j 30m')


class EpisodeModelTest(TestCase):
    def test_str(self):
        p = Program.objects.create(title='P1', slug='p1')
        ep = Episode.objects.create(program=p, title='My Episode', episode_number=1)
        self.assertIn('P1', str(ep))
        self.assertIn('My Episode', str(ep))

    def test_is_published(self):
        p = Program.objects.create(title='P1', slug='p1')
        ep = Episode.objects.create(program=p, title='Ep1', status='PUBLISHED', publish_date=timezone.now())
        self.assertTrue(ep.is_published)

    def test_is_not_published(self):
        p = Program.objects.create(title='P1', slug='p1')
        ep = Episode.objects.create(program=p, title='Ep1', published=False)
        self.assertFalse(ep.is_published)


class GuestStarModelTest(TestCase):
    def test_str(self):
        g = GuestStar.objects.create(full_name='John Doe')
        self.assertEqual(str(g), 'John Doe')


class EpisodeGuestModelTest(TestCase):
    def test_str(self):
        p = Program.objects.create(title='P1', slug='p1')
        ep = Episode.objects.create(program=p, title='Ep1', episode_number=1)
        g = GuestStar.objects.create(full_name='Guest 1')
        eg = EpisodeGuest.objects.create(episode=ep, guest=g)
        self.assertEqual(str(eg), 'Guest 1 - Ep1')


class PlaylistModelTest(TestCase):
    def test_str(self):
        p = Program.objects.create(title='P1', slug='p1')
        pl = Playlist.objects.create(program=p, title='Top Hits')
        self.assertIn('P1', str(pl))
        self.assertIn('Top Hits', str(pl))


class PlaylistItemModelTest(TestCase):
    def test_str_with_artist(self):
        p = Program.objects.create(title='P1', slug='p1')
        pl = Playlist.objects.create(program=p, title='PL1')
        item = PlaylistItem.objects.create(playlist=pl, title='Song 1', artist='Artist 1')
        self.assertEqual(str(item), 'Artist 1 - Song 1')

    def test_str_without_artist(self):
        p = Program.objects.create(title='P1', slug='p1')
        pl = Playlist.objects.create(program=p, title='PL1')
        item = PlaylistItem.objects.create(playlist=pl, title='Song 1')
        self.assertEqual(str(item), 'Song 1')


class AnnouncementModelTest(TestCase):
    def test_str(self):
        ann = Announcement.objects.create(
            title='Breaking News', content='Important',
            publish_start=timezone.now()
        )
        self.assertEqual(str(ann), 'Breaking News')

    def test_is_current(self):
        now = timezone.now()
        ann = Announcement.objects.create(
            title='Current', content='Content',
            publish_start=now - timedelta(days=1),
            publish_end=now + timedelta(days=1), active=True
        )
        self.assertTrue(ann.is_current)

    def test_is_not_current_inactive(self):
        now = timezone.now()
        ann = Announcement.objects.create(
            title='Inactive', content='Content',
            publish_start=now - timedelta(days=1), active=False
        )
        self.assertFalse(ann.is_current)

    def test_is_not_current_expired(self):
        now = timezone.now()
        ann = Announcement.objects.create(
            title='Expired', content='Content',
            publish_start=now - timedelta(days=10),
            publish_end=now - timedelta(days=5), active=True
        )
        self.assertFalse(ann.is_current)


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class BroadcastDashboardViewTest(TestCase):
    def test_dashboard_requires_login(self):
        from django.test import Client
        client = Client()
        response = client.get('/broadcast/')
        self.assertEqual(response.status_code, 302)

    def test_dashboard_renders(self):
        from django.test import Client
        client = Client()
        user = create_admin_user()
        client.login(username='admin', password='testpass123!')
        response = client.get('/broadcast/')
        self.assertEqual(response.status_code, 200)


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class ProgramViewTest(TestCase):
    def setUp(self):
        self.user = create_admin_user()
        self.client.login(username='admin', password='testpass123!')

    def test_program_list(self):
        response = self.client.get('/broadcast/program/')
        self.assertEqual(response.status_code, 200)

    def test_program_create_get(self):
        response = self.client.get('/broadcast/program/buat/')
        self.assertEqual(response.status_code, 200)

    def test_program_create_post(self):
        response = self.client.post('/broadcast/program/buat/', {
            'title': 'New Program',
            'slug': 'new-program',
            'short_description': 'Desc',
            'full_description': 'Full desc',
            'category': 'Talk',
            'genre': 'News',
            'language': 'id',
            'content_rating': 'G',
            'active': True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Program.objects.filter(slug='new-program').exists())

    def test_program_edit(self):
        p = Program.objects.create(title='P1', slug='p1', active=True)
        response = self.client.get(f'/broadcast/program/{p.pk}/edit/')
        self.assertEqual(response.status_code, 200)

    def test_program_delete(self):
        p = Program.objects.create(title='P1', slug='p1', active=True)
        response = self.client.post(f'/broadcast/program/{p.pk}/hapus/')
        self.assertEqual(response.status_code, 302)
        p.refresh_from_db()
        self.assertFalse(p.active)


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class HostViewTest(TestCase):
    def setUp(self):
        self.user = create_admin_user()
        self.client.login(username='admin', password='testpass123!')

    def test_host_list(self):
        response = self.client.get('/broadcast/host/')
        self.assertEqual(response.status_code, 200)

    def test_host_create_get(self):
        response = self.client.get('/broadcast/host/buat/')
        self.assertEqual(response.status_code, 200)

    def test_host_create_post(self):
        response = self.client.post('/broadcast/host/buat/', {
            'full_name': 'New Host',
            'active': True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Host.objects.filter(full_name='New Host').exists())


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class ScheduleViewTest(TestCase):
    def setUp(self):
        self.user = create_admin_user()
        self.client.login(username='admin', password='testpass123!')
        self.program = Program.objects.create(title='P1', slug='p1', active=True)

    def test_schedule_list(self):
        response = self.client.get('/broadcast/jadwal/')
        self.assertEqual(response.status_code, 200)

    def test_schedule_create_get(self):
        response = self.client.get('/broadcast/jadwal/buat/')
        self.assertEqual(response.status_code, 200)

    def test_schedule_create_post(self):
        response = self.client.post('/broadcast/jadwal/buat/', {
            'program': self.program.pk,
            'day_of_week': 'MON',
            'start_time': '08:00',
            'end_time': '10:00',
            'timezone': 'Asia/Jakarta',
            'repeat_weekly': True,
            'active': True,
        })
        self.assertEqual(response.status_code, 302)


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class SessionViewTest(TestCase):
    def setUp(self):
        self.user = create_admin_user()
        self.client.login(username='admin', password='testpass123!')
        self.program = Program.objects.create(title='P1', slug='p1', active=True)

    def test_session_list(self):
        response = self.client.get('/broadcast/sesi/')
        self.assertEqual(response.status_code, 200)

    def test_session_create_get(self):
        response = self.client.get('/broadcast/sesi/buat/')
        self.assertEqual(response.status_code, 200)

    def test_session_create_post(self):
        future = (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')
        response = self.client.post('/broadcast/sesi/buat/', {
            'program': self.program.pk,
            'start_datetime': future,
            'status': 'SCHEDULED',
        })
        self.assertEqual(response.status_code, 302)


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class EpisodeViewTest(TestCase):
    def setUp(self):
        self.user = create_admin_user()
        self.client.login(username='admin', password='testpass123!')
        self.program = Program.objects.create(title='P1', slug='p1', active=True)

    def test_episode_list(self):
        response = self.client.get('/broadcast/episode/')
        self.assertEqual(response.status_code, 200)

    def test_episode_create_get(self):
        response = self.client.get('/broadcast/episode/buat/')
        self.assertEqual(response.status_code, 200)

    def test_episode_create_post(self):
        response = self.client.post('/broadcast/episode/buat/', {
            'program': self.program.pk,
            'episode_number': 1,
            'title': 'Episode 1',
            'description': 'A great episode',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Episode.objects.filter(title='Episode 1').exists())


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class AnnouncementViewTest(TestCase):
    def setUp(self):
        self.user = create_admin_user()
        self.client.login(username='admin', password='testpass123!')

    def test_announcement_list(self):
        response = self.client.get('/broadcast/pengumuman/')
        self.assertEqual(response.status_code, 200)

    def test_announcement_create_get(self):
        response = self.client.get('/broadcast/pengumuman/buat/')
        self.assertEqual(response.status_code, 200)

    def test_announcement_create_post(self):
        now = timezone.now()
        response = self.client.post('/broadcast/pengumuman/buat/', {
            'title': 'Breaking News',
            'content': 'Something important',
            'publish_start': now.strftime('%Y-%m-%dT%H:%M'),
            'active': True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Announcement.objects.filter(title='Breaking News').exists())


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class CalendarViewTest(TestCase):
    def setUp(self):
        self.user = create_admin_user()
        self.client.login(username='admin', password='testpass123!')

    def test_calendar_renders(self):
        response = self.client.get('/broadcast/kalender/')
        self.assertEqual(response.status_code, 200)

    def test_calendar_with_params(self):
        response = self.client.get('/broadcast/kalender/?year=2026&month=7')
        self.assertEqual(response.status_code, 200)


class APIViewTest(TestCase):
    def test_api_programs(self):
        Program.objects.create(title='P1', slug='p1', active=True, featured=False)
        response = self.client.get('/broadcast/api/programs/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('programs', data)

    def test_api_program_detail(self):
        Program.objects.create(title='P1', slug='p1', active=True)
        response = self.client.get('/broadcast/api/program/p1/')
        self.assertEqual(response.status_code, 200)

    def test_api_program_detail_404(self):
        response = self.client.get('/broadcast/api/program/nonexistent/')
        self.assertEqual(response.status_code, 404)

    def test_api_schedule(self):
        response = self.client.get('/broadcast/api/schedule/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('schedules', data)

    def test_api_today(self):
        response = self.client.get('/broadcast/api/today/')
        self.assertEqual(response.status_code, 200)

    def test_api_current(self):
        response = self.client.get('/broadcast/api/current/')
        self.assertEqual(response.status_code, 200)

    def test_api_next(self):
        response = self.client.get('/broadcast/api/next/')
        self.assertEqual(response.status_code, 200)

    def test_api_hosts(self):
        Host.objects.create(full_name='Budi', active=True)
        response = self.client.get('/broadcast/api/hosts/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('hosts', data)

    def test_api_episodes(self):
        response = self.client.get('/broadcast/api/episodes/')
        self.assertEqual(response.status_code, 200)

    def test_api_playlist(self):
        response = self.client.get('/broadcast/api/playlist/')
        self.assertEqual(response.status_code, 200)
