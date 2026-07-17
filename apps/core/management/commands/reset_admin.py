import os

import getpass

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Reset password admin default'

    def handle(self, *args, **options):
        from apps.users.models import User
        from utils.choices import UserRole

        username = os.environ.get('DJANGO_ADMIN_USERNAME', 'admin')
        password = os.environ.get('DJANGO_ADMIN_PASSWORD')
        email = os.environ.get('DJANGO_ADMIN_EMAIL', 'admin@kabulhaden.com')

        if not password:
            password = getpass.getpass('Masukkan password baru: ')
            confirm = getpass.getpass('Konfirmasi password: ')
            if password != confirm:
                self.stdout.write(self.style.ERROR('Password tidak cocok.'))
                return

        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(
                f'Password untuk user "{username}" berhasil direset.'
            ))
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=UserRole.ADMINISTRATOR,
            )
            self.stdout.write(self.style.SUCCESS(
                f'User admin "{username}" berhasil dibuat dengan role ADMINISTRATOR.'
            ))
