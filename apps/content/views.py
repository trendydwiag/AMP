from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView, FormView
)
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from utils.mixins import AuditLogMixin
from .models import (
    ContentCategory, ContentTag, Author, SEOModel,
    ContentVersion, PublishingQueue, ContentHighlight
)
from .forms import (
    ContentCategoryForm, ContentTagForm, AuthorForm, SEOForm,
    ContentVersionForm, PublishingQueueForm, ContentHighlightForm,
    GlobalSearchForm
)
from .services import (
    ContentCategoryService, ContentTagService, AuthorService,
    SEOService, ContentVersionService, PublishingQueueService,
    ContentHighlightService
)


class CMSHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'content/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['total_articles'] = 0
        ctx['total_podcasts'] = 0
        ctx['total_programs'] = 0
        ctx['pending_publish'] = PublishingQueue.objects.filter(status='PENDING').count()
        ctx['recent_versions'] = ContentVersion.objects.order_by('-created_at')[:10]
        ctx['upcoming_publishes'] = PublishingQueue.objects.filter(
            status='PENDING', scheduled_at__gte=timezone.now()
        ).order_by('scheduled_at')[:5]
        return ctx


class ContentCategoryListView(LoginRequiredMixin, AuditLogMixin, ListView):
    model = ContentCategory
    template_name = 'content/category_list.html'
    context_object_name = 'categories'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        content_type = self.request.GET.get('content_type')
        if content_type:
            qs = qs.filter(content_type=content_type)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        return qs.order_by('content_type', 'display_order', 'name')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['content_type_filter'] = self.request.GET.get('content_type', '')
        ctx['q'] = self.request.GET.get('q', '')
        ctx['content_type_choices'] = ContentCategory.CONTENT_TYPE_CHOICES
        return ctx


class ContentCategoryCreateView(LoginRequiredMixin, AuditLogMixin, CreateView):
    model = ContentCategory
    form_class = ContentCategoryForm
    template_name = 'content/category_form.html'
    success_url = reverse_lazy('content:category_list')

    def form_valid(self, form):
        self.log_action(self.request.user, 'CONTENT_CATEGORY_CREATE', f"Created category: {form.instance.name}")
        return super().form_valid(form)


class ContentCategoryUpdateView(LoginRequiredMixin, AuditLogMixin, UpdateView):
    model = ContentCategory
    form_class = ContentCategoryForm
    template_name = 'content/category_form.html'
    success_url = reverse_lazy('content:category_list')

    def form_valid(self, form):
        self.log_action(self.request.user, 'CONTENT_CATEGORY_UPDATE', f"Updated category: {form.instance.name}")
        return super().form_valid(form)


class ContentCategoryDeleteView(LoginRequiredMixin, AuditLogMixin, DeleteView):
    model = ContentCategory
    template_name = 'content/category_confirm_delete.html'
    success_url = reverse_lazy('content:category_list')

    def form_valid(self, form):
        self.log_action(self.request.user, 'CONTENT_CATEGORY_DELETE', f"Deleted category: {self.object.name}")
        return super().form_valid(form)


class ContentTagListView(LoginRequiredMixin, AuditLogMixin, ListView):
    model = ContentTag
    template_name = 'content/tag_list.html'
    context_object_name = 'tags'
    paginate_by = 30

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q)
        return qs.order_by('-usage_count', 'name')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class ContentTagCreateView(LoginRequiredMixin, AuditLogMixin, CreateView):
    model = ContentTag
    form_class = ContentTagForm
    template_name = 'content/tag_form.html'
    success_url = reverse_lazy('content:tag_list')

    def form_valid(self, form):
        self.log_action(self.request.user, 'CONTENT_TAG_CREATE', f"Created tag: {form.instance.name}")
        return super().form_valid(form)


class ContentTagUpdateView(LoginRequiredMixin, AuditLogMixin, UpdateView):
    model = ContentTag
    form_class = ContentTagForm
    template_name = 'content/tag_form.html'
    success_url = reverse_lazy('content:tag_list')

    def form_valid(self, form):
        self.log_action(self.request.user, 'CONTENT_TAG_UPDATE', f"Updated tag: {form.instance.name}")
        return super().form_valid(form)


