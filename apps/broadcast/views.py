from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from apps.users.decorators import admin_required
from .models import (
    Program, Host, HostMember, Schedule, BroadcastSession,
    Episode, GuestStar, Playlist, Announcement
)
from .services import (
    ProgramService, HostService, ScheduleService, BroadcastService,
    EpisodeService, PlaylistService, AnnouncementService, CalendarService
)
from .forms import (
    ProgramForm, HostForm, HostMemberForm, ScheduleForm,
    BroadcastSessionForm, EpisodeForm, GuestStarForm,
    PlaylistForm, AnnouncementForm, BroadcastSearchForm
)


# ---------------------------------------------------------------------------
# Admin Dashboard
# ---------------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class BroadcastDashboardView(TemplateView):
    template_name = 'broadcast/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        broadcast_svc = BroadcastService()
        program_svc = ProgramService()
        episode_svc = EpisodeService()
        announcement_svc = AnnouncementService()
        calendar_svc = CalendarService()
        ctx['current_broadcast'] = broadcast_svc.get_current_broadcast()
        ctx['next_broadcast'] = broadcast_svc.get_next_broadcast()
        ctx['today_schedule'] = broadcast_svc.get_today_schedule()
        ctx['programs'] = program_svc.get_active_programs()
        ctx['recent_episodes'] = Episode.objects.select_related('program').order_by('-created_at')[:10]
        ctx['announcements'] = announcement_svc.get_current_announcements()
        ctx['program_count'] = Program.objects.count()
        ctx['host_count'] = Host.objects.filter(active=True).count()
        ctx['episode_count'] = Episode.objects.count()
        ctx['weekly_calendar'] = calendar_svc.get_weekly_calendar()
        return ctx


# ---------------------------------------------------------------------------
# Program CRUD
# ---------------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ProgramListView(TemplateView):
    template_name = 'broadcast/program_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        search = self.request.GET.get('q', '')
        svc = ProgramService()
        if search:
            ctx['programs'] = svc.search_programs(search)
        else:
            ctx['programs'] = Program.objects.select_related('created_by', 'updated_by').all()
        ctx['search'] = search
        return ctx


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ProgramCreateView(TemplateView):
    template_name = 'broadcast/program_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = ProgramForm()
        ctx['is_edit'] = False
        return ctx

    def post(self, request, *args, **kwargs):
        form = ProgramForm(request.POST, request.FILES)
        if form.is_valid():
            program = form.save(commit=False)
            program.created_by = request.user
            program.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Program berhasil dibuat.')
            return redirect('broadcast:program_list')
        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
        return self.render_to_response(ctx)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ProgramEditView(TemplateView):
    template_name = 'broadcast/program_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        program = get_object_or_404(Program, pk=kwargs['pk'])
        ctx['form'] = ProgramForm(instance=program)
        ctx['is_edit'] = True
        ctx['program'] = program
        return ctx

    def post(self, request, *args, **kwargs):
        program = get_object_or_404(Program, pk=kwargs['pk'])
        form = ProgramForm(request.POST, request.FILES, instance=program)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.updated_by = request.user
            updated.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Program berhasil diperbarui.')
            return redirect('broadcast:program_list')
        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
        return self.render_to_response(ctx)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ProgramDeleteView(View):
    def post(self, request, *args, **kwargs):
        from django.shortcuts import redirect
        from django.contrib import messages
        svc = ProgramService()
        svc.toggle_active(kwargs['pk'])
        messages.success(request, 'Program berhasil dihapus.')
        return redirect('broadcast:program_list')


