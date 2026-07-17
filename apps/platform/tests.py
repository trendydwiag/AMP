import uuid
from unittest.mock import patch, MagicMock

from django.test import TestCase, Client, RequestFactory, override_settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest, JsonResponse

from apps.platform.partner.models import Partner, PartnerMembership, PartnerDomain, PartnerInvitation
from apps.platform.partner.context import PartnerContext, get_partner_from_context
from apps.platform.partner.resolver import PartnerResolver
from apps.platform.partner.middleware import PartnerMiddleware
from apps.platform.partner.service import PartnerService
from apps.platform.feature_flags.models import FeatureFlag, FeatureFlagPartner, FeatureFlagLog
from apps.platform.feature_flags.service import FeatureFlagService
from apps.platform.domains.engine import DomainEngine
from apps.platform.security.tenant import TenantIsolation, AuditLogger, require_partner_access
from apps.platform.choices import PartnerStatus, PartnerTier, FeatureFlagScope

User = get_user_model()


class PartnerModelTestCase(TestCase):
    """Test Partner model fields, properties, and methods."""

    def setUp(self):
        self.partner = Partner.objects.create(
            name='Test Partner',
            slug='test-partner',
            status=PartnerStatus.ACTIVE,
            tier=PartnerTier.COMMUNITY,
            primary_domain='test.example.com',
            primary_color='#FF0000',
            company_name='Test Company',
        )

    def test_partner_creation(self):
        self.assertEqual(self.partner.name, 'Test Partner')
        self.assertEqual(self.partner.slug, 'test-partner')
        self.assertTrue(self.partner.is_active)

    def test_partner_is_active_with_soft_delete(self):
        self.assertTrue(self.partner.is_active)
        self.partner.soft_delete()
        self.assertFalse(self.partner.is_active)
        self.partner.restore()
        self.assertTrue(self.partner.is_active)

    def test_partner_has_feature(self):
        self.partner.feature_overrides = {'podcast': True, 'ads': False}
        self.partner.save()
        self.assertTrue(self.partner.has_feature('podcast'))
        self.assertFalse(self.partner.has_feature('ads'))
        self.assertFalse(self.partner.has_feature('unknown', default=False))
        self.assertTrue(self.partner.has_feature('unknown', default=True))

    def test_partner_get_provider(self):
        self.partner.provider_overrides = {'STREAMING': 'icecast'}
        self.partner.save()
        self.assertEqual(self.partner.get_provider('STREAMING'), 'icecast')
        self.assertIsNone(self.partner.get_provider('STORAGE'))

    def test_partner_get_all_domains(self):
        self.partner.custom_domains = ['custom1.com', 'custom2.com']
        self.partner.save()
        domains = self.partner.get_all_domains()
        self.assertIn('test.example.com', domains)
        self.assertIn('custom1.com', domains)
        self.assertIn('custom2.com', domains)

    def test_partner_slug_auto_generation(self):
        p = Partner.objects.create(name='Auto Slug Partner')
        self.assertEqual(p.slug, 'auto-slug-partner')

    def test_partner_soft_delete_restore(self):
        self.partner.soft_delete()
        self.assertTrue(self.partner.is_deleted)
        self.assertIsNotNone(self.partner.deleted_at)
        self.partner.restore()
        self.assertFalse(self.partner.is_deleted)
        self.assertIsNone(self.partner.deleted_at)

    def test_partner_manager_excludes_deleted(self):
        Partner.objects.create(name='Deleted Partner', slug='deleted-p', status=PartnerStatus.INACTIVE, is_deleted=True)
        self.assertEqual(Partner.objects.count(), 1)
        self.assertEqual(Partner.all_objects.count(), 2)

    def test_partner_storage_usage(self):
        # Storage usage with no media files
        self.assertEqual(self.partner.storage_used_mb, 0)


