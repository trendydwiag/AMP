import logging
from django.core.management.base import BaseCommand
from django.db import transaction

logger = logging.getLogger('platform')


class Command(BaseCommand):
    help = 'Seed default partner (Kabulhaden Online) and all feature flags'

    def handle(self, *args, **options):
        self.stdout.write('Seeding platform data...')

        with transaction.atomic():
            partner = self._seed_partner()
            self._seed_feature_flags(partner)
            self._seed_domains(partner)

        self.stdout.write(self.style.SUCCESS('Platform data seeded successfully!'))

    def _seed_partner(self):
        from apps.platform.partner.service import PartnerService
        service = PartnerService()
        partner = service.get_or_create_default_partner()
        self.stdout.write(f'  Partner: {partner.name} ({partner.slug})')
        return partner

    def _seed_feature_flags(self, partner):
        from apps.platform.feature_flags.models import FeatureFlag, FeatureFlagPartner

        flags_config = [
            {
                'key': 'podcast',
                'name': 'Podcast',
                'description': 'Fitur podcast dan episode',
                'is_enabled': True,
                'category': 'Konten',
            },
            {
                'key': 'article',
                'name': 'Artikel',
                'description': 'Fitur artikel dan berita',
                'is_enabled': True,
                'category': 'Konten',
            },
            {
                'key': 'ads',
                'name': 'Iklan',
                'description': 'Sistem manajemen iklan',
                'is_enabled': True,
                'category': 'Monetisasi',
            },
            {
                'key': 'community',
                'name': 'Komunitas',
                'description': 'Fitur komunitas dan diskusi',
                'is_enabled': True,
                'category': 'Sosial',
            },
            {
                'key': 'analytics',
                'name': 'Analytics',
                'description': 'Dashboard analitik dan statistik',
                'is_enabled': True,
                'category': 'Insight',
            },
            {
                'key': 'sponsor',
                'name': 'Sponsor',
                'description': 'Manajemen sponsor dan mitra',
                'is_enabled': True,
                'category': 'Monetisasi',
            },
            {
                'key': 'media_library',
                'name': 'Media Library',
                'description': 'Perpustakaan media dan file',
                'is_enabled': True,
                'category': 'Konten',
            },
            {
                'key': 'api',
                'name': 'API Access',
                'description': 'Akses API untuk integrasi',
                'is_enabled': True,
                'category': 'Platform',
            },
            {
                'key': 'themes',
                'name': 'Themes',
                'description': 'Theme engine dan kustomisasi tampilan',
                'is_enabled': True,
                'category': 'Platform',
            },
            {
                'key': 'plugins',
                'name': 'Plugins',
                'description': 'Sistem plugin dan ekstensi',
                'is_enabled': True,
                'category': 'Platform',
            },
        ]

        created_count = 0
        for config in flags_config:
            flag, created = FeatureFlag.objects.get_or_create(
                key=config['key'],
                defaults={
                    'name': config['name'],
                    'description': config['description'],
                    'is_enabled': config['is_enabled'],
                    'category': config['category'],
                    'scope': 'GLOBAL',
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'  Feature Flag created: {flag.name} [{flag.key}]')

            # Enable for default partner
            if partner:
                FeatureFlagPartner.objects.get_or_create(
                    flag=flag,
                    partner=partner,
                    defaults={'is_enabled': True}
                )

        self.stdout.write(f'  Feature Flags: {created_count} created, {len(flags_config)} total')

    def _seed_domains(self, partner):
        from apps.platform.partner.models import PartnerDomain

        domains_to_create = [
            {
                'domain': partner.primary_domain,
                'is_primary': True,
                'is_verified': False,
            },
            {
                'domain': f'{partner.slug}.{partner.primary_domain}',
                'is_primary': False,
                'is_verified': False,
            },
        ]

        for domain_data in domains_to_create:
            if domain_data['domain']:
                obj, created = PartnerDomain.objects.get_or_create(
                    partner=partner,
                    domain=domain_data['domain'],
                    defaults={
                        'is_primary': domain_data['is_primary'],
                        'is_verified': domain_data['is_verified'],
                    }
                )
                if created:
                    self.stdout.write(f'  Domain created: {obj.domain}')