# ---------------------------------------------------------------------------
# Host CRUD
# ---------------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class HostListView(TemplateView):
    template_name = 'broadcast/host_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        search = self.request.GET.get('q', '')
        svc = HostService()
        if search:
            ctx['hosts'] = svc.search_hosts(search)
        else:
            ctx['hosts'] = Host.objects.all()
        ctx['search'] = search
        return ctx


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class HostCreateView(TemplateView):
    template_name = 'broadcast/host_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = HostForm()
        ctx['is_edit'] = False
        return ctx

    def post(self, request, *args, **kwargs):
        form = HostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Host berhasil dibuat.')
            return redirect('broadcast:host_list')
        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
        return self.render_to_response(ctx)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class HostEditView(TemplateView):
    template_name = 'broadcast/host_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        host = get_object_or_404(Host, pk=kwargs['pk'])
        ctx['form'] = HostForm(instance=host)
        ctx['is_edit'] = True
        ctx['host'] = host
        return ctx

    def post(self, request, *args, **kwargs):
        host = get_object_or_404(Host, pk=kwargs['pk'])
        form = HostForm(request.POST, request.FILES, instance=host)
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Host berhasil diperbarui.')
            return redirect('broadcast:host_list')
        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
        return self.render_to_response(ctx)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class HostDeleteView(View):
    def post(self, request, *args, **kwargs):
        from django.shortcuts import redirect
        from django.contrib import messages
        svc = HostService()
        svc.toggle_active(kwargs['pk'])
        messages.success(request, 'Host berhasil dihapus.')
        return redirect('broadcast:host_list')


# ---------------------------------------------------------------------------
# Schedule CRUD
# ---------------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ScheduleListView(TemplateView):
    template_name = 'broadcast/schedule_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        day = self.request.GET.get('day', '')
        svc = ScheduleService()
        if day:
            ctx['schedules'] = svc.get_for_day(day)
        else:
            ctx['schedules'] = Schedule.objects.select_related('program').all()
        ctx['selected_day'] = day
        ctx['days'] = [(c, l) for c, l in DayOfWeek.choices]
        return ctx


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ScheduleCreateView(TemplateView):
    template_name = 'broadcast/schedule_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = ScheduleForm()
        ctx['is_edit'] = False
        return ctx

    def post(self, request, *args, **kwargs):
        form = ScheduleForm(request.POST)
        if form.is_valid():
            svc = ScheduleService()
            data = form.cleaned_data
            overlaps = svc.check_overlap(
                data['day_of_week'], data['start_time'], data['end_time']
            )
            if overlaps:
                from django.contrib import messages
                messages.error(request, 'Jadwal bertabrakan dengan jadwal lain di hari yang sama.')
                ctx = self.get_context_data(**kwargs)
                ctx['form'] = form
                return self.render_to_response(ctx)
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Jadwal berhasil dibuat.')
            return redirect('broadcast:schedule_list')
        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
        return self.render_to_response(ctx)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ScheduleEditView(TemplateView):
    template_name = 'broadcast/schedule_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        schedule = get_object_or_404(Schedule, pk=kwargs['pk'])
        ctx['form'] = ScheduleForm(instance=schedule)
        ctx['is_edit'] = True
        ctx['schedule'] = schedule
        return ctx

    def post(self, request, *args, **kwargs):
        schedule = get_object_or_404(Schedule, pk=kwargs['pk'])
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            svc = ScheduleService()
            data = form.cleaned_data
            overlaps = svc.check_overlap(
                data['day_of_week'], data['start_time'], data['end_time'],
                exclude_id=schedule.pk
            )
            if overlaps:
                from django.contrib import messages
                messages.error(request, 'Jadwal bertabrakan dengan jadwal lain di hari yang sama.')
                ctx = self.get_context_data(**kwargs)
                ctx['form'] = form
                return self.render_to_response(ctx)
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Jadwal berhasil diperbarui.')
            return redirect('broadcast:schedule_list')
        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
        return self.render_to_response(ctx)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ScheduleDeleteView(View):
    def post(self, request, *args, **kwargs):
        from django.shortcuts import redirect
        from django.contrib import messages
        schedule = get_object_or_404(Schedule, pk=kwargs['pk'])
        schedule.delete()
        messages.success(request, 'Jadwal berhasil dihapus.')
        return redirect('broadcast:schedule_list')