class PartnerMembershipTestCase(TestCase):
    """Test PartnerMembership model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='memberuser',
            email='member@test.com',
            password='TestPass123!',
        )
        self.partner = Partner.objects.create(
            name='Member Partner',
            slug='member-partner',
            status=PartnerStatus.ACTIVE,
        )
        self.membership = PartnerMembership.objects.create(
            user=self.user,
            partner=self.partner,
            role='EDITOR',
        )

    def test_membership_creation(self):
        self.assertEqual(self.membership.user, self.user)
        self.assertEqual(self.membership.partner, self.partner)
        self.assertEqual(self.membership.role, 'EDITOR')

    def test_membership_is_admin(self):
        self.assertFalse(self.membership.is_admin)
        self.membership.role = 'ADMINISTRATOR'
        self.assertTrue(self.membership.is_admin)
        self.membership.role = 'OWNER'
        self.assertTrue(self.membership.is_admin)

    def test_membership_is_owner(self):
        self.assertFalse(self.membership.is_owner)
        self.membership.role = 'OWNER'
        self.assertTrue(self.membership.is_owner)


class PartnerResolverTestCase(TestCase):
    """Test PartnerResolver's 5-layer resolution strategy."""

    def setUp(self):
        self.resolver = PartnerResolver()
        self.partner = Partner.objects.create(
            name='Resolver Test',
            slug='resolver-test',
            status=PartnerStatus.ACTIVE,
            primary_domain='resolve.example.com',
        )
        self.factory = RequestFactory()

    @override_settings(ALLOWED_HOSTS=['*'])
    def test_resolve_by_domain(self):
        request = self.factory.get('/', HTTP_HOST='resolve.example.com')
        request.session = {}
        partner = self.resolver.resolve(request)
        self.assertEqual(partner, self.partner)

    @override_settings(ALLOWED_HOSTS=['*'], PLATFORM_BASE_DOMAIN='example.com')
    def test_resolve_by_subdomain(self):
        request = self.factory.get('/', HTTP_HOST='resolver-test.example.com')
        request.session = {}
        partner = self.resolver.resolve(request)
        self.assertEqual(partner, self.partner)

    @override_settings(ALLOWED_HOSTS=['*'])
    def test_resolve_by_header_id(self):
        request = self.factory.get('/', HTTP_X_PARTNER_ID=str(self.partner.pk))
        request.session = {}
        partner = self.resolver.resolve(request)
        self.assertEqual(partner, self.partner)

    @override_settings(ALLOWED_HOSTS=['*'])
    def test_resolve_by_header_slug(self):
        request = self.factory.get('/', HTTP_X_PARTNER_SLUG='resolver-test')
        request.session = {}
        partner = self.resolver.resolve(request)
        self.assertEqual(partner, self.partner)

    @override_settings(ALLOWED_HOSTS=['*'])
    def test_resolve_by_session(self):
        request = self.factory.get('/')
        request.session = {'_current_partner_id': str(self.partner.pk)}
        partner = self.resolver.resolve(request)
        self.assertEqual(partner, self.partner)

    def test_resolve_from_domain(self):
        partner = self.resolver.resolve_from_domain('resolve.example.com')
        self.assertEqual(partner, self.partner)

    def test_resolve_from_slug(self):
        partner = self.resolver.resolve_from_slug('resolver-test')
        self.assertEqual(partner, self.partner)

    @override_settings(ALLOWED_HOSTS=['*'])
    def test_resolve_excludes_deleted(self):
        self.partner.soft_delete()
        request = self.factory.get('/', HTTP_HOST='resolve.example.com')
        request.session = {}
        partner = self.resolver.resolve(request)
        self.assertNotEqual(partner, self.partner)

    @override_settings(ALLOWED_HOSTS=['*'], PLATFORM_DEFAULT_PARTNER_SLUG='resolver-test')
    def test_resolve_default_partner(self):
        request = self.factory.get('/', HTTP_HOST='unknown.example.com')
        request.session = {}
        partner = self.resolver.resolve(request)
        self.assertEqual(partner, self.partner)