class ContentTagDeleteView(LoginRequiredMixin, AuditLogMixin, DeleteView):
    model = ContentTag
    template_name = 'content/tag_confirm_delete.html'
    success_url = reverse_lazy('content:tag_list')

    def form_valid(self, form):
        self.log_action(self.request.user, 'CONTENT_TAG_DELETE', f"Deleted tag: {self.object.name}")
        return super().form_valid(form)


class AuthorListView(LoginRequiredMixin, AuditLogMixin, ListView):
    model = Author
    template_name = 'content/author_list.html'
    context_object_name = 'authors'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(email__icontains=q))
        return qs.order_by('name')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class AuthorCreateView(LoginRequiredMixin, AuditLogMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'content/author_form.html'
    success_url = reverse_lazy('content:author_list')

    def form_valid(self, form):
        self.log_action(self.request.user, 'CONTENT_AUTHOR_CREATE', f"Created author: {form.instance.name}")
        return super().form_valid(form)


class AuthorUpdateView(LoginRequiredMixin, AuditLogMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'content/author_form.html'
    success_url = reverse_lazy('content:author_list')

    def form_valid(self, form):
        self.log_action(self.request.user, 'CONTENT_AUTHOR_UPDATE', f"Updated author: {form.instance.name}")
        return super().form_valid(form)


class AuthorDeleteView(LoginRequiredMixin, AuditLogMixin, DeleteView):
    model = Author
    template_name = 'content/author_confirm_delete.html'
    success_url = reverse_lazy('content:author_list')

    def form_valid(self, form):
        self.log_action(self.request.user, 'CONTENT_AUTHOR_DELETE', f"Deleted author: {self.object.name}")
        return super().form_valid(form)


class AuthorDetailView(LoginRequiredMixin, AuditLogMixin, DetailView):
    model = Author
    template_name = 'content/author_detail.html'
    context_object_name = 'author'


class SEOListView(LoginRequiredMixin, AuditLogMixin, ListView):
    model = SEOModel
    template_name = 'content/seo_list.html'
    context_object_name = 'seo_entries'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return qs.select_related('content_type').order_by('-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        low_score = SEOModel.objects.all()
        ctx['low_score_count'] = sum(1 for s in low_score if s.seo_score < 50)
        return ctx


class SEOCreateView(LoginRequiredMixin, AuditLogMixin, CreateView):
    model = SEOModel
    form_class = SEOForm
    template_name = 'content/seo_form.html'
    success_url = reverse_lazy('content:seo_list')

    def form_valid(self, form):
        self.log_action(self.request.user, 'CONTENT_SEO_CREATE', f"Created SEO for: {form.instance.content_type}")
        return super().form_valid(form)


class SEOUpdateView(LoginRequiredMixin, AuditLogMixin, UpdateView):
    model = SEOModel
    form_class = SEOForm
    template_name = 'content/seo_form.html'
    success_url = reverse_lazy('content:seo_list')

    def form_valid(self, form):
        self.log_action(self.request.user, 'CONTENT_SEO_UPDATE', f"Updated SEO: {form.instance.content_type}")
        return super().form_valid(form)


class ContentVersionListView(LoginRequiredMixin, AuditLogMixin, ListView):
    model = ContentVersion
    template_name = 'content/version_list.html'
    context_object_name = 'versions'
    paginate_by = 30

    def get_queryset(self):
        qs = super().get_queryset()
        content_type = self.request.GET.get('content_type')
        if content_type:
            qs = qs.filter(content_type=content_type)
        return qs.select_related('author').order_by('-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['content_type_filter'] = self.request.GET.get('content_type', '')
        ctx['content_type_choices'] = ContentVersion.CONTENT_TYPE_CHOICES
        return ctx


class ContentVersionDetailView(LoginRequiredMixin, AuditLogMixin, DetailView):
    model = ContentVersion
    template_name = 'content/version_detail.html'
    context_object_name = 'version'


class PublishingQueueListView(LoginRequiredMixin, AuditLogMixin, ListView):
    model = PublishingQueue
    template_name = 'content/publishing_queue.html'
    context_object_name = 'queue_items'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs.select_related('created_by').order_by('-scheduled_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_filter'] = self.request.GET.get('status', '')
        ctx['pending_count'] = PublishingQueue.objects.filter(status='PENDING').count()
        ctx['published_count'] = PublishingQueue.objects.filter(status='PUBLISHED').count()
        ctx['failed_count'] = PublishingQueue.objects.filter(status='FAILED').count()
        return ctx


class PublishingQueueCreateView(LoginRequiredMixin, AuditLogMixin, CreateView):
    model = PublishingQueue
    form_class = PublishingQueueForm
    template_name = 'content/publishing_queue_form.html'
    success_url = reverse_lazy('content:publishing_queue')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        self.log_action(self.request.user, 'CONTENT_SCHEDULE', f"Scheduled publish: {form.instance.content_type}")
        return super().form_valid(form)


class PublishingQueueCancelView(LoginRequiredMixin, AuditLogMixin, TemplateView):
    def post(self, request, pk):
        queue = PublishingQueue.objects.filter(pk=pk).first()
        if queue and queue.status == 'PENDING':
            queue.status = 'CANCELLED'
            queue.save(update_fields=['status'])
            self.log_action(request.user, 'CONTENT_UNSCHEDULE', f"Cancelled: {queue.content_type}")
        return JsonResponse({'status': 'ok'})


class ContentHighlightListView(LoginRequiredMixin, AuditLogMixin, ListView):
    model = ContentHighlight
    template_name = 'content/highlight_list.html'
    context_object_name = 'highlights'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        highlight_type = self.request.GET.get('highlight_type')
        if highlight_type:
            qs = qs.filter(highlight_type=highlight_type)
        return qs.order_by('highlight_type', 'display_order')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['highlight_type_filter'] = self.request.GET.get('highlight_type', '')
        ctx['highlight_type_choices'] = ContentHighlight.HIGHLIGHT_TYPE_CHOICES
        return ctx


class ContentHighlightCreateView(LoginRequiredMixin, AuditLogMixin, CreateView):
    model = ContentHighlight
    form_class = ContentHighlightForm
    template_name = 'content/highlight_form.html'
    success_url = reverse_lazy('content:highlight_list')

    def form_valid(self, form):
        self.log_action(self.request.user, 'CONTENT_HIGHLIGHT_CREATE', f"Created highlight: {form.instance.highlight_type}")
        return super().form_valid(form)


class ContentHighlightUpdateView(LoginRequiredMixin, AuditLogMixin, UpdateView):
    model = ContentHighlight
    form_class = ContentHighlightForm
    template_name = 'content/highlight_form.html'
    success_url = reverse_lazy('content:highlight_list')

    def form_valid(self, form):
        self.log_action(self.request.user, 'CONTENT_HIGHLIGHT_UPDATE', f"Updated highlight: {form.instance.highlight_type}")
        return super().form_valid(form)


class ContentHighlightDeleteView(LoginRequiredMixin, AuditLogMixin, DeleteView):
    model = ContentHighlight
    template_name = 'content/highlight_confirm_delete.html'
    success_url = reverse_lazy('content:highlight_list')

    def form_valid(self, form):
        self.log_action(self.request.user, 'CONTENT_HIGHLIGHT_DELETE', f"Deleted highlight: {self.object.highlight_type}")
        return super().form_valid(form)


class GlobalSearchView(LoginRequiredMixin, TemplateView):
    template_name = 'content/search_results.html'

    def get(self, request, *args, **kwargs):
        if request.headers.get('HX-Request'):
            return self.render_to_response(self.get_context_data(**kwargs))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        content_type = self.request.GET.get('content_type', '')
        ctx['query'] = query
        ctx['content_type_filter'] = content_type
        ctx['results'] = []

        if query:
            from apps.news.models import Article
            from apps.podcast.models import Podcast, PodcastEpisode
            from apps.broadcast.models import Program, Episode

            articles = Article.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )[:5]

            podcasts = Podcast.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )[:5]

            programs = Program.objects.filter(
                Q(title__icontains=query) | Q(full_description__icontains=query)
            )[:5]

            ctx['results'] = [
                {'type': 'article', 'items': articles},
                {'type': 'podcast', 'items': podcasts},
                {'type': 'program', 'items': programs},
            ]

        return ctx


class ContentAuditLogView(LoginRequiredMixin, AuditLogMixin, ListView):
    model = ContentVersion
    template_name = 'content/audit_log.html'
    context_object_name = 'audit_entries'
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset()
        content_type = self.request.GET.get('content_type')
        if content_type:
            qs = qs.filter(content_type=content_type)
        return qs.select_related('author').order_by('-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['content_type_filter'] = self.request.GET.get('content_type', '')
        ctx['content_type_choices'] = ContentVersion.CONTENT_TYPE_CHOICES
        return ctx