# ---------------------------------------------------------------------------
# Broadcast Session CRUD
# ---------------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class BroadcastSessionListView(TemplateView):
    template_name = 'broadcast/session_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        status = self.request.GET.get('status', '')
        svc = BroadcastService()
        if status == 'live':
            ctx['sessions'] = svc.get_live_sessions()
        elif status == 'upcoming':
            ctx['sessions'] = svc.get_upcoming()
        elif status == 'finished':
            ctx['sessions'] = svc.get_finished()
        else:
            ctx['sessions'] = BroadcastSession.objects.select_related('program').all()
        ctx['selected_status'] = status
        return ctx


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class BroadcastSessionCreateView(TemplateView):
    template_name = 'broadcast/session_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = BroadcastSessionForm()
        ctx['is_edit'] = False
        return ctx

    def post(self, request, *args, **kwargs):
        form = BroadcastSessionForm(request.POST)
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Sesi broadcast berhasil dibuat.')
            return redirect('broadcast:session_list')
        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
        return self.render_to_response(ctx)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class BroadcastSessionEditView(TemplateView):
    template_name = 'broadcast/session_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        session = get_object_or_404(BroadcastSession, pk=kwargs['pk'])
        ctx['form'] = BroadcastSessionForm(instance=session)
        ctx['is_edit'] = True
        ctx['session'] = session
        return ctx

    def post(self, request, *args, **kwargs):
        session = get_object_or_404(BroadcastSession, pk=kwargs['pk'])
        form = BroadcastSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Sesi broadcast berhasil diperbarui.')
            return redirect('broadcast:session_list')
        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
        return self.render_to_response(ctx)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class BroadcastSessionDeleteView(View):
    def post(self, request, *args, **kwargs):
        from django.shortcuts import redirect
        from django.contrib import messages
        svc = BroadcastService()
        svc.cancel_session(kwargs['pk'])
        messages.success(request, 'Sesi broadcast berhasil dibatalkan.')
        return redirect('broadcast:session_list')


# ---------------------------------------------------------------------------
# Episode CRUD
# ---------------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class EpisodeListView(TemplateView):
    template_name = 'broadcast/episode_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        search = self.request.GET.get('q', '')
        program_id = self.request.GET.get('program', '')
        svc = EpisodeService()
        if search:
            ctx['episodes'] = svc.search_episodes(search)
        elif program_id:
            ctx['episodes'] = svc.get_for_program(program_id)
        else:
            ctx['episodes'] = Episode.objects.select_related('program').all()
        ctx['search'] = search
        ctx['programs'] = Program.objects.all()
        ctx['selected_program'] = program_id
        return ctx


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class EpisodeCreateView(TemplateView):
    template_name = 'broadcast/episode_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = EpisodeForm()
        ctx['is_edit'] = False
        return ctx

    def post(self, request, *args, **kwargs):
        form = EpisodeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Episode berhasil dibuat.')
            return redirect('broadcast:episode_list')
        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
        return self.render_to_response(ctx)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class EpisodeEditView(TemplateView):
    template_name = 'broadcast/episode_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        episode = get_object_or_404(Episode, pk=kwargs['pk'])
        ctx['form'] = EpisodeForm(instance=episode)
        ctx['is_edit'] = True
        ctx['episode'] = episode
        return ctx

    def post(self, request, *args, **kwargs):
        episode = get_object_or_404(Episode, pk=kwargs['pk'])
        form = EpisodeForm(request.POST, request.FILES, instance=episode)
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Episode berhasil diperbarui.')
            return redirect('broadcast:episode_list')
        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
        return self.render_to_response(ctx)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class EpisodeDeleteView(View):
    def post(self, request, *args, **kwargs):
        from django.shortcuts import redirect
        from django.contrib import messages
        Episode.objects.filter(pk=kwargs['pk']).delete()
        messages.success(request, 'Episode berhasil dihapus.')
        return redirect('broadcast:episode_list')


