import io
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.media_manager.models import Folder, Tag, MediaFile
from apps.media_manager.services import FolderService, TagService, MediaFileService
from apps.media_manager.validators import validate_media_file
from apps.users.models import User


class FolderModelTest(TestCase):
    def test_create_folder(self):
        f = Folder.objects.create(name='Test Folder')
        self.assertEqual(f.name, 'Test Folder')
        self.assertTrue(f.slug)

    def test_folder_str(self):
        f = Folder.objects.create(name='My Folder')
        self.assertEqual(str(f), 'My Folder')

    def test_folder_full_path(self):
        parent = Folder.objects.create(name='Parent')
        child = Folder.objects.create(name='Child', parent=parent)
        self.assertEqual(child.full_path, 'Parent / Child')

    def test_folder_file_count(self):
        f = Folder.objects.create(name='Test')
        self.assertEqual(f.file_count, 0)

    def test_folder_unique_name_per_parent(self):
        parent = Folder.objects.create(name='Parent')
        Folder.objects.create(name='Child', parent=parent)
        with self.assertRaises(Exception):
            Folder.objects.create(name='Child', parent=parent)


class TagModelTest(TestCase):
    def test_create_tag(self):
        t = Tag.objects.create(name='Nature')
        self.assertEqual(t.name, 'Nature')
        self.assertEqual(t.slug, 'nature')

    def test_tag_str(self):
        t = Tag.objects.create(name='Photo')
        self.assertEqual(str(t), 'Photo')


class MediaFileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='uploader', email='up@test.com', password='TestPass123!'
        )

    def test_create_media_file(self):
        f = SimpleUploadedFile("test.txt", b"hello", content_type="text/plain")
        m = MediaFile.objects.create(
            title='Test File', file=f, original_filename='test.txt',
            file_type='OTHER', file_size=5, uploaded_by=self.user
        )
        self.assertEqual(m.title, 'Test File')
        self.assertTrue(m.pk)

    def test_formatted_size(self):
        m = MediaFile(title='t', original_filename='t.txt', file_type='OTHER', file_size=1048576)
        self.assertIn('MB', m.formatted_size)

    def test_file_type_properties(self):
        m = MediaFile(title='t', original_filename='t.jpg', file_type='IMAGE')
        self.assertTrue(m.is_image)
        self.assertFalse(m.is_video)

    def test_type_badge_color(self):
        m = MediaFile(title='t', original_filename='t.jpg', file_type='IMAGE')
        self.assertIn('green', m.type_badge_color)


class FolderServiceTest(TestCase):
    def test_create_and_get(self):
        svc = FolderService()
        f = svc.create_folder('Svc Folder')
        self.assertEqual(f.name, 'Svc Folder')
        self.assertIsNotNone(f.pk)

    def test_delete_folder(self):
        svc = FolderService()
        f = svc.create_folder('To Delete')
        pk = f.pk
        svc.delete_folder(pk)
        self.assertFalse(Folder.objects.filter(pk=pk).exists())


class TagServiceTest(TestCase):
    def test_create_tag(self):
        svc = TagService()
        t = svc.create_tag('TestTag', color='#FF0000')
        self.assertEqual(t.name, 'TestTag')

    def test_delete_tag(self):
        svc = TagService()
        t = svc.create_tag('DelTag')
        svc.delete_tag(t.pk)
        self.assertFalse(Tag.objects.filter(pk=t.pk).exists())


class MediaFileServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='svcuser', email='svc@test.com', password='TestPass123!'
        )

    def test_upload_file(self):
        svc = MediaFileService()
        f = SimpleUploadedFile("upload.txt", b"content", content_type="text/plain")
        m = svc.upload_file(f, 'Upload Test', self.user)
        self.assertEqual(m.title, 'Upload Test')
        self.assertIn(m.file_type, ['DOCUMENT', 'OTHER'])

    def test_detect_image_type(self):
        svc = MediaFileService()
        self.assertEqual(svc._detect_file_type('image/png', '.png'), 'IMAGE')

    def test_detect_video_type(self):
        svc = MediaFileService()
        self.assertEqual(svc._detect_file_type('video/mp4', '.mp4'), 'VIDEO')

    def test_delete_file(self):
        svc = MediaFileService()
        f = SimpleUploadedFile("del.txt", b"x", content_type="text/plain")
        m = svc.upload_file(f, 'Del', self.user)
        pk = m.pk
        svc.delete_file(pk)
        self.assertFalse(MediaFile.objects.filter(pk=pk).exists())

    def test_get_stats(self):
        svc = MediaFileService()
        stats = svc.get_stats()
        self.assertIn('total_files', stats)
        self.assertIn('total_size', stats)


class MediaFormsTest(TestCase):
    def test_validate_valid_file(self):
        f = SimpleUploadedFile("ok.txt", b"hello", content_type="text/plain")
        self.assertTrue(validate_media_file(f))

    def test_validate_invalid_extension(self):
        f = SimpleUploadedFile("bad.exe", b"x", content_type="application/exe")
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            validate_media_file(f)

    def test_validate_oversized_file(self):
        f = SimpleUploadedFile("big.txt", b"x" * (11 * 1024 * 1024), content_type="text/plain")
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            validate_media_file(f, max_size_mb=10)


class MediaViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin', email='admin@test.com', password='TestPass123!'
        )
        self.user = User.objects.create_user(
            username='user1', email='u1@test.com', password='TestPass123!'
        )

    @override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
    def test_dashboard_requires_admin(self):
        self.client.login(username='user1', password='TestPass123!')
        resp = self.client.get(reverse('media_manager:dashboard'))
        self.assertIn(resp.status_code, [302, 403])

    @override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
    def test_admin_can_access_dashboard(self):
        self.client.login(username='admin', password='TestPass123!')
        resp = self.client.get(reverse('media_manager:dashboard'))
        self.assertEqual(resp.status_code, 200)

    @override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
    def test_list_view(self):
        self.client.login(username='admin', password='TestPass123!')
        resp = self.client.get(reverse('media_manager:list'))
        self.assertEqual(resp.status_code, 200)

    @override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
    def test_upload_view_get(self):
        self.client.login(username='admin', password='TestPass123!')
        resp = self.client.get(reverse('media_manager:upload'))
        self.assertEqual(resp.status_code, 200)

    @override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
    def test_upload_view_post(self):
        self.client.login(username='admin', password='TestPass123!')
        f = SimpleUploadedFile("test.txt", b"content", content_type="text/plain")
        resp = self.client.post(reverse('media_manager:upload'), {
            'files': f,
            'is_public': 'on',
        })
        self.assertIn(resp.status_code, [200, 302])

    @override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
    def test_folders_view(self):
        self.client.login(username='admin', password='TestPass123!')
        resp = self.client.get(reverse('media_manager:folders'))
        self.assertEqual(resp.status_code, 200)

    @override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
    def test_tags_view(self):
        self.client.login(username='admin', password='TestPass123!')
        resp = self.client.get(reverse('media_manager:tags'))
        self.assertEqual(resp.status_code, 200)

    @override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
    def test_search_api(self):
        self.client.login(username='admin', password='TestPass123!')
        resp = self.client.get(reverse('media_manager:api_search'), {'q': 'test'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('files', resp.json())
