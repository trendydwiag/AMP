from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from apps.users.decorators import admin_required
from .models import Folder, Tag, MediaFile
from .forms import FolderForm, TagForm, MediaFileUploadForm, MediaFileEditForm, MediaSearchForm
from .services import FolderService, TagService, MediaFileService


class MediaBaseView(TemplateView):
    template_name = 'media_manager/base.html'


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class MediaDashboardView(TemplateView):
    template_name = 'media_manager/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = MediaFileService()
        context['stats'] = service.get_stats()
        context['recent_files'] = MediaFile.objects.all()[:12]
        context['folders'] = Folder.objects.filter(parent__isnull=True)
        context['tags'] = Tag.objects.all()
        context['search_form'] = MediaSearchForm()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class MediaListView(ListView):
    model = MediaFile
    template_name = 'media_manager/list.html'
    context_object_name = 'files'
    paginate_by = 24

    def get_queryset(self):
        qs = MediaFile.objects.all()
        folder_id = self.request.GET.get('folder')
        file_type = self.request.GET.get('type')
        query = self.request.GET.get('q')
        if folder_id:
            qs = qs.filter(folder_id=folder_id)
        if file_type:
            qs = qs.filter(file_type=file_type)
        if query:
            from django.db.models import Q
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(original_filename__icontains=query) |
                Q(alt_text__icontains=query)
            )
        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = MediaSearchForm(self.request.GET)
        context['current_folder'] = self.request.GET.get('folder')
        context['current_type'] = self.request.GET.get('type')
        context['folders'] = Folder.objects.filter(parent__isnull=True)
        context['tags'] = Tag.objects.all()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class MediaUploadView(TemplateView):
    template_name = 'media_manager/upload.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upload_form'] = MediaFileUploadForm()
        context['folders'] = Folder.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        service = MediaFileService()
        files = request.FILES.getlist('files')
        folder_id = request.POST.get('folder') or None
        is_public = request.POST.get('is_public') == 'on'

        if not files:
            messages.error(request, 'Tidak ada file yang dipilih.')
            return redirect('media_manager:upload')

        uploaded_count = 0
        for f in files:
            try:
                service.upload_file(
                    file_obj=f,
                    title=f.name,
                    user=request.user,
                    folder_id=folder_id,
                    is_public=is_public
                )
                uploaded_count += 1
            except Exception as e:
                messages.warning(request, f'Gagal upload {f.name}: {str(e)}')

        if uploaded_count > 0:
            messages.success(request, f'{uploaded_count} file berhasil diupload.')
        return redirect('media_manager:list')


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class MediaDetailView(TemplateView):
    template_name = 'media_manager/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        media = get_object_or_404(MediaFile, pk=kwargs['pk'])
        context['media'] = media
        context['edit_form'] = MediaFileEditForm(instance=media)
        context['tags'] = Tag.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        media = get_object_or_404(MediaFile, pk=kwargs['pk'])
        form = MediaFileEditForm(request.POST, instance=media)
        if form.is_valid():
            form.save()
            messages.success(request, 'File media berhasil diperbarui.')
            return redirect('media_manager:detail', pk=media.pk)
        context = self.get_context_data(**kwargs)
        context['edit_form'] = form
        return self.render_to_response(context)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class MediaDeleteView(TemplateView):
    template_name = 'media_manager/delete_confirm.html'

    def post(self, request, *args, **kwargs):
        service = MediaFileService()
        service.delete_file(kwargs['pk'])
        messages.success(request, 'File media berhasil dihapus.')
        return redirect('media_manager:list')


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class MediaBulkDeleteView(TemplateView):
    def post(self, request, *args, **kwargs):
        file_ids = request.POST.getlist('file_ids')
        if file_ids:
            service = MediaFileService()
            service.bulk_delete(file_ids)
            messages.success(request, f'{len(file_ids)} file berhasil dihapus.')
        return redirect('media_manager:list')


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class FolderCreateView(TemplateView):
    template_name = 'media_manager/folder_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FolderForm()
        context['folders'] = Folder.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = FolderForm(request.POST)
        if form.is_valid():
            service = FolderService()
            service.create_folder(
                name=form.cleaned_data['name'],
                parent_id=form.cleaned_data.get('parent_id'),
                description=form.cleaned_data.get('description', ''),
                created_by=request.user
            )
            messages.success(request, 'Folder berhasil dibuat.')
            return redirect('media_manager:folders')
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class FolderDeleteView(TemplateView):
    def post(self, request, *args, **kwargs):
        service = FolderService()
        service.delete_folder(kwargs['pk'])
        messages.success(request, 'Folder berhasil dihapus.')
        return redirect('media_manager:folders')


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class TagCreateView(TemplateView):
    template_name = 'media_manager/tag_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TagForm()
        context['tags'] = Tag.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = TagForm(request.POST)
        if form.is_valid():
            service = TagService()
            service.create_tag(
                name=form.cleaned_data['name'],
                color=form.cleaned_data.get('color', '#3B82F6')
            )
            messages.success(request, 'Tag berhasil dibuat.')
            return redirect('media_manager:tags')
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class TagDeleteView(TemplateView):
    def post(self, request, *args, **kwargs):
        service = TagService()
        service.delete_tag(kwargs['pk'])
        messages.success(request, 'Tag berhasil dihapus.')
        return redirect('media_manager:tags')


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class MediaSearchAPIView(TemplateView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        file_type = request.GET.get('type', '')
        folder_id = request.GET.get('folder', '')

        qs = MediaFile.objects.all()
        if query:
            from django.db.models import Q
            qs = qs.filter(Q(title__icontains=query) | Q(original_filename__icontains=query))
        if file_type:
            qs = qs.filter(file_type=file_type)
        if folder_id:
            qs = qs.filter(folder_id=folder_id)

        files = qs[:24]
        data = [{
            'id': str(f.pk),
            'title': f.title,
            'file_url': f.file.url if f.file else '',
            'thumbnail_url': f.thumbnail.url if f.thumbnail else (f.file.url if f.is_image and f.file else ''),
            'file_type': f.file_type,
            'formatted_size': f.formatted_size,
            'type_badge_color': f.type_badge_color,
        } for f in files]
        return JsonResponse({'files': data})


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class FoldersView(TemplateView):
    template_name = 'media_manager/folders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['folders'] = Folder.objects.filter(parent__isnull=True)
        context['all_folders'] = Folder.objects.all()
        context['form'] = FolderForm()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class TagsView(TemplateView):
    template_name = 'media_manager/tags.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['form'] = TagForm()
        return context