class PartnerServiceTestCase(TestCase):
    """Test PartnerService business logic."""

    def setUp(self):
        self.service = PartnerService()
        self.user = User.objects.create_user(
            username='serviceuser',
            email='service@test.com',
            password='TestPass123!',
            role='ADMINISTRATOR',
        )
        self.partner = Partner.objects.create(
            name='Service Test',
            slug='service-test',
            status=PartnerStatus.ACTIVE,
            primary_domain='service.example.com',
            company_name='Service Corp',
        )

    def test_get_active_partners(self):
        Partner.objects.create(name='Inactive', slug='inactive', status=PartnerStatus.INACTIVE)
        partners = self.service.get_active_partners()
        self.assertEqual(partners.count(), 1)
        self.assertEqual(partners.first(), self.partner)

    def test_get_partner_by_slug(self):
        found = self.service.get_partner_by_slug('service-test')
        self.assertEqual(found, self.partner)
        self.assertIsNone(self.service.get_partner_by_slug('nonexistent'))

    def test_get_partner_by_pk(self):
        found = self.service.get_partner_by_pk(self.partner.pk)
        self.assertEqual(found, self.partner)

    def test_create_partner(self):
        data = {
            'name': 'New Partner',
            'slug': 'new-partner',
            'company_name': 'New Corp',
            'tier': 'STARTER',
            'primary_domain': 'new.example.com',
        }
        partner = self.service.create_partner(data, created_by=self.user)
        self.assertEqual(partner.name, 'New Partner')
        self.assertEqual(partner.owner, self.user)
        # Check membership was created
        membership = PartnerMembership.objects.get(user=self.user, partner=partner)
        self.assertEqual(membership.role, 'OWNER')

    def test_update_partner(self):
        data = {'name': 'Updated Name', 'company_name': 'Updated Corp'}
        partner = self.service.update_partner(self.partner, data, changed_by=self.user)
        self.assertEqual(partner.name, 'Updated Name')
        self.assertEqual(partner.company_name, 'Updated Corp')

    def test_switch_partner(self):
        request = MagicMock()
        request.user = self.user
        session = {}
        request.session = session
        request.partner_context = PartnerContext()

        # Create membership
        PartnerMembership.objects.create(user=self.user, partner=self.partner, role='ADMINISTRATOR')

        result = self.service.switch_partner(request, self.partner)
        self.assertTrue(result)
        self.assertEqual(session['_current_partner_id'], str(self.partner.pk))

    def test_switch_partner_no_permission(self):
        viewer = User.objects.create_user(
            username='viewer', email='viewer@test.com', password='Pass123!',
        )
        request = MagicMock()
        request.user = viewer
        request.session = {}

        result = self.service.switch_partner(request, self.partner)
        self.assertFalse(result)

    def test_load_partner_config(self):
        config = self.service.load_partner_config(self.partner)
        self.assertEqual(config['partner_slug'], 'service-test')
        self.assertEqual(config['company_name'], 'Service Corp')
        self.assertIn('branding', config)
        self.assertIn('limits', config)
        self.assertIn('providers', config)
        self.assertIn('features', config)

    def test_get_user_partners(self):
        PartnerMembership.objects.create(user=self.user, partner=self.partner, role='ADMINISTRATOR')
        partners = self.service.get_user_partners(self.user)
        self.assertEqual(len(partners), 1)
        self.assertEqual(partners[0], self.partner)

    def test_add_member(self):
        member = User.objects.create_user(
            username='newmember', email='new@test.com', password='Pass123!'
        )
        membership = self.service.add_member(self.partner, member, role='EDITOR')
        self.assertEqual(membership.role, 'EDITOR')
        self.assertTrue(membership.is_active)

    def test_remove_member(self):
        member = User.objects.create_user(
            username='removemember', email='remove@test.com', password='Pass123!'
        )
        PartnerMembership.objects.create(user=member, partner=self.partner, role='VIEWER')
        result = self.service.remove_member(self.partner, member)
        self.assertTrue(result)
        membership = PartnerMembership.objects.get(user=member, partner=self.partner)
        self.assertFalse(membership.is_active)

    def test_get_or_create_default_partner(self):
        partner = self.service.get_or_create_default_partner()
        self.assertEqual(partner.slug, 'kabulhaden-online')
        self.assertEqual(partner.name, 'Kabulhaden Online')


