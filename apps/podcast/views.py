from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify

from utils.mixins import AuditLogMixin
from .models import Podcast, PodcastEpisode
from apps.content.models import ContentCategory, Author


class PodcastCMSListView(LoginRequiredMixin, AuditLogMixin, ListView):
    model = Podcast
    template_name = 'podcast/cms/podcast_list.html'
    context_object_name = 'podcasts'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
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
        ctx['status_choices'] = [('DRAFT', 'Draft'), ('PUBLISHED', 'Published'), ('ARCHIVED', 'Diarsipkan')]
        ctx['total_count'] = Podcast.objects.count()
        ctx['published_count'] = Podcast.objects.filter(status='PUBLISHED').count()
        return ctx


class PodcastCMSCreateView(LoginRequiredMixin, AuditLogMixin, CreateView):
    model = Podcast
    template_name = 'podcast/cms/podcast_form.html'
    fields = ['title', 'description', 'short_description', 'thumbnail', 'banner', 'category', 'language', 'seo_title', 'seo_description', 'status', 'featured']
    success_url = reverse_lazy('podcast:cms_podcast_list')

    def form_valid(self, form):
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.title)
        response = super().form_valid(form)
        self.log_action(self.request.user, 'PODCAST_CREATE', f"Created podcast: {self.object.title}")
        return response


class PodcastCMSUpdateView(LoginRequiredMixin, AuditLogMixin, UpdateView):
    model = Podcast
    template_name = 'podcast/cms/podcast_form.html'
    fields = ['title', 'description', 'short_description', 'thumbnail', 'banner', 'category', 'language', 'seo_title', 'seo_description', 'status', 'featured', 'active']
    success_url = reverse_lazy('podcast:cms_podcast_list')

    def form_valid(self, form):
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.title)
        response = super().form_valid(form)
        self.log_action(self.request.user, 'PODCAST_UPDATE', f"Updated podcast: {self.object.title}")
        return response


class PodcastCMSDeleteView(LoginRequiredMixin, AuditLogMixin, DeleteView):
    model = Podcast
    template_name = 'podcast/cms/podcast_confirm_delete.html'
    success_url = reverse_lazy('podcast:cms_podcast_list')

    def form_valid(self, form):
        self.log_action(self.request.user, 'PODCAST_DELETE', f"Deleted podcast: {self.object.title}")
        return super().form_valid(form)


class PodcastCMSDetailView(LoginRequiredMixin, AuditLogMixin, DetailView):
    model = Podcast
    template_name = 'podcast/cms/podcast_detail.html'
    context_object_name = 'podcast'


class PodcastCMSWorkflowView(LoginRequiredMixin, AuditLogMixin, TemplateView):
    def post(self, request, pk):
        podcast = Podcast.objects.filter(pk=pk).first()
        if not podcast:
            return JsonResponse({'error': 'Podcast tidak ditemukan'}, status=404)
        action = request.POST.get('action')
        valid = {'DRAFT': ['PUBLISHED', 'ARCHIVED'], 'PUBLISHED': ['ARCHIVED', 'DRAFT'], 'ARCHIVED': ['DRAFT']}
        if action not in valid.get(podcast.status, []):
            return JsonResponse({'error': f'Transisi tidak diizinkan'}, status=400)
        old = podcast.status
        podcast.status = action
        if action == 'PUBLISHED':
            podcast.last_published_at = timezone.now()
        podcast.save(update_fields=['status', 'last_published_at', 'updated_at'])
        self.log_action(request.user, f'PODCAST_{action}', f"Podcast '{podcast.title}' {old} -> {action}")
        if request.headers.get('HX-Request'):
            return JsonResponse({'status': 'ok', 'new_status': podcast.status})
        return JsonResponse({'status': 'ok'})


class PodcastEpisodeCMSListView(LoginRequiredMixin, AuditLogMixin, ListView):
    model = PodcastEpisode
    template_name = 'podcast/cms/episode_list.html'
    context_object_name = 'episodes'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('podcast')
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


class PodcastEpisodeCMSCreateView(LoginRequiredMixin, AuditLogMixin, CreateView):
    model = PodcastEpisode
    template_name = 'podcast/cms/episode_form.html'
    fields = ['podcast', 'title', 'description', 'audio_file', 'audio_url', 'cover_image', 'duration', 'episode_number', 'season_number', 'status', 'transcript', 'og_title', 'og_description']
    success_url = reverse_lazy('podcast:cms_episode_list')

    def form_valid(self, form):
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.title)
        response = super().form_valid(form)
        self.log_action(self.request.user, 'PODCAST_EPISODE_CREATE', f"Created episode: {self.object.title}")
        return response


class PodcastEpisodeCMSUpdateView(LoginRequiredMixin, AuditLogMixin, UpdateView):
    model = PodcastEpisode
    template_name = 'podcast/cms/episode_form.html'
    fields = ['podcast', 'title', 'description', 'audio_file', 'audio_url', 'cover_image', 'duration', 'episode_number', 'season_number', 'status', 'published', 'publish_date', 'transcript', 'og_title', 'og_description']
    success_url = reverse_lazy('podcast:cms_episode_list')

    def form_valid(self, form):
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.title)
        response = super().form_valid(form)
        self.log_action(self.request.user, 'PODCAST_EPISODE_UPDATE', f"Updated episode: {self.object.title}")
        return response


class PodcastEpisodeCMSDeleteView(LoginRequiredMixin, AuditLogMixin, DeleteView):
    model = PodcastEpisode
    template_name = 'podcast/cms/episode_confirm_delete.html'
    success_url = reverse_lazy('podcast:cms_episode_list')

    def form_valid(self, form):
        self.log_action(self.request.user, 'PODCAST_EPISODE_DELETE', f"Deleted episode: {self.object.title}")
        return super().form_valid(form)


class PodcastEpisodeCMSDetailView(LoginRequiredMixin, AuditLogMixin, DetailView):
    model = PodcastEpisode
    template_name = 'podcast/cms/episode_detail.html'
    context_object_name = 'episode'


class PodcastEpisodeCMSWorkflowView(LoginRequiredMixin, AuditLogMixin, TemplateView):
    def post(self, request, pk):
        episode = PodcastEpisode.objects.filter(pk=pk).first()
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
        self.log_action(request.user, f'PODCAST_EPISODE_{action}', f"Episode '{episode.title}' -> {action}")
        if request.headers.get('HX-Request'):
            return JsonResponse({'status': 'ok', 'new_status': episode.status})
        return JsonResponse({'status': 'ok'})
