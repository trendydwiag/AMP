import os
from django.db import models
from utils.services import BaseService
from .repositories import FolderRepository, TagRepository, MediaFileRepository
from .models import Folder, Tag, MediaFile


class FolderService(BaseService[FolderRepository]):
    def __init__(self):
        repo = FolderRepository()
        super().__init__(repo)

    def get_all_folders(self):
        return self.repository.get_all()

    def get_root_folders(self):
        return self.repository.get_root_folders()

    def get_folder_with_children(self, folder_id):
        folder = self.repository.get_by_id(folder_id)
        children = self.repository.get_children(folder_id)
        return folder, children

    def create_folder(self, name, parent_id=None, description='', created_by=None):
        folder = Folder(
            name=name, parent_id=parent_id,
            description=description, created_by=created_by
        )
        folder.save()
        return folder

    def update_folder(self, folder_id, **kwargs):
        folder = self.repository.get_by_id(folder_id)
        for key, value in kwargs.items():
            setattr(folder, key, value)
        folder.save()
        return folder

    def delete_folder(self, folder_id):
        folder = self.repository.get_by_id(folder_id)
        folder.delete()


class TagService(BaseService[TagRepository]):
    def __init__(self):
        repo = TagRepository()
        super().__init__(repo)

    def get_all_tags(self):
        return self.repository.get_all()

    def create_tag(self, name, color='#3B82F6'):
        tag = Tag(name=name, color=color)
        tag.save()
        return tag

    def update_tag(self, tag_id, **kwargs):
        tag = self.repository.get_by_id(tag_id)
        for key, value in kwargs.items():
            setattr(tag, key, value)
        tag.save()
        return tag

    def delete_tag(self, tag_id):
        tag = self.repository.get_by_id(tag_id)
        tag.delete()


class MediaFileService(BaseService[MediaFileRepository]):
    def __init__(self):
        repo = MediaFileRepository()
        super().__init__(repo)

    def get_all_files(self):
        return self.repository.get_all()

    def get_by_folder(self, folder_id=None):
        return self.repository.get_by_folder(folder_id)

    def get_by_type(self, file_type):
        return self.repository.get_by_type(file_type)

    def search_files(self, query):
        return self.repository.search(query)

    def get_file_detail(self, file_id):
        return self.repository.get_by_id(file_id)

    def upload_file(self, file_obj, title, user, folder_id=None, alt_text='', caption='', is_public=True, tag_ids=None):
        import mimetypes
        from django.utils.text import slugify

        original_filename = file_obj.name
        ext = os.path.splitext(original_filename)[1].lower()
        mime_type = mimetypes.guess_type(original_filename)[0] or 'application/octet-stream'

        file_type = self._detect_file_type(mime_type, ext)

        media = MediaFile(
            title=title,
            file=file_obj,
            original_filename=original_filename,
            file_type=file_type,
            mime_type=mime_type,
            file_size=file_obj.size,
            alt_text=alt_text,
            caption=caption,
            folder_id=folder_id,
            uploaded_by=user,
            is_public=is_public,
        )
        media.save()

        if tag_ids:
            media.tags.set(tag_ids)

        return media

    def update_file(self, file_id, **kwargs):
        media = self.repository.get_by_id(file_id)
        tag_ids = kwargs.pop('tag_ids', None)
        for key, value in kwargs.items():
            setattr(media, key, value)
        media.save()
        if tag_ids is not None:
            media.tags.set(tag_ids)
        return media

    def delete_file(self, file_id):
        media = self.repository.get_by_id(file_id)
        if media.file:
            media.file.delete(save=False)
        if media.thumbnail:
            media.thumbnail.delete(save=False)
        media.delete()

    def bulk_delete(self, file_ids):
        for file_id in file_ids:
            self.delete_file(file_id)

    def _detect_file_type(self, mime_type, ext):
        if mime_type and mime_type.startswith('image/'):
            return 'IMAGE'
        if mime_type and mime_type.startswith('video/'):
            return 'VIDEO'
        if mime_type and mime_type.startswith('audio/'):
            return 'AUDIO'
        doc_exts = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.csv']
        if ext in doc_exts:
            return 'DOCUMENT'
        return 'OTHER'

    def get_stats(self):
        from django.db.models import Sum, Count
        total_files = MediaFile.objects.count()
        total_size = MediaFile.objects.aggregate(total=Sum('file_size'))['total'] or 0
        by_type = MediaFile.objects.values('file_type').annotate(count=Count('id'))
        return {
            'total_files': total_files,
            'total_size': total_size,
            'by_type': {item['file_type']: item['count'] for item in by_type},
        }
