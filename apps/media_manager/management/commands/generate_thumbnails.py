from django.core.management.base import BaseCommand
from apps.media_manager.models import MediaFile


class Command(BaseCommand):
    help = 'Generate ulang thumbnails untuk semua file gambar'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force', action='store_true',
            help='Generate ulang semua thumbnails termasuk yang sudah ada'
        )

    def handle(self, *args, **options):
        force = options['force']
        images = MediaFile.objects.filter(file_type='IMAGE')

        if not images.exists():
            self.stdout.write('Tidak ada file gambar ditemukan.')
            return

        generated = 0
        skipped = 0

        for image in images:
            if image.thumbnail and not force:
                skipped += 1
                continue

            try:
                from PIL import Image
                from django.conf import settings
                import os

                img_path = image.file.path
                if not os.path.exists(img_path):
                    self.stdout.write(self.style.WARNING(f'File tidak ditemukan: {img_path}'))
                    continue

                img = Image.open(img_path)
                img.thumbnail((300, 200), Image.Resampling.LANCZOS)

                thumb_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
                os.makedirs(thumb_dir, exist_ok=True)

                thumb_name = f'thumb_{image.pk}.jpg'
                thumb_path = os.path.join(thumb_dir, thumb_name)
                img.save(thumb_path, 'JPEG', quality=85)

                image.thumbnail.name = f'thumbnails/{thumb_name}'
                image.save(update_fields=['thumbnail'])
                generated += 1

            except ImportError:
                self.stdout.write(self.style.WARNING('Pillow tidak terinstall. Skip generate thumbnails.'))
                return
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Gagal generate thumbnail {image.title}: {e}'))

        self.stdout.write(self.style.SUCCESS(
            f'Thumbnails: {generated} dibuat, {skipped} dilewati (sudah ada).'
        ))
