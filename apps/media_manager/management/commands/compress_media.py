from django.core.management.base import BaseCommand
from apps.media_manager.models import MediaFile


class Command(BaseCommand):
    help = 'Kompresi gambar untuk menghemat storage'

    def add_arguments(self, parser):
        parser.add_argument(
            '--quality', type=int, default=85,
            help='Kualitas kompresi JPEG (1-100, default: 85)'
        )
        parser.add_argument(
            '--max-width', type=int, default=1920,
            help='Lebar maksimum dalam px (default: 1920)'
        )
        parser.add_argument(
            '--dry-run', action='store_true',
            help='Tampilkan tanpa mengubah'
        )

    def handle(self, *args, **options):
        quality = options['quality']
        max_width = options['max_width']
        dry_run = options['dry_run']

        images = MediaFile.objects.filter(file_type='IMAGE')

        if not images.exists():
            self.stdout.write('Tidak ada file gambar ditemukan.')
            return

        optimized = 0
        for image in images:
            try:
                from PIL import Image
                import os

                img_path = image.file.path
                if not os.path.exists(img_path):
                    continue

                original_size = os.path.getsize(img_path)
                img = Image.open(img_path)

                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

                if dry_run:
                    self.stdout.write(f'  {image.title}: {original_size / 1024:.0f}KB')
                    continue

                img.save(img_path, 'JPEG', quality=quality, optimize=True)
                new_size = os.path.getsize(img_path)
                image.file_size = new_size
                image.save(update_fields=['file_size'])
                optimized += 1

            except ImportError:
                self.stdout.write(self.style.WARNING('Pillow tidak terinstall.'))
                return
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Gagal kompresi {image.title}: {e}'))

        if not dry_run:
            self.stdout.write(self.style.SUCCESS(f'{optimized} gambar berhasil dikompresi.'))