class FeatureFlagTestCase(TestCase):
    """Test FeatureFlag model and service."""

    def setUp(self):
        self.flag = FeatureFlag.objects.create(
            key='test_feature',
            name='Test Feature',
            description='A test feature',
            is_enabled=True,
            scope=FeatureFlagScope.GLOBAL,
            category='testing',
        )
        self.partner = Partner.objects.create(
            name='FF Test Partner',
            slug='ff-test-partner',
            status=PartnerStatus.ACTIVE,
        )

    def test_flag_creation(self):
        self.assertEqual(self.flag.key, 'test_feature')
        self.assertTrue(self.flag.is_enabled)

    def test_flag_is_available_for_partner(self):
        self.assertTrue(self.flag.is_available_for_partner(self.partner))

    def test_flag_disabled_not_available(self):
        self.flag.is_enabled = False
        self.flag.save()
        self.assertFalse(self.flag.is_available_for_partner(self.partner))

    def test_flag_partner_override(self):
        FeatureFlagPartner.objects.create(
            flag=self.flag,
            partner=self.partner,
            is_enabled=False,
        )
        self.assertFalse(self.flag.is_available_for_partner(self.partner))

    def test_flag_required_tier(self):
        self.flag.required_tier = 'PROFESSIONAL'
        self.flag.save()
        self.partner.tier = 'COMMUNITY'
        self.partner.save()
        self.assertFalse(self.flag.is_available_for_partner(self.partner))
        self.partner.tier = 'PROFESSIONAL'
        self.partner.save()
        self.assertTrue(self.flag.is_available_for_partner(self.partner))


class FeatureFlagServiceTestCase(TestCase):
    """Test FeatureFlagService caching and operations."""

    def setUp(self):
        self.service = FeatureFlagService()
        self.flag = FeatureFlag.objects.create(
            key='cached_feature',
            name='Cached Feature',
            is_enabled=True,
        )
        self.partner = Partner.objects.create(
            name='Cache Test',
            slug='cache-test',
            status=PartnerStatus.ACTIVE,
        )

    def test_is_enabled(self):
        self.assertTrue(self.service.is_enabled('cached_feature'))
        self.assertFalse(self.service.is_enabled('nonexistent'))

    def test_get_config(self):
        self.flag.config = {'timeout': 30}
        self.flag.save()
        config = self.service.get_config('cached_feature')
        self.assertEqual(config['timeout'], 30)

    def test_enable_disable(self):
        self.service.disable('cached_feature')
        self.flag.refresh_from_db()
        self.assertFalse(self.flag.is_enabled)

        self.service.enable('cached_feature')
        self.flag.refresh_from_db()
        self.assertTrue(self.flag.is_enabled)

    def test_get_enabled_features(self):
        features = self.service.get_enabled_features(self.partner)
        self.assertIn('cached_feature', features)

    def test_set_for_partner(self):
        result = self.service.set_for_partner('cached_feature', self.partner, False)
        self.assertTrue(result)
        override = FeatureFlagPartner.objects.get(flag=self.flag, partner=self.partner)
        self.assertFalse(override.is_enabled)


