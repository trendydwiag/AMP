from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Perbaiki dan sinkronkan permission pengguna'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='', help='Username user spesifik yang akan diperiksa')
        parser.add_argument('--dry-run', action='store_true', help='Tampilkan perubahan tanpa menerapkannya')

    def handle(self, *args, **options):
        from apps.users.models import User
        from utils.choices import UserRole, AccountStatus

        username = options['username']
        dry_run = options['dry_run']

        if username:
            try:
                users = [User.objects.get(username=username)]
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User "{username}" tidak ditemukan.'))
                return
        else:
            users = list(User.objects.all())

        if not users:
            self.stdout.write(self.style.WARNING('Tidak ada user ditemukan.'))
            return

        issues = []

        for user in users:
            user_issues = []

            if user.role == UserRole.SUPERUSER:
                if not user.is_superuser:
                    user_issues.append('is_superuser seharusnya True')
                if not user.is_staff:
                    user_issues.append('is_staff seharusnya True')

            if user.role == UserRole.ADMINISTRATOR:
                if not user.is_staff:
                    user_issues.append('is_staff seharusnya True')

            if not user.is_active and user.account_status == AccountStatus.ACTIVE:
                user_issues.append('account_status seharusnya SUSPENDED (akun tidak aktif)')

            if user.failed_login_attempts < 0:
                user_issues.append(f'failed_login_attempts negatif ({user.failed_login_attempts})')

            if user_issues:
                issues.append((user, user_issues))

        if not issues:
            self.stdout.write(self.style.SUCCESS('Semua permission sudah sinkron. Tidak ada masalah ditemukan.'))
            return

        self.stdout.write(f'Ditemukan {len(issues)} user dengan masalah:\n')

        fixed = 0
        for user, user_issues in issues:
            self.stdout.write(f'  {user.username} ({user.role}):')
            for issue in user_issues:
                self.stdout.write(f'    - {issue}')

            if not dry_run:
                if user.role == UserRole.SUPERUSER:
                    user.is_superuser = True
                    user.is_staff = True

                if user.role == UserRole.ADMINISTRATOR:
                    user.is_staff = True

                if not user.is_active and user.account_status == AccountStatus.ACTIVE:
                    user.account_status = AccountStatus.SUSPENDED

                if user.failed_login_attempts < 0:
                    user.failed_login_attempts = 0

                user.save()
                fixed += 1

        if dry_run:
            self.stdout.write(self.style.WARNING(
                f'[DRY RUN] {len(issues)} user dengan masalah ditemukan. Tidak ada perubahan yang diterapkan.'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'{fixed} user berhasil diperbaiki.'
            ))