# ---------------------------------------------------------------------------
# Announcement CRUD
# ---------------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class AnnouncementListView(TemplateView):
    template_name = 'broadcast/announcement_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['announcements'] = Announcement.objects.all()
        return ctx


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class AnnouncementCreateView(TemplateView):
    template_name = 'broadcast/announcement_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = AnnouncementForm()
        ctx['is_edit'] = False
        return ctx

    def post(self, request, *args, **kwargs):
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Pengumuman berhasil dibuat.')
            return redirect('broadcast:announcement_list')
        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
        return self.render_to_response(ctx)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class AnnouncementEditView(TemplateView):
    template_name = 'broadcast/announcement_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        announcement = get_object_or_404(Announcement, pk=kwargs['pk'])
        ctx['form'] = AnnouncementForm(instance=announcement)
        ctx['is_edit'] = True
        ctx['announcement'] = announcement
        return ctx

    def post(self, request, *args, **kwargs):
        announcement = get_object_or_404(Announcement, pk=kwargs['pk'])
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)
        if form.is_valid():
            form.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Pengumuman berhasil diperbarui.')
            return redirect('broadcast:announcement_list')
        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
        return self.render_to_response(ctx)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class AnnouncementDeleteView(View):
    def post(self, request, *args, **kwargs):
        from django.shortcuts import redirect
        from django.contrib import messages
        svc = AnnouncementService()
        svc.toggle_active(kwargs['pk'])
        messages.success(request, 'Pengumuman berhasil dihapus.')
        return redirect('broadcast:announcement_list')


# ---------------------------------------------------------------------------
# Calendar
# ---------------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class CalendarView(TemplateView):
    template_name = 'broadcast/calendar.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        calendar_svc = CalendarService()
        today = timezone.now().date()
        year = int(self.request.GET.get('year', today.year))
        month = int(self.request.GET.get('month', today.month))
        ctx['calendar'] = calendar_svc.get_monthly_calendar(year, month)
        ctx['year'] = year
        ctx['month'] = month
        from datetime import date as date_cls
        first_day = date_cls(year, month, 1)
        weekday_offset = (first_day.weekday()) % 7
        ctx['empty_days'] = range(weekday_offset)
        ctx['today_day'] = today.day if today.year == year and today.month == month else None
        return ctx


# ---------------------------------------------------------------------------
# Public API Views
# ---------------------------------------------------------------------------

class ProgramListAPIView(View):
    def get(self, request):
        svc = ProgramService()
        q = request.GET.get('q', '')
        qs = svc.search_programs(q) if q else svc.get_active_programs()
        data = [{
            'id': str(p.pk), 'title': p.title, 'slug': p.slug,
            'short_description': p.short_description,
            'category': p.category, 'genre': p.genre,
            'content_rating': p.content_rating,
            'featured': p.featured,
        } for p in qs[:50]]
        return JsonResponse({'programs': data})


class ProgramDetailAPIView(View):
    def get(self, request, slug=None):
        svc = ProgramService()
        program = svc.get_by_slug(slug) if slug else None
        if not program:
            return JsonResponse({'error': 'Program not found'}, status=404)
        hosts = [{'id': str(h.host.pk), 'name': h.host.display_name, 'is_lead': h.is_lead}
                 for h in program.host_members.select_related('host')]
        schedules = [{'day': s.get_day_of_week_display(), 'start': s.start_time.strftime('%H:%M'),
                      'end': s.end_time.strftime('%H:%M')} for s in program.schedules.filter(active=True)]
        return JsonResponse({
            'id': str(program.pk), 'title': program.title, 'slug': program.slug,
            'short_description': program.short_description,
            'full_description': program.full_description,
            'category': program.category, 'genre': program.genre,
            'content_rating': program.content_rating,
            'featured': program.featured,
            'hosts': hosts, 'schedules': schedules,
        })


