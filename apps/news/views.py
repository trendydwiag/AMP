import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
)
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.text import slugify

from utils.mixins import AuditLogMixin
from .models import Article, Category, Tag
from .forms import ArticleForm


class ArticleCMSListView(LoginRequiredMixin, AuditLogMixin, ListView):
    model = Article
    template_name = 'news/cms/article_list.html'
    context_object_name = 'articles'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('category', 'author')
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(excerpt__icontains=q))
        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(category_id=category)
        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_filter'] = self.request.GET.get('status', '')
        ctx['q'] = self.request.GET.get('q', '')
        ctx['category_filter'] = self.request.GET.get('category', '')
        ctx['status_choices'] = [
            ('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Menunggu Review'),
            ('APPROVED', 'Disetujui'), ('SCHEDULED', 'Terjadwal'),
            ('PUBLISHED', 'Diterbitkan'), ('ARCHIVED', 'Diarsipkan'),
            ('REJECTED', 'Ditolak'),
        ]
        ctx['categories'] = Category.objects.filter(active=True).order_by('name')
        ctx['total_count'] = Article.objects.count()
        ctx['draft_count'] = Article.objects.filter(status='DRAFT').count()
        ctx['published_count'] = Article.objects.filter(status='PUBLISHED').count()
        ctx['pending_count'] = Article.objects.filter(status='PENDING_REVIEW').count()
        return ctx


