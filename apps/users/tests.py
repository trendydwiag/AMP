import secrets
from datetime import timedelta

from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.users.models import (
    UserProfile, LoginHistory, PasswordHistory,
    AuditLog, EmailVerification, TwoFactorDevice, TOTPHelper,
)
from apps.users.repositories import (
    UserRepository, UserProfileRepository, LoginHistoryRepository,
    PasswordHistoryRepository, AuditLogRepository, EmailVerificationRepository,
    TwoFactorDeviceRepository,
)
from apps.users.services import (
    UserService, LoginHistoryService, AuditLogService,
    EmailVerificationService, TwoFactorService, UserProfileService,
    PasswordHistoryService,
)
from apps.users.forms import (
    LoginForm, RegisterForm, ProfileForm, UserProfileForm,
    AdminPasswordResetForm, TwoFactorSetupForm,
)
from utils.choices import UserRole, AccountStatus, LoginStatus, AuditAction

User = get_user_model()


class UserModelTestCase(TestCase):
    """Test custom User model fields, properties, and methods."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@kabulhaden.com',
            password='TestPassword123!',
            first_name='Test',
            last_name='User',
        )

    def test_user_creation_with_uuid(self):
        """Verify user gets UUID primary key."""
        self.assertIsNotNone(self.user.id)
        self.assertEqual(str(self.user.id.__class__.__name__), 'UUID')

    def test_default_role_is_viewer(self):
        """Verify default role assignment."""
        self.assertEqual(self.user.role, UserRole.VIEWER)

    def test_superuser_flags(self):
        """Verify superuser has correct flags."""
        admin = User.objects.create_superuser(
            username='admin', email='admin@kabulhaden.com', password='AdminPass123!'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.role, UserRole.SUPERUSER)

    def test_get_full_name(self):
        """Verify full name property."""
        self.assertEqual(self.user.get_full_name, 'Test User')

    def test_get_full_name_fallback(self):
        """Verify full name falls back to username."""
        user = User.objects.create_user(
            username='nobody', email='nobody@kabulhaden.com', password='Pass123!'
        )
        self.assertEqual(user.get_full_name, 'nobody')

    def test_get_short_name(self):
        """Verify short name property."""
        self.assertEqual(self.user.get_short_name, 'Test')

    def test_is_account_locked_false(self):
        """Verify account is not locked by default."""
        self.assertFalse(self.user.is_account_locked)

    def test_is_account_locked_true(self):
        """Verify account locking."""
        self.user.lock_account(duration_minutes=30)
        self.assertTrue(self.user.is_account_locked)

    def test_is_suspended_false(self):
        """Verify account is not suspended by default."""
        self.assertFalse(self.user.is_suspended)

    def test_suspend(self):
        """Verify account suspension."""
        self.user.suspend()
        self.assertTrue(self.user.is_suspended)
        self.assertFalse(self.user.is_active)

    def test_activate(self):
        """Verify account activation."""
        self.user.suspend()
        self.user.activate()
        self.assertFalse(self.user.is_suspended)
        self.assertTrue(self.user.is_active)

    def test_can_login_active(self):
        """Verify active user can login."""
        self.assertTrue(self.user.can_login)

    def test_can_login_suspended(self):
        """Verify suspended user cannot login."""
        self.user.suspend()
        self.assertFalse(self.user.can_login)

    def test_can_login_locked(self):
        """Verify locked user cannot login."""
        self.user.lock_account()
        self.assertFalse(self.user.can_login)

    def test_increment_failed_login(self):
        """Verify failed login counter increments."""
        self.assertEqual(self.user.failed_login_attempts, 0)
        self.user.increment_failed_login()
        self.user.refresh_from_db()
        self.assertEqual(self.user.failed_login_attempts, 1)

    def test_reset_failed_login(self):
        """Verify failed login counter resets."""
        self.user.failed_login_attempts = 5
        self.user.save(update_fields=['failed_login_attempts'])
        self.user.reset_failed_login()
        self.user.refresh_from_db()
        self.assertEqual(self.user.failed_login_attempts, 0)

    def test_unlock_account(self):
        """Verify account unlock."""
        self.user.lock_account()
        self.user.unlock_account()
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_account_locked)
        self.assertEqual(self.user.failed_login_attempts, 0)

    def test_generate_totp_secret(self):
        """Verify TOTP secret generation."""
        secret = self.user.generate_totp_secret()
        self.assertEqual(len(secret), 40)

    def test_user_str(self):
        """Verify string representation."""
        self.assertIn('testuser', str(self.user))


class TOTPHelperTestCase(TestCase):
    """Test TOTP token generation and verification."""

    def test_generate_and_verify(self):
        """Verify TOTP token generation and verification."""
        secret = secrets.token_hex(20)
        token = TOTPHelper.generate_token(secret)
        self.assertEqual(len(token), 6)
        self.assertTrue(TOTPHelper.verify(secret, token))

    def test_verify_invalid_token(self):
        """Verify invalid token is rejected."""
        secret = secrets.token_hex(20)
        self.assertFalse(TOTPHelper.verify(secret, '000000'))

    def test_verify_with_tolerance(self):
        """Verify token with time tolerance."""
        secret = secrets.token_hex(20)
        token = TOTPHelper.generate_token(secret)
        self.assertTrue(TOTPHelper.verify(secret, token, tolerance=1))


class UserProfileModelTestCase(TestCase):
    """Test UserProfile model creation and properties."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='profiletest', email='profile@kabulhaden.com', password='Pass123!'
        )

    def test_profile_creation(self):
        """Verify profile can be created for user."""
        profile = UserProfile.objects.create(user=self.user, bio='Test bio', phone='08123456789')
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.bio, 'Test bio')

    def test_profile_str(self):
        """Verify profile string representation."""
        profile = UserProfile.objects.create(user=self.user)
        self.assertIn('profiletest', str(profile))


