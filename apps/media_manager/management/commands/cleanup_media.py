from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.media_manager.models import MediaFile


class Command(BaseCommand):
    help = 'Bersihkan file media orphans dan cache thumbnails lama'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days', type=int, default=30,
            help='Hapus file lebih tua dari N hari (default: 30)'
        )
        parser.add_argument(
            '--dry-run', action='store_true',
            help='Tampilkan file yang akan dihapus tanpa menghapus'
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        cutoff = timezone.now() - timedelta(days=days)

        orphans = MediaFile.objects.filter(
            created_at__lt=cutoff,
            file=''
        )

        count = orphans.count()
        if dry_run:
            self.stdout.write(f'[DRY RUN] {count} file orphans akan dihapus:')
            for media in orphans[:20]:
                self.stdout.write(f'  - {media.title} ({media.created_at})')
        else:
            for media in orphans:
                if media.thumbnail:
                    media.thumbnail.delete(save=False)
            deleted, _ = orphans.delete()
            self.stdout.write(self.style.SUCCESS(f'{deleted} file orphans berhasil dihapus.'))
