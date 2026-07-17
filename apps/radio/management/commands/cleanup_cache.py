from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Cleanup old radio cache and statistics data'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=30, help='Delete data older than N days')
        parser.add_argument('--dry-run', action='store_true', help='Preview without deleting')

    def handle(self, *args, **options):
        from django.utils import timezone
        from datetime import timedelta
        from apps.radio.models import ListenerStatistic, StreamHealth

        days = options['days']
        dry_run = options['dry_run']
        cutoff = timezone.now() - timedelta(days=days)

        listener_count = ListenerStatistic.objects.filter(recorded_at__lt=cutoff).count()
        health_count = StreamHealth.objects.filter(last_checked__lt=cutoff).count()

        if dry_run:
            self.stdout.write(f'[DRY RUN] {listener_count} listener stats, {health_count} health checks to delete')
        else:
            ListenerStatistic.objects.filter(recorded_at__lt=cutoff).delete()
            StreamHealth.objects.filter(last_checked__lt=cutoff).delete()
            self.stdout.write(self.style.SUCCESS(
                f'Cleaned up {listener_count} listener stats, {health_count} health checks older than {days} days'
            ))