class ScheduleAPIView(View):
    def get(self, request):
        day = request.GET.get('day', '')
        svc = ScheduleService()
        qs = svc.get_for_day(day) if day else svc.get_active_schedules()
        data = [{
            'id': str(s.pk), 'program': s.program.title,
            'day': s.get_day_of_week_display(), 'day_code': s.day_of_week,
            'start': s.start_time.strftime('%H:%M'), 'end': s.end_time.strftime('%H:%M'),
            'duration_minutes': s.duration_minutes,
        } for s in qs[:100]]
        return JsonResponse({'schedules': data})


class TodayScheduleAPIView(View):
    def get(self, request):
        svc = BroadcastService()
        sessions = svc.get_today_schedule()
        data = [{
            'id': str(s.pk), 'program': s.program.title,
            'start': s.start_datetime.isoformat(),
            'end': s.end_datetime.isoformat() if s.end_datetime else None,
            'status': s.status,
        } for s in sessions]
        return JsonResponse({'today': data})


class CurrentBroadcastAPIView(View):
    def get(self, request):
        svc = BroadcastService()
        session = svc.get_current_broadcast()
        if not session:
            return JsonResponse({'current': None})
        return JsonResponse({
            'current': {
                'id': str(session.pk), 'program': session.program.title,
                'start': session.start_datetime.isoformat(),
                'end': session.end_datetime.isoformat() if session.end_datetime else None,
                'status': session.status,
                'duration': session.duration_display,
            }
        })


class NextBroadcastAPIView(View):
    def get(self, request):
        svc = BroadcastService()
        session = svc.get_next_broadcast()
        if not session:
            return JsonResponse({'next': None})
        return JsonResponse({
            'next': {
                'id': str(session.pk), 'program': session.program.title,
                'start': session.start_datetime.isoformat(),
                'end': session.end_datetime.isoformat() if session.end_datetime else None,
                'status': session.status,
            }
        })


class HostListAPIView(View):
    def get(self, request):
        svc = HostService()
        q = request.GET.get('q', '')
        qs = svc.search_hosts(q) if q else svc.get_active_hosts()
        data = [{
            'id': str(h.pk), 'full_name': h.full_name,
            'stage_name': h.stage_name, 'display_name': h.display_name,
            'email': h.email,
        } for h in qs[:50]]
        return JsonResponse({'hosts': data})


class HostDetailAPIView(View):
    def get(self, request, pk=None):
        svc = HostService()
        host = svc.repository.get_by_id(pk)
        if not host:
            return JsonResponse({'error': 'Host not found'}, status=404)
        programs = [{'id': str(hm.program.pk), 'title': hm.program.title, 'is_lead': hm.is_lead}
                    for hm in host.host_members.select_related('program')]
        return JsonResponse({
            'id': str(host.pk), 'full_name': host.full_name,
            'stage_name': host.stage_name, 'display_name': host.display_name,
            'biography': host.biography, 'email': host.email,
            'instagram': host.instagram, 'youtube': host.youtube,
            'programs': programs,
        })


class EpisodeListAPIView(View):
    def get(self, request):
        svc = EpisodeService()
        q = request.GET.get('q', '')
        program_id = request.GET.get('program', '')
        if q:
            qs = svc.search_episodes(q)
        elif program_id:
            qs = svc.get_for_program(program_id)
        else:
            qs = svc.get_published()
        data = [{
            'id': str(e.pk), 'title': e.title,
            'program': e.program.title,
            'episode_number': e.episode_number,
            'published': e.published,
            'publish_date': e.publish_date.isoformat() if e.publish_date else None,
        } for e in qs[:50]]
        return JsonResponse({'episodes': data})