class LoginHistoryModelTestCase(TestCase):
    """Test LoginHistory model recording and queries."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='logintest', email='login@kabulhaden.com', password='Pass123!'
        )

    def test_record_login(self):
        """Verify login history records correctly."""
        entry = LoginHistory.objects.create(
            user=self.user,
            username_attempted='logintest',
            ip_address='127.0.0.1',
            status=LoginStatus.SUCCESS,
        )
        self.assertEqual(entry.user, self.user)
        self.assertEqual(entry.status, LoginStatus.SUCCESS)

    def test_record_failed_login(self):
        """Verify failed login recording."""
        entry = LoginHistory.objects.create(
            user=self.user,
            username_attempted='logintest',
            ip_address='127.0.0.1',
            status=LoginStatus.FAILED,
            failure_reason='Password salah',
        )
        self.assertEqual(entry.status, LoginStatus.FAILED)


class AuditLogModelTestCase(TestCase):
    """Test AuditLog model creation and queries."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='auditest', email='audit@kabulhaden.com', password='Pass123!'
        )

    def test_create_audit_log(self):
        """Verify audit log creation."""
        log = AuditLog.objects.create(
            user=self.user,
            action=AuditAction.LOGIN,
            resource=f"User: {self.user.username}",
            details="Login successful",
            ip_address='127.0.0.1',
        )
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.action, AuditAction.LOGIN)


