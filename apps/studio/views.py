from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST


@method_decorator(login_required, name='dispatch')
class AMPStudioDashboardView(TemplateView):
    template_name = 'amp_studio/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # ── Stats ──
        stats = {}
        try:
            from apps.news.models import Article
            from apps.podcast.models import PodcastEpisode
            from apps.broadcast.models import Program, Episode
            from django.utils import timezone
            from datetime import timedelta

            today = timezone.now().date()
            week_ago = today - timedelta(days=7)

            stats['articles_today'] = Article.objects.filter(
                status='published', published_at__date=today
            ).count()
            stats['articles_pending'] = Article.objects.filter(
                status='pending_review'
            ).count()
            stats['podcast_total'] = PodcastEpisode.objects.count()
            stats['podcast_week'] = PodcastEpisode.objects.filter(
                created_at__date__gte=week_ago
            ).count()
            stats['programs_active'] = Program.objects.filter(is_active=True).count()
            stats['episodes_scheduled'] = Episode.objects.filter(
                status='scheduled'
            ).count()
        except Exception:
            pass

        context['stats'] = stats

        # ── Today's Schedule ──
        today_schedule = []
        current_program_info = {'current_program': '', 'host': '', 'start_time': '', 'end_time': '', 'remaining_minutes': 0, 'next_program': '', 'next_start_time': ''}
        try:
            from apps.broadcast.services import CurrentProgramResolver, ScheduleService
            from django.utils import timezone
            from utils.choices import DayOfWeek
            now = timezone.now()
            day_map = {
                0: DayOfWeek.MONDAY, 1: DayOfWeek.TUESDAY, 2: DayOfWeek.WEDNESDAY,
                3: DayOfWeek.THURSDAY, 4: DayOfWeek.FRIDAY, 5: DayOfWeek.SATURDAY, 6: DayOfWeek.SUNDAY,
            }
            current_day = day_map[now.weekday()]
            schedule_svc = ScheduleService()
            today_schedules = schedule_svc.get_for_day(current_day)

            for s in today_schedules:
                is_live = False
                is_past = False
                current_time = now.time()
                is_live = s.start_time <= current_time < s.end_time
                is_past = current_time >= s.end_time

                today_schedule.append({
                    'program_name': s.program.title if s.program else str(s),
                    'host_name': s.program.host_members.filter(is_lead=True).select_related('host').first().host.display_name if s.program else '',
                    'start_time': s.start_time,
                    'end_time': s.end_time,
                    'is_live': is_live,
                    'is_past': is_past,
                })

            resolver = CurrentProgramResolver()
            current_program_info = resolver.resolve()
        except Exception:
            pass

        context['today_schedule'] = today_schedule
        context['current_program_info'] = current_program_info

        # ── Recent Articles ──
        try:
            from apps.news.models import Article
            context['recent_articles'] = Article.objects.select_related(
                'category'
            ).order_by('-created_at')[:5]
        except Exception:
            context['recent_articles'] = []

        # ── Pending Reviews ──
        pending = []
        try:
            from apps.news.models import Article
            from apps.podcast.models import PodcastEpisode
            from apps.broadcast.models import Episode

            for a in Article.objects.filter(status='pending_review').order_by('-created_at')[:3]:
                pending.append({
                    'title': a.title,
                    'content_type': 'Artikel',
                    'author_name': getattr(a, 'author_name', ''),
                    'pk': a.pk,
                })
            for e in PodcastEpisode.objects.filter(status='pending_review').order_by('-created_at')[:3]:
                pending.append({
                    'title': e.title,
                    'content_type': 'Podcast',
                    'author_name': getattr(e, 'host_name', ''),
                    'pk': e.pk,
                })
        except Exception:
            pass

        context['pending_reviews'] = pending

        # ── Recent Activity ──
        activity = []
        try:
            from django.contrib.admin.models import LogEntry
            from django.contrib.contenttypes.models import ContentType

            logs = LogEntry.objects.select_related('user').order_by('-action_time')[:8]
            for log in logs:
                action_map = {
                    1: 'create',
                    2: 'update',
                    3: 'delete',
                }
                action = action_map.get(log.action_flag, 'other')
                desc = log.change_message if log.change_message else str(log.object_repr)

                activity.append({
                    'user_name': log.user.get_full_name() if log.user else 'Sistem',
                    'description': desc,
                    'action': action,
                    'timestamp': log.action_time,
                })
        except Exception:
            pass

        context['recent_activity'] = activity

        # ── Storage ──
        storage = {'used_gb': '0.0', 'total_gb': '50', 'percent': 0, 'audio_count': 0, 'image_count': 0}
        try:
            from django.conf import settings as django_settings
            import os
            media_root = getattr(django_settings, 'MEDIA_ROOT', '')
            if media_root and os.path.exists(media_root):
                total_size = 0
                audio_count = 0
                image_count = 0
                for dirpath, dirnames, filenames in os.walk(media_root):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        total_size += os.path.getsize(fp)
                        ext = os.path.splitext(f)[1].lower()
                        if ext in ('.mp3', '.wav', '.ogg', '.aac', '.flac', '.m4a'):
                            audio_count += 1
                        elif ext in ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'):
                            image_count += 1
                used_gb = round(total_size / (1024**3), 2)
                storage = {
                    'used_gb': used_gb,
                    'total_gb': '50',
                    'percent': min(used_gb / 50 * 100, 100),
                    'audio_count': audio_count,
                    'image_count': image_count,
                }
        except Exception:
            pass

        context['storage'] = storage

        # ── Popular Programs ──
        try:
            from apps.broadcast.models import Program
            from django.db.models import Count
            context['popular_programs'] = Program.objects.annotate(
                episode_count=Count('episodes')
            ).order_by('-episode_count')[:5]
        except Exception:
            context['popular_programs'] = []

        # ── Sponsor Summary ──
        try:
            from apps.sponsor.models import Sponsor
            context['active_sponsors'] = Sponsor.objects.filter(is_active=True).count()
        except Exception:
            context['active_sponsors'] = 0

        # ── Action Cards: detect missing content ──
        try:
            from apps.radio.models import RadioStation
            context['has_radio_station'] = RadioStation.objects.filter(is_active=True).exists()
        except Exception:
            context['has_radio_station'] = False

        try:
            from apps.podcast.models import PodcastEpisode
            context['has_podcast'] = PodcastEpisode.objects.exists()
        except Exception:
            context['has_podcast'] = False

        context['has_schedule'] = bool(context.get('today_schedule'))
        context['has_sponsor'] = context.get('active_sponsors', 0) > 0

        try:
            from apps.news.models import Article
            context['has_news'] = Article.objects.filter(status='published').exists()
        except Exception:
            context['has_news'] = False

        # ── Setup Wizard: check completion ──
        context['setup_wizard_done'] = self.request.session.get('setup_wizard_done', False)

        # ── P3: System Health Widget ──
        context['system_health'] = self._get_system_health()

        # ── Site Identity for welcome banner ──
        try:
            from apps.settings.models import SiteSettings
            site = SiteSettings.objects.first()
            if site:
                context['SITE_NAME'] = site.site_name or 'Kabulhaden Online'
                context['SITE_LOGO'] = site.site_logo.url if site.site_logo else None
            else:
                context['SITE_NAME'] = 'Kabulhaden Online'
                context['SITE_LOGO'] = None
        except Exception:
            context['SITE_NAME'] = 'Kabulhaden Online'
            context['SITE_LOGO'] = None

        return context

    def _get_system_health(self):
        """Compute system health for 6 services. Never raises — always returns a dict."""
        def s(status, label, detail=''):
            # status: 'healthy' | 'degraded' | 'down' | 'unknown'
            return {'status': status, 'label': label, 'detail': detail}

        health = {}

        # ── Streaming ──
        try:
            from apps.radio.models import StreamHealth, RadioStation
            station = RadioStation.objects.filter(is_active=True).first()
            if station:
                h = StreamHealth.objects.filter(station=station).order_by('-last_checked').first()
                if h:
                    ps = h.provider_status.upper()
                    if ps == 'HEALTHY':
                        health['streaming'] = s('healthy', 'Streaming', f'{h.stream_bitrate or "—"} kbps')
                    elif ps == 'DEGRADED':
                        health['streaming'] = s('degraded', 'Streaming', f'Respons {h.response_time or "—"}ms')
                    elif ps in ('DOWN', 'TIMEOUT'):
                        health['streaming'] = s('down', 'Streaming', h.error_message or 'Tidak dapat dijangkau')
                    else:
                        health['streaming'] = s('unknown', 'Streaming', 'Belum ada data')
                else:
                    health['streaming'] = s('unknown', 'Streaming', 'Belum ada data')
            else:
                health['streaming'] = s('down', 'Streaming', 'Tidak ada stasiun aktif')
        except Exception:
            health['streaming'] = s('unknown', 'Streaming', 'Tidak dapat diperiksa')

        # ── Website ──
        try:
            from apps.settings.models import SiteSettings
            site = SiteSettings.objects.first()
            if site and site.site_url:
                health['website'] = s('healthy', 'Website', site.site_url[:40])
            else:
                health['website'] = s('degraded', 'Website', 'URL situs belum dikonfigurasi')
        except Exception:
            health['website'] = s('unknown', 'Website', 'Tidak dapat diperiksa')

        # ── Database ──
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
            health['database'] = s('healthy', 'Database', 'Koneksi aktif')
        except Exception as e:
            health['database'] = s('down', 'Database', str(e)[:60])

        # ── Storage ──
        try:
            import shutil
            from django.conf import settings as dj_settings
            media_root = getattr(dj_settings, 'MEDIA_ROOT', '/tmp')
            total, used, free = shutil.disk_usage(media_root or '/')
            free_gb = round(free / (1024 ** 3), 1)
            pct_used = round(used / total * 100)
            if pct_used > 90:
                health['storage'] = s('down', 'Storage', f'{pct_used}% penuh')
            elif pct_used > 75:
                health['storage'] = s('degraded', 'Storage', f'{free_gb} GB tersisa')
            else:
                health['storage'] = s('healthy', 'Storage', f'{free_gb} GB tersisa')
        except Exception:
            health['storage'] = s('unknown', 'Storage', 'Tidak dapat diperiksa')

        # ── SSL ──
        try:
            request = self.request
            is_https = request.is_secure() or request.META.get('HTTP_X_FORWARDED_PROTO') == 'https'
            if is_https:
                health['ssl'] = s('healthy', 'SSL / HTTPS', 'Sertifikat aktif')
            else:
                health['ssl'] = s('degraded', 'SSL / HTTPS', 'HTTP saja (development)')
        except Exception:
            health['ssl'] = s('unknown', 'SSL / HTTPS', 'Tidak dapat diperiksa')

        # ── Backup ──
        try:
            import os
            from django.conf import settings as dj_settings
            backup_dir = getattr(dj_settings, 'BACKUP_DIR', None)
            if backup_dir and os.path.exists(backup_dir):
                backups = sorted([
                    f for f in os.listdir(backup_dir)
                    if f.endswith(('.sql', '.gz', '.zip'))
                ])
                if backups:
                    health['backup'] = s('healthy', 'Backup', f'Terakhir: {backups[-1][:20]}')
                else:
                    health['backup'] = s('degraded', 'Backup', 'Tidak ada file backup')
            else:
                health['backup'] = s('degraded', 'Backup', 'Direktori backup belum dikonfigurasi')
        except Exception:
            health['backup'] = s('degraded', 'Backup', 'Tidak terkonfigurasi')

        return health


