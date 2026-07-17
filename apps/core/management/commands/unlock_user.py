from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Buka kunci akun pengguna yang terkunci'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='?', type=str, help='Username pengguna yang akan dibuka kuncinya')
        parser.add_argument('--unlock-all', action='store_true', help='Buka kunci semua akun yang terkunci')

    def handle(self, *args, **options):
        from django.db.models import Q
        from apps.users.models import User

        username = options['username']
        unlock_all = options['unlock_all']

        if unlock_all:
            users = User.objects.filter(
                Q(account_status='LOCKED') | Q(is_active=False)
            )
            count = users.count()

            if count == 0:
                self.stdout.write(self.style.WARNING('Tidak ada akun yang terkunci ditemukan.'))
                return

            for user in users:
                user.is_active = True
                user.account_status = 'ACTIVE'
                user.failed_login_attempts = 0
                user.account_locked_until = None
                user.save(update_fields=[
                    'is_active', 'account_status',
                    'failed_login_attempts', 'account_locked_until',
                ])

            self.stdout.write(self.style.SUCCESS(
                f'{count} akun berhasil dibuka kuncinya.'
            ))
        else:
            if not username:
                self.stdout.write(self.style.ERROR(
                    'Harap masukkan username atau gunakan flag --unlock-all.'
                ))
                return

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User "{username}" tidak ditemukan.'))
                return

            user.is_active = True
            user.account_status = 'ACTIVE'
            user.failed_login_attempts = 0
            user.account_locked_until = None
            user.save(update_fields=[
                'is_active', 'account_status',
                'failed_login_attempts', 'account_locked_until',
            ])

            self.stdout.write(self.style.SUCCESS(
                f'Akun "{username}" berhasil dibuka kuncinya.'
            ))
