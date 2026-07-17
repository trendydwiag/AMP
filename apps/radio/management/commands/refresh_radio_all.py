from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Refresh all radio data (now playing + listeners + health)'

    def handle(self, *args, **options):
        from apps.radio.services import NowPlayingService, ListenerService, StreamHealthService

        self.stdout.write('Refreshing now playing...')
        NowPlayingService().refresh_all()

        self.stdout.write('Refreshing listener stats...')
        ListenerService().refresh_all()

        self.stdout.write('Checking stream health...')
        StreamHealthService().refresh_all()

        self.stdout.write(self.style.SUCCESS('All radio data refreshed.'))
