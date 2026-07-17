from utils.repositories import BaseRepository
from .models import Folder, Tag, MediaFile


class FolderRepository(BaseRepository):
    model = Folder

    def get_root_folders(self):
        return self.model.objects.filter(parent__isnull=True).order_by('name')

    def get_children(self, parent_id):
        return self.model.objects.filter(parent_id=parent_id).order_by('name')


class TagRepository(BaseRepository):
    model = Tag


class MediaFileRepository(BaseRepository):
    model = MediaFile

    def get_by_folder(self, folder_id=None):
        qs = self.model.objects.all()
        if folder_id:
            qs = qs.filter(folder_id=folder_id)
        else:
            qs = qs.filter(folder__isnull=True)
        return qs.order_by('-created_at')

    def get_by_type(self, file_type):
        return self.model.objects.filter(file_type=file_type).order_by('-created_at')

    def search(self, query):
        from django.db.models import Q
        return self.model.objects.filter(
            Q(title__icontains=query) |
            Q(original_filename__icontains=query) |
            Q(alt_text__icontains=query) |
            Q(caption__icontains=query)
        ).order_by('-created_at')

    def get_public_files(self):
        return self.model.objects.filter(is_public=True).order_by('-created_at')