class EmailVerificationModelTestCase(TestCase):
    """Test EmailVerification token lifecycle."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='evtest', email='verify@kabulhaden.com', password='Pass123!'
        )

    def test_token_generation(self):
        """Verify token generation."""
        token = EmailVerification.generate_token()
        self.assertEqual(len(token), 64)

    def test_token_expiry(self):
        """Verify token expiration check."""
        verification = EmailVerification.objects.create(
            user=self.user,
            token=EmailVerification.generate_token(),
            expires_at=timezone.now() - timedelta(hours=1),
        )
        self.assertTrue(verification.is_expired)

    def test_token_valid(self):
        """Verify valid token check."""
        verification = EmailVerification.objects.create(
            user=self.user,
            token=EmailVerification.generate_token(),
            expires_at=timezone.now() + timedelta(hours=48),
        )
        self.assertTrue(verification.is_valid)


class UserRepositoryTestCase(TestCase):
    """Test UserRepository data access methods."""

    def setUp(self):
        self.repo = UserRepository()
        self.user = User.objects.create_user(
            username='repotest', email='repo@kabulhaden.com', password='Pass123!'
        )

    def test_get_by_username(self):
        """Verify username lookup."""
        found = self.repo.get_by_username('repotest')
        self.assertEqual(found, self.user)

    def test_get_by_username_not_found(self):
        """Verify username not found returns None."""
        self.assertIsNone(self.repo.get_by_username('nonexistent'))

    def test_get_by_email(self):
        """Verify email lookup."""
        found = self.repo.get_by_email('repo@kabulhaden.com')
        self.assertEqual(found, self.user)

    def test_get_by_email_case_insensitive(self):
        """Verify case-insensitive email lookup."""
        found = self.repo.get_by_email('REPO@KABULHADEN.COM')
        self.assertEqual(found, self.user)

    def test_list_active(self):
        """Verify active user listing."""
        active_users = self.repo.list_active()
        self.assertIn(self.user, active_users)

    def test_list_by_role(self):
        """Verify role-based listing."""
        viewers = self.repo.list_by_role(UserRole.VIEWER)
        self.assertIn(self.user, viewers)


class UserServiceTestCase(TestCase):
    """Test UserService business logic."""

    def setUp(self):
        self.service = UserService()

    def test_register_new_user(self):
        """Verify new user registration."""
        user = self.service.register_new_user(
            username='newuser', email='new@kabulhaden.com', raw_password='SecurePass123!'
        )
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, 'newuser')

    def test_register_duplicate_username(self):
        """Verify duplicate username raises error."""
        self.service.register_new_user(
            username='dupuser', email='dup@kabulhaden.com', raw_password='SecurePass123!'
        )
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            self.service.register_new_user(
                username='dupuser', email='other@kabulhaden.com', raw_password='SecurePass123!'
            )

    def test_register_duplicate_email(self):
        """Verify duplicate email raises error."""
        self.service.register_new_user(
            username='emailuser', email='email@kabulhaden.com', raw_password='SecurePass123!'
        )
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            self.service.register_new_user(
                username='emailuser2', email='email@kabulhaden.com', raw_password='SecurePass123!'
            )

    def test_change_user_password(self):
        """Verify password change."""
        user = User.objects.create_user(
            username='pwuser', email='pw@kabulhaden.com', password='OldPass123!'
        )
        self.service.change_user_password(user, 'NewSecurePass123!')
        user.refresh_from_db()
        self.assertTrue(user.check_password('NewSecurePass123!'))

    def test_suspend_user(self):
        """Verify user suspension with audit."""
        admin = User.objects.create_superuser(
            username='superadmin', email='super@kabulhaden.com', password='AdminPass123!'
        )
        target = User.objects.create_user(
            username='target', email='target@kabulhaden.com', password='Pass123!'
        )
        self.service.suspend_user(target, admin, '127.0.0.1')
        target.refresh_from_db()
        self.assertTrue(target.is_suspended)

    def test_activate_user(self):
        """Verify user activation with audit."""
        admin = User.objects.create_superuser(
            username='superadmin2', email='super2@kabulhaden.com', password='AdminPass123!'
        )
        target = User.objects.create_user(
            username='target2', email='target2@kabulhaden.com', password='Pass123!'
        )
        target.suspend()
        self.service.activate_user(target, admin, '127.0.0.1')
        target.refresh_from_db()
        self.assertTrue(target.is_active)

    def test_lock_unlock_account(self):
        """Verify account lock/unlock with audit."""
        admin = User.objects.create_superuser(
            username='superadmin3', email='super3@kabulhaden.com', password='AdminPass123!'
        )
        target = User.objects.create_user(
            username='target3', email='target3@kabulhaden.com', password='Pass123!'
        )
        self.service.lock_account(target, admin, '127.0.0.1')
        target.refresh_from_db()
        self.assertTrue(target.is_account_locked)

        self.service.unlock_account(target, admin, '127.0.0.1')
        target.refresh_from_db()
        self.assertFalse(target.is_account_locked)

    def test_assign_role(self):
        """Verify role assignment with audit."""
        admin = User.objects.create_superuser(
            username='superadmin4', email='super4@kabulhaden.com', password='AdminPass123!'
        )
        target = User.objects.create_user(
            username='target4', email='target4@kabulhaden.com', password='Pass123!'
        )
        self.service.assign_role(target, UserRole.EDITOR, admin, '127.0.0.1')
        target.refresh_from_db()
        self.assertEqual(target.role, UserRole.EDITOR)


class LoginHistoryServiceTestCase(TestCase):
    """Test LoginHistoryService recording."""

    def setUp(self):
        self.service = LoginHistoryService()
        self.user = User.objects.create_user(
            username='loginhist', email='loginhist@kabulhaden.com', password='Pass123!'
        )

    def test_record_login_attempt(self):
        """Verify login attempt recording."""
        entry = self.service.record_login_attempt(
            username='loginhist',
            ip_address='127.0.0.1',
            status=LoginStatus.SUCCESS,
            user_agent='TestAgent',
            user=self.user,
        )
        self.assertIsNotNone(entry.id)
        self.assertEqual(entry.status, LoginStatus.SUCCESS)


class EmailVerificationServiceTestCase(TestCase):
    """Test EmailVerificationService token operations."""

    def setUp(self):
        self.service = EmailVerificationService()
        self.user = User.objects.create_user(
            username='evtest', email='ev@kabulhaden.com', password='Pass123!'
        )

    def test_create_verification(self):
        """Verify token creation."""
        token = self.service.create_verification(self.user)
        self.assertEqual(len(token), 64)

    def test_verify_email_valid_token(self):
        """Verify email with valid token."""
        token = self.service.create_verification(self.user)
        verified_user = self.service.verify_email(token)
        self.assertIsNotNone(verified_user)
        verified_user.refresh_from_db()
        self.assertTrue(verified_user.email_verified)

    def test_verify_email_invalid_token(self):
        """Verify email with invalid token."""
        result = self.service.verify_email('invalidtoken123')
        self.assertIsNone(result)

    def test_verify_email_expired_token(self):
        """Verify email with expired token."""
        verification = EmailVerification.objects.create(
            user=self.user,
            token=EmailVerification.generate_token(),
            expires_at=timezone.now() - timedelta(hours=1),
        )
        result = self.service.verify_email(verification.token)
        self.assertIsNone(result)


class TwoFactorServiceTestCase(TestCase):
    """Test TwoFactorService operations."""

    def setUp(self):
        self.service = TwoFactorService()
        self.user = User.objects.create_user(
            username='2fatest', email='2fa@kabulhaden.com', password='Pass123!'
        )

    def test_generate_secret(self):
        """Verify secret generation."""
        secret = self.service.generate_secret()
        self.assertEqual(len(secret), 40)

    def test_setup_and_verify_2fa(self):
        """Verify 2FA setup and token verification."""
        secret = self.service.setup_2fa(self.user, "Test Device")
        self.assertIsNotNone(secret)

        device = TwoFactorDeviceRepository().get_by_user(self.user)
        self.assertIsNotNone(device)

        token = TOTPHelper.generate_token(secret)
        self.assertTrue(self.service.verify_token(self.user, token))

    def test_verify_invalid_token(self):
        """Verify invalid token is rejected."""
        self.service.setup_2fa(self.user, "Test Device")
        self.assertFalse(self.service.verify_token(self.user, '000000'))

    def test_disable_2fa(self):
        """Verify 2FA disabling."""
        self.service.setup_2fa(self.user, "Test Device")
        result = self.service.disable_2fa(self.user)
        self.assertTrue(result)
        device = TwoFactorDeviceRepository().get_by_user(self.user)
        self.assertIsNone(device)


class PasswordHistoryServiceTestCase(TestCase):
    """Test PasswordHistoryService tracking."""

    def setUp(self):
        self.service = PasswordHistoryService()
        self.user = User.objects.create_user(
            username='pwhtest', email='pwh@kabulhaden.com', password='Pass123!'
        )

    def test_record_password(self):
        """Verify password recording."""
        self.service.record_password(self.user, 'Pass123!')
        entries = PasswordHistory.objects.filter(user=self.user)
        self.assertTrue(entries.exists())


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class LoginViewTestCase(TestCase):
    """Test authentication views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='viewtest', email='view@kabulhaden.com', password='TestPass123!'
        )

    def test_login_page_loads(self):
        """Verify login page renders."""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        """Verify successful login."""
        response = self.client.post(reverse('users:login'), {
            'username': 'viewtest',
            'password': 'TestPass123!',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_failure_wrong_password(self):
        """Verify failed login with wrong password."""
        response = self.client.post(reverse('users:login'), {
            'username': 'viewtest',
            'password': 'WrongPass123!',
        })
        self.assertEqual(response.status_code, 200)

    def test_login_failure_nonexistent_user(self):
        """Verify failed login with nonexistent user."""
        response = self.client.post(reverse('users:login'), {
            'username': 'nonexistent',
            'password': 'TestPass123!',
        })
        self.assertEqual(response.status_code, 200)

    def test_login_suspended_user(self):
        """Verify suspended user cannot login."""
        self.user.suspend()
        response = self.client.post(reverse('users:login'), {
            'username': 'viewtest',
            'password': 'TestPass123!',
        })
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """Verify logout."""
        self.client.login(username='viewtest', password='TestPass123!')
        response = self.client.post(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)

    def test_register_page_loads(self):
        """Verify registration page renders."""
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_success(self):
        """Verify successful registration."""
        response = self.client.post(reverse('users:register'), {
            'username': 'newreg',
            'email': 'newreg@kabulhaden.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'SecureP@ssw0rd!',
            'password2': 'SecureP@ssw0rd!',
        })
        self.assertEqual(response.status_code, 302)

    def test_register_duplicate(self):
        """Verify duplicate registration fails."""
        response = self.client.post(reverse('users:register'), {
            'username': 'viewtest',
            'email': 'other@kabulhaden.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        })
        self.assertEqual(response.status_code, 200)

    def test_forgot_password_page_loads(self):
        """Verify forgot password page renders."""
        response = self.client.get(reverse('users:forgot_password'))
        self.assertEqual(response.status_code, 200)

    def test_forgot_password_submit(self):
        """Verify forgot password form submission."""
        response = self.client.post(reverse('users:forgot_password'), {
            'email': 'view@kabulhaden.com',
        })
        self.assertEqual(response.status_code, 302)

    def test_verify_email_notice_page(self):
        """Verify email notice page renders."""
        response = self.client.get(reverse('users:verify_email_notice'))
        self.assertEqual(response.status_code, 200)

    def test_verify_email_invalid_token(self):
        """Verify invalid token redirect."""
        response = self.client.get(reverse('users:verify_email', kwargs={'token': 'invalidtoken'}))
        self.assertEqual(response.status_code, 302)

    def test_verify_email_valid_token(self):
        """Verify valid token verification."""
        token = EmailVerificationService().create_verification(self.user)
        response = self.client.get(reverse('users:verify_email', kwargs={'token': token}))
        self.assertEqual(response.status_code, 302)


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class ProfileViewTestCase(TestCase):
    """Test profile views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='proftest', email='prof@kabulhaden.com', password='TestPass123!'
        )
        self.client.login(username='proftest', password='TestPass123!')

    def test_profile_page_loads(self):
        """Verify profile page renders."""
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_update(self):
        """Verify profile update."""
        response = self.client.post(reverse('users:profile'), {
            'update_profile': '1',
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'prof@kabulhaden.com',
            'bio': 'Updated bio',
            'phone': '08111111111',
        })
        self.assertEqual(response.status_code, 302)

    def test_change_password_page_loads(self):
        """Verify change password page renders."""
        response = self.client.get(reverse('users:change_password'))
        self.assertEqual(response.status_code, 200)


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class AdminUserManagementTestCase(TestCase):
    """Test admin user management views."""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admintest', email='admintest@kabulhaden.com', password='AdminPass123!'
        )
        self.target = User.objects.create_user(
            username='targetuser', email='target@kabulhaden.com', password='TargetPass123!'
        )
        self.client.login(username='admintest', password='AdminPass123!')

    def test_user_list_page(self):
        """Verify admin user list page renders."""
        response = self.client.get(reverse('users:admin_user_list'))
        self.assertEqual(response.status_code, 200)

    def test_user_list_search(self):
        """Verify user list search filtering."""
        response = self.client.get(reverse('users:admin_user_list'), {'q': 'target'})
        self.assertEqual(response.status_code, 200)

    def test_user_list_role_filter(self):
        """Verify user list role filtering."""
        response = self.client.get(reverse('users:admin_user_list'), {'role': UserRole.VIEWER})
        self.assertEqual(response.status_code, 200)

    def test_user_detail_page(self):
        """Verify admin user detail page renders."""
        response = self.client.get(
            reverse('users:admin_user_detail', kwargs={'user_id': self.target.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_user_detail_not_found(self):
        """Verify user detail for nonexistent user redirects."""
        import uuid
        fake_id = uuid.uuid4()
        response = self.client.get(
            reverse('users:admin_user_detail', kwargs={'user_id': fake_id})
        )
        self.assertEqual(response.status_code, 302)

    def test_admin_suspend_user(self):
        """Verify admin can suspend user."""
        response = self.client.post(
            reverse('users:admin_user_detail', kwargs={'user_id': self.target.id}),
            {'action': 'suspend'}
        )
        self.assertEqual(response.status_code, 302)
        self.target.refresh_from_db()
        self.assertTrue(self.target.is_suspended)

    def test_admin_activate_user(self):
        """Verify admin can activate user."""
        self.target.suspend()
        response = self.client.post(
            reverse('users:admin_user_detail', kwargs={'user_id': self.target.id}),
            {'action': 'activate'}
        )
        self.assertEqual(response.status_code, 302)
        self.target.refresh_from_db()
        self.assertTrue(self.target.is_active)

    def test_admin_deactivate_user(self):
        """Verify admin can deactivate user."""
        response = self.client.post(
            reverse('users:admin_user_detail', kwargs={'user_id': self.target.id}),
            {'action': 'deactivate'}
        )
        self.assertEqual(response.status_code, 302)
        self.target.refresh_from_db()
        self.assertFalse(self.target.is_active)

    def test_admin_lock_account(self):
        """Verify admin can lock account."""
        response = self.client.post(
            reverse('users:admin_user_detail', kwargs={'user_id': self.target.id}),
            {'action': 'lock'}
        )
        self.assertEqual(response.status_code, 302)
        self.target.refresh_from_db()
        self.assertTrue(self.target.is_account_locked)

    def test_admin_unlock_account(self):
        """Verify admin can unlock account."""
        self.target.lock_account()
        response = self.client.post(
            reverse('users:admin_user_detail', kwargs={'user_id': self.target.id}),
            {'action': 'unlock'}
        )
        self.assertEqual(response.status_code, 302)
        self.target.refresh_from_db()
        self.assertFalse(self.target.is_account_locked)

    def test_admin_assign_role(self):
        """Verify admin can assign role."""
        response = self.client.post(
            reverse('users:admin_user_detail', kwargs={'user_id': self.target.id}),
            {'action': 'assign_role', 'role': UserRole.EDITOR}
        )
        self.assertEqual(response.status_code, 302)
        self.target.refresh_from_db()
        self.assertEqual(self.target.role, UserRole.EDITOR)

    def test_admin_reset_password(self):
        """Verify admin can reset password."""
        response = self.client.post(
            reverse('users:admin_user_detail', kwargs={'user_id': self.target.id}),
            {
                'action': 'reset_password',
                'new_password': 'NewResetPass123!',
                'confirm_password': 'NewResetPass123!',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.target.refresh_from_db()
        self.assertTrue(self.target.check_password('NewResetPass123!'))
        self.assertTrue(self.target.force_password_change)

    def test_admin_create_user_page(self):
        """Verify admin create user page renders."""
        response = self.client.get(reverse('users:admin_user_create'))
        self.assertEqual(response.status_code, 200)

    def test_admin_create_user(self):
        """Verify admin can create user."""
        response = self.client.post(reverse('users:admin_user_create'), {
            'username': 'admincreated',
            'email': 'admincreated@kabulhaden.com',
            'password': 'AdminCreated123!',
            'role': UserRole.EDITOR,
            'is_staff': False,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='admincreated').exists())


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class DecoratorTestCase(TestCase):
    """Test custom decorators."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='dectest', email='dec@kabulhaden.com', password='TestPass123!',
            role=UserRole.VIEWER,
        )
        self.admin = User.objects.create_superuser(
            username='decadmin', email='decadmin@kabulhaden.com', password='AdminPass123!'
        )

    def test_guest_only_redirects_authenticated(self):
        """Verify guest_only redirects authenticated users."""
        self.client.login(username='dectest', password='TestPass123!')
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 302)

    def test_login_required_redirects_anonymous(self):
        """Verify login_required redirects anonymous users."""
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class MiddlewareTestCase(TestCase):
    """Test custom middleware."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='mwtest', email='mw@kabulhaden.com', password='TestPass123!'
        )

    def test_last_activity_updates(self):
        """Verify last activity is tracked."""
        self.client.login(username='mwtest', password='TestPass123!')
        self.client.get(reverse('core:home'))
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.last_activity)


@override_settings(AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'])
class FormTestCase(TestCase):
    """Test auth forms validation."""

    def test_login_form_valid(self):
        """Verify valid login form."""
        User.objects.create_user(username='formtest', email='form@kabulhaden.com', password='TestPass123!')
        form = LoginForm(data={'username': 'formtest', 'password': 'TestPass123!'})
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        """Verify invalid login form."""
        form = LoginForm(data={'username': 'nonexistent', 'password': 'WrongPass'})
        self.assertFalse(form.is_valid())

    def test_register_form_valid(self):
        """Verify valid registration form."""
        form = RegisterForm(data={
            'username': 'newreg',
            'email': 'newreg@kabulhaden.com',
            'password1': 'SecureP@ssw0rd123!',
            'password2': 'SecureP@ssw0rd123!',
        })
        self.assertTrue(form.is_valid())

    def test_register_form_password_mismatch(self):
        """Verify registration form password mismatch."""
        form = RegisterForm(data={
            'username': 'newreg2',
            'email': 'newreg2@kabulhaden.com',
            'password1': 'SecureP@ssw0rd123!',
            'password2': 'DifferentPass123!',
        })
        self.assertFalse(form.is_valid())

    def test_register_form_duplicate_username(self):
        """Verify registration form duplicate username."""
        User.objects.create_user(username='existing', email='exist@kabulhaden.com', password='Pass123!')
        form = RegisterForm(data={
            'username': 'existing',
            'email': 'other@kabulhaden.com',
            'password1': 'SecureP@ssw0rd123!',
            'password2': 'SecureP@ssw0rd123!',
        })
        self.assertFalse(form.is_valid())

    def test_two_factor_setup_form_valid(self):
        """Verify valid 2FA setup form."""
        form = TwoFactorSetupForm(data={'token': '123456'})
        self.assertTrue(form.is_valid())

    def test_two_factor_setup_form_invalid_length(self):
        """Verify 2FA form rejects wrong length token."""
        form = TwoFactorSetupForm(data={'token': '12345'})
        self.assertFalse(form.is_valid())

    def test_admin_password_reset_form_mismatch(self):
        """Verify admin password reset form mismatch."""
        form = AdminPasswordResetForm(data={
            'new_password': 'Pass123!',
            'confirm_password': 'Different123!',
        })
        self.assertFalse(form.is_valid())