@method_decorator(login_required, name='dispatch')
class AMPStudioPreviewView(View):
    def get(self, request, content_type, pk):
        template = f'amp_studio/preview.html'
        context = {'content_type': content_type, 'pk': pk}
        return render(request, template, context)


@method_decorator(login_required, name='dispatch')
class AMPStudioCalendarView(TemplateView):
    template_name = 'amp_studio/calendar.html'


@method_decorator(login_required, name='dispatch')
class AMPStudioMediaExplorerView(TemplateView):
    template_name = 'amp_studio/media_explorer.html'


@method_decorator(login_required, name='dispatch')
class AMPStudioAnalyticsView(TemplateView):
    template_name = 'amp_studio/analytics.html'


@method_decorator(login_required, name='dispatch')
class PartnerSwitchView(View):
    """Handle partner switching for SUPERUSER and ADMINISTRATOR roles."""

    def post(self, request, partner_pk):
        user = request.user
        if not hasattr(user, 'role') or user.role not in ('SUPERUSER', 'ADMINISTRATOR'):
            messages.error(request, 'Anda tidak memiliki izin untuk mengganti partner.')
            return redirect('studio:dashboard')

        from apps.platform.partner.service import PartnerService
        from apps.platform.partner.models import Partner
        service = PartnerService()

        partner = get_object_or_404(Partner, pk=partner_pk, is_deleted=False)

        if service.switch_partner(request, partner):
            messages.success(request, f'Beralih ke partner: {partner.name}')
        else:
            messages.error(request, f'Gagal beralih ke partner: {partner.name}')

        # Redirect back to referring page or dashboard
        next_url = request.META.get('HTTP_REFERER', '/')
        return redirect(next_url)

    def get(self, request, partner_pk):
        return self.post(request, partner_pk)


