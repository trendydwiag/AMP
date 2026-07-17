import logging
from typing import Optional
from django.db import transaction
from django.utils import timezone

from .models import Partner, PartnerMembership, PartnerDomain

logger = logging.getLogger('platform')


class PartnerService:
    """Business logic for Partner CRUD, configuration loading, and partner switching."""

    def get_active_partners(self):
        """Return all active, non-deleted partners."""
        return Partner.objects.filter(status='ACTIVE', is_deleted=False).order_by('name')

    def get_all_partners(self, include_deleted=False):
        """Return all partners, optionally including soft-deleted."""
        qs = Partner.all_objects.all().order_by('name') if include_deleted else Partner.objects.all()
        return qs.order_by('name')

    def get_partner_by_slug(self, slug: str) -> Optional[Partner]:
        """Resolve partner by slug."""
        return Partner.objects.filter(slug=slug, is_deleted=False).first()

    def get_partner_by_pk(self, pk) -> Optional[Partner]:
        """Resolve partner by UUID pk."""
        return Partner.objects.filter(pk=pk, is_deleted=False).first()

    def get_or_create_default_partner(self) -> Partner:
        """Get or create the default platform partner."""
        from django.conf import settings
        default_slug = getattr(settings, 'PLATFORM_DEFAULT_PARTNER_SLUG', 'kabulhaden-online')
        default_name = getattr(settings, 'PLATFORM_DEFAULT_PARTNER_NAME', 'Kabulhaden Online')

        partner, created = Partner.objects.get_or_create(
            slug=default_slug,
            defaults={
                'name': default_name,
                'status': 'ACTIVE',
                'tier': 'PROFESSIONAL',
                'company_name': 'Kabulhaden Online',
                'primary_domain': 'kabulhaden.com',
                'primary_color': '#4E2F1F',
                'secondary_color': '#FAF7F3',
                'accent_color': '#8B5E3C',
                'tagline': 'Media Radio & Podcast Digital',
                'description': 'Kabulhaden Online adalah media radio dan podcast digital yang menyajikan konten berkualitas.',
                'contact_email': 'info@kabulhaden.com',
                'timezone': 'Asia/Jakarta',
                'language': 'id',
                'max_users': 50,
                'max_storage_mb': 51200,
                'max_articles': 5000,
                'max_podcasts': 100,
                'max_episodes': 5000,
                'feature_overrides': {
                    'podcast': True,
                    'article': True,
                    'ads': True,
                    'community': True,
                    'analytics': True,
                    'sponsor': True,
                    'media_library': True,
                    'api': True,
                    'themes': True,
                    'plugins': True,
                },
                'provider_overrides': {
                    'STREAMING': 'icecast',
                    'STORAGE': 'local',
                    'EMAIL': 'django',
                },
            }
        )
        if created:
            logger.info(f"Default partner created: {partner.name} ({partner.slug})")
        return partner

    @transaction.atomic
    def create_partner(self, data: dict, created_by=None) -> Partner:
        """Create a new partner with optional creator membership."""
        partner = Partner.objects.create(
            name=data['name'],
            slug=data.get('slug', ''),
            company_name=data.get('company_name', ''),
            tier=data.get('tier', 'COMMUNITY'),
            primary_domain=data.get('primary_domain', ''),
            primary_color=data.get('primary_color', '#4E2F1F'),
            secondary_color=data.get('secondary_color', '#FAF7F3'),
            accent_color=data.get('accent_color', '#8B5E3C'),
            tagline=data.get('tagline', ''),
            description=data.get('description', ''),
            contact_email=data.get('contact_email', ''),
            contact_phone=data.get('contact_phone', ''),
            contact_website=data.get('contact_website', ''),
            timezone=data.get('timezone', 'Asia/Jakarta'),
            language=data.get('language', 'id'),
            max_users=data.get('max_users', 5),
            max_storage_mb=data.get('max_storage_mb', 1024),
            max_articles=data.get('max_articles', 100),
            max_podcasts=data.get('max_podcasts', 10),
            max_episodes=data.get('max_episodes', 50),
            owner=created_by,
        )

        if created_by:
            PartnerMembership.objects.create(
                user=created_by,
                partner=partner,
                role='OWNER',
                is_active=True,
            )

        # Create default domain entry if primary_domain is set
        if partner.primary_domain:
            PartnerDomain.objects.create(
                partner=partner,
                domain=partner.primary_domain,
                is_primary=True,
                is_verified=False,
            )

        logger.info(f"Partner created: {partner.name} ({partner.slug}) by {created_by}")
        return partner

    @transaction.atomic
    def update_partner(self, partner: Partner, data: dict, changed_by=None) -> Partner:
        """Update partner fields."""
        updatable_fields = [
            'name', 'company_name', 'tier', 'status',
            'primary_domain', 'primary_color', 'secondary_color', 'accent_color',
            'tagline', 'description',
            'contact_email', 'contact_phone', 'contact_website',
            'timezone', 'language', 'locale',
            'max_users', 'max_storage_mb', 'max_articles', 'max_podcasts', 'max_episodes',
            'feature_overrides', 'provider_overrides',
            'logo', 'favicon',
            'storage_provider', 'streaming_provider', 'smtp_provider',
        ]

        for field in updatable_fields:
            if field in data:
                setattr(partner, field, data[field])

        partner.save()
        logger.info(f"Partner updated: {partner.name} by {changed_by}")
        return partner

    def switch_partner(self, request, partner: Partner) -> bool:
        """Switch the active partner in the user's session.

        Only ADMINISTRATOR and SUPERUSER roles can switch partners.
        """
        user = request.user
        if not user.is_authenticated:
            return False

        # Check role permission
        if not hasattr(user, 'role') or user.role not in ('SUPERUSER', 'ADMINISTRATOR'):
            logger.warning(f"User {user.username} attempted unauthorized partner switch")
            return False

        # Check user has membership in target partner
        has_membership = PartnerMembership.objects.filter(
            user=user,
            partner=partner,
            is_active=True,
        ).exists()

        # Superuser can switch to any active partner
        if user.role == 'SUPERUSER':
            has_membership = True

        if not has_membership:
            logger.warning(f"User {user.username} has no membership in partner {partner.name}")
            return False

        # Store in session
        request.session['_current_partner_id'] = str(partner.pk)
        if hasattr(request.session, 'modified'):
            request.session.modified = True

        # Update partner context on request
        from .context import PartnerContext
        ctx = PartnerContext(
            partner=partner,
            resolution_method='session',
            resolved_domain=partner.primary_domain,
            is_default=False,
        )
        request.partner_context = ctx

        logger.info(f"Partner switched to: {partner.name} by {user.username}")
        return True

    def load_partner_config(self, partner: Partner) -> dict:
        """Load full partner configuration including feature overrides and provider overrides.

        Returns a merged config dict suitable for use in views and templates.
        """
        config = {
            'partner_id': str(partner.pk),
            'partner_slug': partner.slug,
            'partner_name': partner.name,
            'company_name': partner.company_name,
            'tier': partner.tier,
            'status': partner.status,
            'timezone': partner.timezone,
            'language': partner.language,
            'locale': partner.locale,
            'branding': {
                'primary_color': partner.primary_color,
                'secondary_color': partner.secondary_color,
                'accent_color': partner.accent_color,
                'logo_url': partner.logo.url if partner.logo else '',
                'favicon_url': partner.favicon.url if partner.favicon else '',
                'tagline': partner.tagline,
            },
            'limits': {
                'max_users': partner.max_users,
                'max_storage_mb': partner.max_storage_mb,
                'max_articles': partner.max_articles,
                'max_podcasts': partner.max_podcasts,
                'max_episodes': partner.max_episodes,
            },
            'providers': {
                'storage': partner.storage_provider or partner.get_provider('STORAGE'),
                'streaming': partner.streaming_provider or partner.get_provider('STREAMING'),
                'email': partner.smtp_provider or partner.get_provider('EMAIL'),
            },
            'features': partner.feature_overrides,
            'domains': partner.get_all_domains(),
        }
        return config

    def get_partner_members(self, partner: Partner):
        """Return active memberships for a partner."""
        return PartnerMembership.objects.filter(
            partner=partner, is_active=True
        ).select_related('user').order_by('-role', 'user__username')

    def get_user_partners(self, user):
        """Return all active partners a user belongs to."""
        memberships = PartnerMembership.objects.filter(
            user=user, is_active=True, partner__is_deleted=False
        ).select_related('partner').order_by('partner__name')
        return [m.partner for m in memberships]

    def add_member(self, partner: Partner, user, role: str = 'VIEWER') -> PartnerMembership:
        """Add a user as member of a partner."""
        membership, created = PartnerMembership.objects.get_or_create(
            user=user,
            partner=partner,
            defaults={'role': role, 'is_active': True},
        )
        if not created:
            membership.role = role
            membership.is_active = True
            membership.save(update_fields=['role', 'is_active', 'updated_at'])
        return membership

    def remove_member(self, partner: Partner, user) -> bool:
        """Deactivate a user's membership in a partner."""
        try:
            membership = PartnerMembership.objects.get(user=user, partner=partner)
            membership.is_active = False
            membership.save(update_fields=['is_active', 'updated_at'])
            return True
        except PartnerMembership.DoesNotExist:
            return False