class DomainEngineTestCase(TestCase):
    """Test DomainEngine domain resolution."""

    def setUp(self):
        self.engine = DomainEngine()
        self.partner = Partner.objects.create(
            name='Domain Test',
            slug='domain-test',
            status=PartnerStatus.ACTIVE,
            primary_domain='domain.example.com',
        )
        self.factory = RequestFactory()

    def test_resolve_primary_domain(self):
        request = self.factory.get('/', HTTP_HOST='domain.example.com')
        partner, method = self.engine._resolve_domain('domain.example.com')
        self.assertEqual(partner, self.partner)
        self.assertEqual(method, 'domain_primary')

    def test_resolve_custom_domain(self):
        PartnerDomain.objects.create(
            partner=self.partner,
            domain='custom.example.com',
            is_primary=False,
            is_verified=True,
        )
        partner, method = self.engine._resolve_domain('custom.example.com')
        self.assertEqual(partner, self.partner)
        self.assertEqual(method, 'domain_custom')

    def test_resolve_subdomain(self):
        with override_settings(PLATFORM_BASE_DOMAIN='example.com'):
            partner, method = self.engine._resolve_domain('domain-test.example.com')
            self.assertEqual(partner, self.partner)
            self.assertEqual(method, 'subdomain')

    def test_get_partner_domains(self):
        domains = self.engine.get_partner_domains(self.partner)
        self.assertEqual(len(domains), 1)
        self.assertEqual(domains[0]['domain'], 'domain.example.com')
        self.assertTrue(domains[0]['is_primary'])

    def test_get_subdomain_for_partner(self):
        subdomain = self.engine.get_subdomain_for_partner(self.partner)
        self.assertEqual(subdomain, 'domain-test.kabulhaden.com')

    def test_verify_domain(self):
        # This tests the structure; actual DNS verification depends on network
        is_valid, msg = self.engine.verify_domain('nonexistent.invalid')
        self.assertFalse(is_valid)


class TenantIsolationTestCase(TestCase):
    """Test TenantIsolation security measures."""

    def setUp(self):
        self.partner_a = Partner.objects.create(
            name='Partner A', slug='partner-a', status=PartnerStatus.ACTIVE,
        )
        self.partner_b = Partner.objects.create(
            name='Partner B', slug='partner-b', status=PartnerStatus.ACTIVE,
        )

    def test_get_partner_queryset(self):
        from apps.podcast.models import Podcast
        Podcast.objects.create(title='Podcast A', partner=self.partner_a)
        Podcast.objects.create(title='Podcast B', partner=self.partner_b)

        qs_a = TenantIsolation.get_partner_queryset(Podcast, self.partner_a)
        self.assertEqual(qs_a.count(), 1)
        self.assertEqual(qs_a.first().title, 'Podcast A')

    def test_check_object_access_same_partner(self):
        from apps.podcast.models import Podcast
        podcast = Podcast.objects.create(title='Podcast A', partner=self.partner_a)

        request = MagicMock()
        request.user = MagicMock(is_authenticated=True, role='EDITOR')
        request.partner_context = PartnerContext(partner=self.partner_a, is_default=False)

        with patch('apps.platform.partner.context.get_partner_from_context', return_value=self.partner_a):
            self.assertTrue(TenantIsolation.check_object_access(podcast, request))

    def test_check_object_access_different_partner(self):
        from apps.podcast.models import Podcast
        podcast = Podcast.objects.create(title='Podcast B', partner=self.partner_a)

        request = MagicMock()
        request.user = MagicMock(is_authenticated=True, role='EDITOR')
        request.partner_context = PartnerContext(partner=self.partner_b, is_default=False)

        with patch('apps.platform.partner.context.get_partner_from_context', return_value=self.partner_b):
            self.assertFalse(TenantIsolation.check_object_access(podcast, request))

    def test_check_object_access_superuser(self):
        from apps.podcast.models import Podcast
        podcast = Podcast.objects.create(title='Test', partner=self.partner_a)

        request = MagicMock()
        request.user = MagicMock(is_authenticated=True, role='SUPERUSER')

        self.assertTrue(TenantIsolation.check_object_access(podcast, request))

    def test_check_object_access_no_partner(self):
        from apps.podcast.models import Podcast
        podcast = Podcast.objects.create(title='Global', partner=None)

        request = MagicMock()
        request.user = MagicMock(is_authenticated=True, role='EDITOR')

        self.assertTrue(TenantIsolation.check_object_access(podcast, request))