class ArticleCMSCreateView(LoginRequiredMixin, AuditLogMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'news/cms/article_form.html'
    success_url = reverse_lazy('news:cms_article_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.filter(active=True).order_by('name')
        return ctx

    def form_valid(self, form):
        form.instance.author_name = self.request.user.get_full_name() or self.request.user.username
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.title)
        response = super().form_valid(form)
        self.log_action(self.request.user, 'ARTICLE_CREATE', f"Created article: {self.object.title}")
        return response


class ArticleCMSUpdateView(LoginRequiredMixin, AuditLogMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'news/cms/article_form.html'
    success_url = reverse_lazy('news:cms_article_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.filter(active=True).order_by('name')
        return ctx

    def form_valid(self, form):
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.title)
        form.instance.version = form.instance.version + 1
        response = super().form_valid(form)
        self.log_action(self.request.user, 'ARTICLE_UPDATE', f"Updated article: {self.object.title} v{self.object.version}")
        return response


class ArticleCMSDeleteView(LoginRequiredMixin, AuditLogMixin, DeleteView):
    model = Article
    template_name = 'news/cms/article_confirm_delete.html'
    success_url = reverse_lazy('news:cms_article_list')

    def form_valid(self, form):
        self.log_action(self.request.user, 'ARTICLE_DELETE', f"Deleted article: {self.object.title}")
        return super().form_valid(form)


class ArticleCMSDetailView(LoginRequiredMixin, AuditLogMixin, DetailView):
    model = Article
    template_name = 'news/cms/article_detail.html'
    context_object_name = 'article'


class ArticleCMSWorkflowView(LoginRequiredMixin, AuditLogMixin, TemplateView):
    def post(self, request, pk):
        article = Article.objects.filter(pk=pk).first()
        if not article:
            return JsonResponse({'error': 'Artikel tidak ditemukan'}, status=404)

        action = request.POST.get('action')
        valid_transitions = {
            'DRAFT': ['PENDING_REVIEW', 'ARCHIVED'],
            'PENDING_REVIEW': ['APPROVED', 'REJECTED'],
            'APPROVED': ['SCHEDULED', 'PUBLISHED'],
            'SCHEDULED': ['PUBLISHED', 'DRAFT'],
            'PUBLISHED': ['ARCHIVED', 'DRAFT'],
            'ARCHIVED': ['DRAFT'],
            'REJECTED': ['DRAFT'],
        }

        allowed = valid_transitions.get(article.status, [])
        if action not in allowed:
            return JsonResponse({'error': f'Transisi {action} tidak diizinkan dari status {article.status}'}, status=400)

        old_status = article.status
        article.status = action

        if action == 'PUBLISHED':
            article.last_published_at = timezone.now()
            if not article.publish_date:
                article.publish_date = timezone.now()

        article.save(update_fields=['status', 'last_published_at', 'publish_date', 'updated_at'])

        self.log_action(request.user, f'ARTICLE_{action}', f"Article '{article.title}' status: {old_status} -> {action}")

        if request.headers.get('HX-Request'):
            return JsonResponse({
                'status': 'ok',
                'new_status': article.status,
                'status_display': article.get_status_display(),
            })

        return JsonResponse({'status': 'ok', 'new_status': article.status})


class ArticleCMSPublishView(LoginRequiredMixin, AuditLogMixin, TemplateView):
    def post(self, request, pk):
        article = Article.objects.filter(pk=pk).first()
        if not article:
            return JsonResponse({'error': 'Artikel tidak ditemukan'}, status=404)

        article.status = 'PUBLISHED'
        article.last_published_at = timezone.now()
        if not article.publish_date:
            article.publish_date = timezone.now()
        article.save(update_fields=['status', 'last_published_at', 'publish_date', 'updated_at'])

        self.log_action(request.user, 'ARTICLE_PUBLISH', f"Published article: {article.title}")

        if request.headers.get('HX-Request'):
            return JsonResponse({'status': 'ok', 'new_status': 'PUBLISHED'})
        return JsonResponse({'status': 'ok'})


class ArticleCMSUnpublishView(LoginRequiredMixin, AuditLogMixin, TemplateView):
    def post(self, request, pk):
        article = Article.objects.filter(pk=pk).first()
        if not article:
            return JsonResponse({'error': 'Artikel tidak ditemukan'}, status=404)

        article.status = 'DRAFT'
        article.save(update_fields=['status', 'updated_at'])

        self.log_action(request.user, 'ARTICLE_UNPUBLISH', f"Unpublished article: {article.title}")

        if request.headers.get('HX-Request'):
            return JsonResponse({'status': 'ok', 'new_status': 'DRAFT'})
        return JsonResponse({'status': 'ok'})


class ArticleCMSScheduleView(LoginRequiredMixin, AuditLogMixin, TemplateView):
    def post(self, request, pk):
        article = Article.objects.filter(pk=pk).first()
        if not article:
            return JsonResponse({'error': 'Artikel tidak ditemukan'}, status=404)

        scheduled_at = request.POST.get('scheduled_at')
        if not scheduled_at:
            return JsonResponse({'error': 'Waktu jadwal harus diisi'}, status=400)

        article.scheduled_at = parse_datetime(scheduled_at)
        article.status = 'SCHEDULED'
        article.save(update_fields=['scheduled_at', 'status', 'updated_at'])

        self.log_action(request.user, 'ARTICLE_SCHEDULE', f"Scheduled article: {article.title} at {scheduled_at}")

        if request.headers.get('HX-Request'):
            return JsonResponse({'status': 'ok', 'new_status': 'SCHEDULED'})
        return JsonResponse({'status': 'ok'})


class ArticleCMSAutosaveView(LoginRequiredMixin, TemplateView):
    def post(self, request, pk):
        article = Article.objects.filter(pk=pk).first()
        if not article:
            return JsonResponse({'error': 'Artikel tidak ditemukan'}, status=404)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        for field in ['title', 'excerpt', 'content', 'seo_title', 'seo_description']:
            if field in data:
                setattr(article, field, data[field])

        article.save(update_fields=['title', 'excerpt', 'content', 'seo_title', 'seo_description', 'updated_at'])

        return JsonResponse({
            'status': 'ok',
            'saved_at': article.updated_at.isoformat(),
            'word_count': article.word_count,
            'reading_time': article.reading_time_minutes,
        })
