from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Refresh now playing data for all active stations'

    def add_arguments(self, parser):
        parser.add_argument('--station', type=str, help='Station UUID to refresh specific station')

    def handle(self, *args, **options):
        from apps.radio.services import NowPlayingService
        svc = NowPlayingService()

        station_id = options.get('station')
        if station_id:
            np = svc.refresh_from_provider(station_id)
            if np:
                self.stdout.write(self.style.SUCCESS(
                    f'{np.station.station_name}: {np.artist} - {np.song_title} [{np.stream_status}]'
                ))
            else:
                self.stdout.write(self.style.WARNING(f'Station {station_id}: No data'))
        else:
            svc.refresh_all()
            self.stdout.write(self.style.SUCCESS('All stations refreshed.'))
