from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Check stream health for all active stations'

    def add_arguments(self, parser):
        parser.add_argument('--station', type=str, help='Station UUID')

    def handle(self, *args, **options):
        from apps.radio.services import StreamHealthService
        svc = StreamHealthService()

        station_id = options.get('station')
        if station_id:
            health = svc.refresh_from_provider(station_id)
            if health:
                self.stdout.write(self.style.SUCCESS(
                    f'{health.station.station_name}: {health.get_provider_status_display()} '
                    f'({health.response_time:.0f}ms, HTTP {health.http_status})'
                ))
            else:
                self.stdout.write(self.style.WARNING(f'Station {station_id}: No data'))
        else:
            svc.refresh_all()
            self.stdout.write(self.style.SUCCESS('All stations health checked.'))
