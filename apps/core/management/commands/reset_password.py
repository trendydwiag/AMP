import getpass

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Reset password pengguna'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username pengguna yang akan direset passwordnya')
        parser.add_argument('--password', type=str, default='', help='Password baru (jika tidak diisi, akan diminta secara interaktif)')
        parser.add_argument('--unlock', action='store_true', help='Buka kunci akun bersamaan dengan reset password')

    def handle(self, *args, **options):
        from apps.users.models import User

        username = options['username']
        password = options['password']
        unlock = options['unlock']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" tidak ditemukan.'))
            return

        if not password:
            password = getpass.getpass(f'Masukkan password baru untuk "{username}": ')
            confirm = getpass.getpass('Konfirmasi password: ')
            if password != confirm:
                self.stdout.write(self.style.ERROR('Password tidak cocok.'))
                return

        user.set_password(password)
        update_fields = ['password']

        if unlock:
            user.is_active = True
            user.account_status = 'ACTIVE'
            user.failed_login_attempts = 0
            user.account_locked_until = None
            update_fields.extend([
                'is_active', 'account_status',
                'failed_login_attempts', 'account_locked_until',
            ])

        user.save(update_fields=update_fields)

        msg = f'Password untuk user "{username}" berhasil direset.'
        if unlock:
            msg += ' Akun juga telah dibuka kuncinya.'
        self.stdout.write(self.style.SUCCESS(msg))