@method_decorator(login_required, name='dispatch')
class PartnerListView(View):
    """Return partner list as JSON for the partner switcher dropdown."""

    def get(self, request):
        user = request.user
        if not hasattr(user, 'role') or user.role not in ('SUPERUSER', 'ADMINISTRATOR'):
            return JsonResponse({'partners': [], 'current': None})

        from apps.platform.partner.service import PartnerService
        service = PartnerService()

        user_partners = service.get_user_partners(user)
        current_partner = getattr(request, 'partner_context', None)
        current_id = str(current_partner.partner.pk) if current_partner and current_partner.partner else None

        partners_data = []
        for p in user_partners:
            partners_data.append({
                'pk': str(p.pk),
                'name': p.name,
                'slug': p.slug,
                'tier': p.tier,
                'primary_color': p.primary_color,
                'logo_url': p.logo.url if p.logo else '',
                'company_name': p.company_name or p.name,
            })

        # If superuser and has only one partner, show all active partners
        if user.role == 'SUPERUSER' and len(partners_data) <= 1:
            all_partners = service.get_active_partners()
            partners_data = []
            for p in all_partners:
                partners_data.append({
                    'pk': str(p.pk),
                    'name': p.name,
                    'slug': p.slug,
                    'tier': p.tier,
                    'primary_color': p.primary_color,
                    'logo_url': p.logo.url if p.logo else '',
                    'company_name': p.company_name or p.name,
                })

        return JsonResponse({
            'partners': partners_data,
            'current': current_id,
        })


