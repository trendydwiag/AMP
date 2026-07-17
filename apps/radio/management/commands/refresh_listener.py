from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Refresh listener statistics for all active stations'

    def add_arguments(self, parser):
        parser.add_argument('--station', type=str, help='Station UUID')

    def handle(self, *args, **options):
        from apps.radio.services import ListenerService
        svc = ListenerService()

        station_id = options.get('station')
        if station_id:
            stat = svc.refresh_from_provider(station_id)
            if stat:
                self.stdout.write(self.style.SUCCESS(
                    f'{stat.station.station_name}: {stat.current_listeners} listeners'
                ))
            else:
                self.stdout.write(self.style.WARNING(f'Station {station_id}: No data'))
        else:
            svc.refresh_all()
            self.stdout.write(self.style.SUCCESS('All stations listener data refreshed.'))