class PlaylistAPIView(View):
    def get(self, request):
        program_id = request.GET.get('program', '')
        svc = PlaylistService()
        qs = svc.get_for_program(program_id) if program_id else svc.get_active_playlists()
        data = []
        for pl in qs[:50]:
            items = [{'title': i.title, 'artist': i.artist, 'duration': i.duration}
                     for i in pl.items.all()[:20]]
            data.append({
                'id': str(pl.pk), 'title': pl.title,
                'program': pl.program.title, 'items': items,
            })
        return JsonResponse({'playlists': data})


# ---------------------------------------------------------------------------
# CMS Views – Program
# ---------------------------------------------------------------------------

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify
from utils.mixins import AuditLogMixin


class ProgramCMSListView(LoginRequiredMixin, AuditLogMixin, ListView):
    model = Program
    template_name = 'broadcast/cms/program_list.html'
    context_object_name = 'programs'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(full_description__icontains=q))
        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_filter'] = self.request.GET.get('status', '')
        ctx['q'] = self.request.GET.get('q', '')
        ctx['status_choices'] = [('DRAFT', 'Draft'), ('PUBLISHED', 'Published'), ('ARCHIVED', 'Diarsipkan')]
        ctx['total_count'] = Program.objects.count()
        ctx['published_count'] = Program.objects.filter(status='PUBLISHED').count()
        return ctx


class ProgramCMSCreateView(LoginRequiredMixin, AuditLogMixin, CreateView):
    model = Program
    template_name = 'broadcast/cms/program_form.html'
    fields = ['title', 'short_description', 'full_description', 'thumbnail', 'banner', 'category', 'language', 'genre', 'target_audience', 'content_rating', 'featured', 'status', 'seo_title', 'seo_description']
    success_url = reverse_lazy('broadcast:cms_program_list')

    def form_valid(self, form):
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.title)
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        self.log_action(self.request.user, 'PROGRAM_CREATE', f"Created program: {self.object.title}")
        return response


class ProgramCMSUpdateView(LoginRequiredMixin, AuditLogMixin, UpdateView):
    model = Program
    template_name = 'broadcast/cms/program_form.html'
    fields = ['title', 'short_description', 'full_description', 'thumbnail', 'banner', 'category', 'language', 'genre', 'target_audience', 'content_rating', 'featured', 'active', 'status', 'seo_title', 'seo_description']
    success_url = reverse_lazy('broadcast:cms_program_list')

    def form_valid(self, form):
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.title)
        form.instance.updated_by = self.request.user
        response = super().form_valid(form)
        self.log_action(self.request.user, 'PROGRAM_UPDATE', f"Updated program: {self.object.title}")
        return response


class ProgramCMSDeleteView(LoginRequiredMixin, AuditLogMixin, DeleteView):
    model = Program
    template_name = 'broadcast/cms/program_confirm_delete.html'
    success_url = reverse_lazy('broadcast:cms_program_list')

    def form_valid(self, form):
        self.log_action(self.request.user, 'PROGRAM_DELETE', f"Deleted program: {self.object.title}")
        return super().form_valid(form)


class ProgramCMSDetailView(LoginRequiredMixin, AuditLogMixin, DetailView):
    model = Program
    template_name = 'broadcast/cms/program_detail.html'
    context_object_name = 'program'


class ProgramCMSWorkflowView(LoginRequiredMixin, AuditLogMixin, TemplateView):
    def post(self, request, pk):
        program = Program.objects.filter(pk=pk).first()
        if not program:
            return JsonResponse({'error': 'Program tidak ditemukan'}, status=404)
        action = request.POST.get('action')
        valid = {'DRAFT': ['PUBLISHED', 'ARCHIVED'], 'PUBLISHED': ['ARCHIVED', 'DRAFT'], 'ARCHIVED': ['DRAFT']}
        if action not in valid.get(program.status, []):
            return JsonResponse({'error': 'Transisi tidak diizinkan'}, status=400)
        old = program.status
        program.status = action
        if action == 'PUBLISHED':
            program.last_published_at = timezone.now()
        program.save(update_fields=['status', 'last_published_at', 'updated_at'])
        self.log_action(request.user, f'PROGRAM_{action}', f"Program '{program.title}' {old} -> {action}")
        if request.headers.get('HX-Request'):
            return JsonResponse({'status': 'ok', 'new_status': program.status})
        return JsonResponse({'status': 'ok'})