@method_decorator(login_required, name='dispatch')
class StreamingCenterView(TemplateView):
    """Streaming Center — single source of truth for stream configuration and live status."""
    template_name = 'amp_studio/streaming_center.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            from apps.radio.models import RadioStation, RadioProvider, StreamHealth
            from apps.radio.services import RadioStationService, StreamHealthService, ListenerService, NowPlayingService

            station_svc = RadioStationService()
            station = station_svc.get_primary_station()
            context['station'] = station

            if station:
                health_svc = StreamHealthService()
                listener_svc = ListenerService()
                np_svc = NowPlayingService()

                context['providers'] = station.providers.filter(active=True)
                context['primary_provider'] = station.primary_provider
                context['health'] = health_svc.get_latest(station.pk)
                context['listener_stat'] = listener_svc.get_current(station.pk)
                context['now_playing'] = np_svc.get_now_playing(station.pk)
                context['health_history'] = health_svc.get_health_history(station.pk, limit=20)
            else:
                context['providers'] = []
                context['primary_provider'] = None
                context['health'] = None
                context['listener_stat'] = None
                context['now_playing'] = None
                context['health_history'] = []

        except Exception:
            context['station'] = None
            context['providers'] = []
            context['primary_provider'] = None
            context['health'] = None
            context['listener_stat'] = None
            context['now_playing'] = None
            context['health_history'] = []

        return context


@method_decorator(login_required, name='dispatch')
class SetupWizardView(TemplateView):
    """Quick Setup Wizard — guided 5-step onboarding for first-time founders."""
    template_name = 'amp_studio/setup_wizard.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        step = int(request.GET.get('step', 1))
        context['current_step'] = max(1, min(step, 5))

        # Gather completion flags for each step
        try:
            from apps.settings.models import SiteSettings
            site = SiteSettings.objects.first()
            context['step1_done'] = bool(site and site.site_name)
            context['step2_done'] = bool(site and site.site_logo)
        except Exception:
            context['step1_done'] = False
            context['step2_done'] = False

        try:
            from apps.radio.models import RadioProvider
            context['step3_done'] = RadioProvider.objects.filter(active=True).exists()
        except Exception:
            context['step3_done'] = False

        try:
            from apps.settings.models import SocialMediaSettings
            sm = SocialMediaSettings.objects.first()
            context['step4_done'] = bool(sm and (sm.facebook_url or sm.instagram_url or sm.twitter_url))
        except Exception:
            context['step4_done'] = False

        context['step5_done'] = request.session.get('setup_wizard_done', False)

        # Build the steps list for the progress indicator
        # Format: (step_number, label, done)
        context['steps'] = [
            (1, 'Identitas Radio', context['step1_done']),
            (2, 'Upload Logo', context['step2_done']),
            (3, 'Streaming URL', context['step3_done']),
            (4, 'Media Sosial', context['step4_done']),
            (5, 'Selesai', context['step5_done']),
        ]
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """Mark wizard as complete."""
        request.session['setup_wizard_done'] = True
        messages.success(request, 'Selamat! Setup Kabulhaden Anda sudah selesai.')
        return redirect('studio:dashboard')


@method_decorator(login_required, name='dispatch')
class CommunityView(TemplateView):
    """Community hub — discussions and listener interactions."""
    template_name = 'amp_studio/community.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            from apps.community.models import Discussion, Reply
            context['discussion_count'] = Discussion.objects.count()
            context['reply_count'] = Reply.objects.count()
            context['discussions'] = Discussion.objects.select_related(
                'author'
            ).order_by('-created_at')[:10]
        except Exception:
            context['discussion_count'] = 0
            context['reply_count'] = 0
            context['discussions'] = []
        return context


@method_decorator(login_required, name='dispatch')
class IklanView(TemplateView):
    """Advertising & sponsor management."""
    template_name = 'amp_studio/iklan.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            from apps.sponsor.models import Sponsor, Advertisement
            context['sponsors'] = Sponsor.objects.order_by('-is_active', 'name')[:20]
            context['active_sponsors'] = Sponsor.objects.filter(is_active=True).count()
            context['ad_count'] = Advertisement.objects.count()
        except Exception:
            context['sponsors'] = []
            context['active_sponsors'] = 0
            context['ad_count'] = 0
        return context