class PartnerContextTestCase(TestCase):
    """Test PartnerContext dataclass."""

    def setUp(self):
        self.partner = Partner.objects.create(
            name='Context Test',
            slug='context-test',
            status=PartnerStatus.ACTIVE,
            tier=PartnerTier.PROFESSIONAL,
            feature_overrides={'podcast': True},
            provider_overrides={'STREAMING': 'icecast'},
        )

    def test_context_properties(self):
        ctx = PartnerContext(partner=self.partner, is_default=False)
        self.assertEqual(ctx.partner_name, 'Context Test')
        self.assertTrue(ctx.is_active)
        self.assertEqual(ctx.tier, 'PROFESSIONAL')

    def test_context_has_feature(self):
        ctx = PartnerContext(partner=self.partner)
        self.assertTrue(ctx.has_feature('podcast'))
        self.assertFalse(ctx.has_feature('unknown'))

    def test_context_get_provider(self):
        ctx = PartnerContext(partner=self.partner)
        self.assertEqual(ctx.get_provider('STREAMING'), 'icecast')
        self.assertIsNone(ctx.get_provider('STORAGE'))

    def test_context_to_dict(self):
        ctx = PartnerContext(partner=self.partner)
        d = ctx.to_dict()
        self.assertEqual(d['partner_name'], 'Context Test')
        self.assertEqual(d['tier'], 'PROFESSIONAL')

    def test_context_empty(self):
        ctx = PartnerContext()
        self.assertIsNone(ctx.partner_id)
        self.assertEqual(ctx.partner_name, '')
        self.assertFalse(ctx.is_active)

    def test_get_partner_from_context(self):
        ctx = PartnerContext(partner=self.partner)
        request = MagicMock(partner_context=ctx)
        self.assertEqual(get_partner_from_context(request), self.partner)

    def test_get_partner_from_context_none(self):
        request = MagicMock(spec=[])  # No partner_context attribute
        self.assertIsNone(get_partner_from_context(request))


class AuditLoggerTestCase(TestCase):
    """Test AuditLogger functionality."""

    def test_log_action(self):
        user = User.objects.create_user(
            username='audituser', email='audit@test.com', password='Pass123!'
        )
        partner = Partner.objects.create(
            name='Audit Partner', slug='audit-partner', status=PartnerStatus.ACTIVE,
        )
        # Should not raise
        AuditLogger.log_action(
            action='PARTNER_CREATE',
            user=user,
            partner=partner,
            object_repr='Test Partner',
            details={'name': 'Test'},
        )
        # Verify log was created
        self.assertTrue(FeatureFlagLog.objects.filter(action='PARTNER_CREATE').exists())


class PartnerInvitationTestCase(TestCase):
    """Test PartnerInvitation model."""

    def setUp(self):
        self.partner = Partner.objects.create(
            name='Invite Partner', slug='invite-partner', status=PartnerStatus.ACTIVE,
        )
        self.user = User.objects.create_user(
            username='inviter', email='inviter@test.com', password='Pass123!'
        )

    def test_invitation_creation(self):
        from django.utils import timezone
        from datetime import timedelta
        inv = PartnerInvitation.objects.create(
            partner=self.partner,
            email='new@test.com',
            role='EDITOR',
            invited_by=self.user,
            expires_at=timezone.now() + timedelta(days=7),
        )
        self.assertEqual(inv.status, 'PENDING')
        self.assertTrue(inv.is_valid)

    def test_invitation_expired(self):
        from django.utils import timezone
        from datetime import timedelta
        inv = PartnerInvitation.objects.create(
            partner=self.partner,
            email='expired@test.com',
            role='VIEWER',
            invited_by=self.user,
            expires_at=timezone.now() - timedelta(days=1),
        )
        self.assertTrue(inv.is_expired)
        self.assertFalse(inv.is_valid)