# ---------------------------------------------------------------------------
# CMS Views – Episode
# ---------------------------------------------------------------------------

class BroadcastEpisodeCMSListView(LoginRequiredMixin, AuditLogMixin, ListView):
    model = Episode
    template_name = 'broadcast/cms/episode_list.html'
    context_object_name = 'episodes'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('program')
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_filter'] = self.request.GET.get('status', '')
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class BroadcastEpisodeCMSCreateView(LoginRequiredMixin, AuditLogMixin, CreateView):
    model = Episode
    template_name = 'broadcast/cms/episode_form.html'
    fields = ['program', 'title', 'description', 'episode_number', 'cover_image', 'recording_audio', 'recording_video', 'status', 'transcript', 'og_title', 'og_description']
    success_url = reverse_lazy('broadcast:cms_episode_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.log_action(self.request.user, 'BROADCAST_EPISODE_CREATE', f"Created episode: {self.object.title}")
        return response


class BroadcastEpisodeCMSUpdateView(LoginRequiredMixin, AuditLogMixin, UpdateView):
    model = Episode
    template_name = 'broadcast/cms/episode_form.html'
    fields = ['program', 'title', 'description', 'episode_number', 'cover_image', 'recording_audio', 'recording_video', 'status', 'published', 'publish_date', 'transcript', 'og_title', 'og_description']
    success_url = reverse_lazy('broadcast:cms_episode_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.log_action(self.request.user, 'BROADCAST_EPISODE_UPDATE', f"Updated episode: {self.object.title}")
        return response


class BroadcastEpisodeCMSDeleteView(LoginRequiredMixin, AuditLogMixin, DeleteView):
    model = Episode
    template_name = 'broadcast/cms/episode_confirm_delete.html'
    success_url = reverse_lazy('broadcast:cms_episode_list')

    def form_valid(self, form):
        self.log_action(self.request.user, 'BROADCAST_EPISODE_DELETE', f"Deleted episode: {self.object.title}")
        return super().form_valid(form)


class BroadcastEpisodeCMSDetailView(LoginRequiredMixin, AuditLogMixin, DetailView):
    model = Episode
    template_name = 'broadcast/cms/episode_detail.html'
    context_object_name = 'episode'


class BroadcastEpisodeCMSWorkflowView(LoginRequiredMixin, AuditLogMixin, TemplateView):
    def post(self, request, pk):
        episode = Episode.objects.filter(pk=pk).first()
        if not episode:
            return JsonResponse({'error': 'Episode tidak ditemukan'}, status=404)
        action = request.POST.get('action')
        valid = {'DRAFT': ['PUBLISHED'], 'PUBLISHED': ['DRAFT']}
        if action not in valid.get(episode.status, []):
            return JsonResponse({'error': 'Transisi tidak diizinkan'}, status=400)
        episode.status = action
        if action == 'PUBLISHED':
            episode.last_published_at = timezone.now()
            episode.published = True
            if not episode.publish_date:
                episode.publish_date = timezone.now()
        else:
            episode.published = False
        episode.save(update_fields=['status', 'published', 'publish_date', 'last_published_at', 'updated_at'])
        self.log_action(request.user, f'BROADCAST_EPISODE_{action}', f"Episode '{episode.title}' -> {action}")
        if request.headers.get('HX-Request'):
            return JsonResponse({'status': 'ok', 'new_status': episode.status})
        return JsonResponse({'status': 'ok'})


# ---------------------------------------------------------------------------
# Imports used inline
# ---------------------------------------------------------------------------
from utils.choices import DayOfWeek  # noqa: E402 – used in ScheduleListView
