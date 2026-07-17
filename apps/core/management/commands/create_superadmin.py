import os

import getpass

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Buat akun super administrator baru'

    def handle(self, *args, **options):
        from apps.users.models import User
        from utils.choices import UserRole

        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username:
            username = input('Username: ')
        if not email:
            email = input('Email: ')
        if not password:
            password = getpass.getpass('Password: ')
            confirm = getpass.getpass('Konfirmasi password: ')
            if password != confirm:
                self.stdout.write(self.style.ERROR('Password tidak cocok.'))
                return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(
                f'Username "{username}" sudah digunakan.'
            ))
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(
                f'Email "{email}" sudah digunakan.'
            ))
            return

        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                role=UserRole.SUPERUSER,
            )
            self.stdout.write(self.style.SUCCESS(
                f'Super administrator "{user.username}" berhasil dibuat.'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Gagal membuat super administrator: {e}'))
