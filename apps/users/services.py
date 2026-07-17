import secrets
from typing import Optional, Any

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils import timezone

from utils.choices import LoginStatus, AuditAction
from utils.services import BaseService
from apps.users.repositories import (
    UserRepository, UserProfileRepository, LoginHistoryRepository,
    PasswordHistoryRepository, AuditLogRepository, EmailVerificationRepository,
    TwoFactorDeviceRepository,
)
from apps.users.models import User, TOTPHelper


class UserService(BaseService[UserRepository]):
    """Service handling business domain logic for users."""

    def __init__(self, repository: UserRepository = None) -> None:
        super().__init__(repository or UserRepository())

    def register_new_user(
        self, username: str, email: str, raw_password: str, **extra_fields: Any
    ) -> User:
        """Validate and register a new User."""
        if self.repository.get_by_username(username):
            raise ValidationError("Username sudah terdaftar.")
        if self.repository.get_by_email(email):
            raise ValidationError("Email sudah terdaftar.")

        def _create():
            user = self.repository.create(
                username=username,
                email=email,
                password=raw_password,
                **extra_fields,
            )
            PasswordHistoryService().record_password(user, raw_password)
            return user

        return self.execute_in_transaction(_create)

    def change_user_password(self, user: User, new_password: str) -> None:
        """Safely update a user's password and record in history."""
        def _change():
            user.set_password(new_password)
            user.force_password_change = False
            user.save()
            PasswordHistoryService().record_password(user, new_password)
        self.execute_in_transaction(_change)

    def suspend_user(self, target_user: User, admin_user: User, ip_address: str = None) -> None:
        """Suspend a user account with audit logging."""
        def _suspend():
            target_user.suspend()
            AuditLogService().log(
                action=AuditAction.USER_SUSPEND,
                user=admin_user,
                resource=f"User: {target_user.username}",
                details=f"Akun ditangguhkan oleh {admin_user.username}.",
                ip_address=ip_address,
            )
        self.execute_in_transaction(_suspend)

    def activate_user(self, target_user: User, admin_user: User, ip_address: str = None) -> None:
        """Activate a user account with audit logging."""
        def _activate():
            target_user.activate()
            AuditLogService().log(
                action=AuditAction.USER_ACTIVATE,
                user=admin_user,
                resource=f"User: {target_user.username}",
                details=f"Akun diaktifkan oleh {admin_user.username}.",
                ip_address=ip_address,
            )
        self.execute_in_transaction(_activate)

    def deactivate_user(self, target_user: User, admin_user: User, ip_address: str = None) -> None:
        """Deactivate a user account with audit logging."""
        def _deactivate():
            target_user.is_active = False
            target_user.account_status = 'INACTIVE'
            target_user.save(update_fields=['is_active', 'account_status'])
            AuditLogService().log(
                action=AuditAction.USER_DEACTIVATE,
                user=admin_user,
                resource=f"User: {target_user.username}",
                details=f"Akun dinonaktifkan oleh {admin_user.username}.",
                ip_address=ip_address,
            )
        self.execute_in_transaction(_deactivate)

    def lock_account(self, target_user: User, admin_user: User, ip_address: str = None) -> None:
        """Lock a user account with audit logging."""
        def _lock():
            target_user.lock_account()
            AuditLogService().log(
                action=AuditAction.ACCOUNT_LOCK,
                user=admin_user,
                resource=f"User: {target_user.username}",
                details=f"Akun dikunci oleh {admin_user.username}.",
                ip_address=ip_address,
            )
        self.execute_in_transaction(_lock)

    def unlock_account(self, target_user: User, admin_user: User, ip_address: str = None) -> None:
        """Unlock a user account with audit logging."""
        def _unlock():
            target_user.unlock_account()
            AuditLogService().log(
                action=AuditAction.ACCOUNT_UNLOCK,
                user=admin_user,
                resource=f"User: {target_user.username}",
                details=f"Akun dibuka oleh {admin_user.username}.",
                ip_address=ip_address,
            )
        self.execute_in_transaction(_unlock)

    def assign_role(self, target_user: User, new_role: str, admin_user: User, ip_address: str = None) -> None:
        """Assign a new role to a user with audit logging."""
        def _assign():
            old_role = target_user.role
            target_user.role = new_role
            target_user.save(update_fields=['role'])
            AuditLogService().log(
                action=AuditAction.ROLE_ASSIGN,
                user=admin_user,
                resource=f"User: {target_user.username}",
                details=f"Peran diubah dari {old_role} ke {new_role}.",
                ip_address=ip_address,
            )
        self.execute_in_transaction(_assign)

    def force_password_reset(self, target_user: User, admin_user: User, ip_address: str = None) -> None:
        """Force a user to change their password on next login."""
        def _force():
            target_user.force_password_change = True
            target_user.save(update_fields=['force_password_change'])
            AuditLogService().log(
                action=AuditAction.PASSWORD_RESET,
                user=admin_user,
                resource=f"User: {target_user.username}",
                details=f"User dipaksa mengganti password oleh {admin_user.username}.",
                ip_address=ip_address,
            )
        self.execute_in_transaction(_force)

    def update_profile(self, user: User, **profile_data: Any) -> None:
        """Update user profile information with audit logging."""
        def _update():
            profile, _ = UserProfileRepository().get_or_create(user)
            for field, value in profile_data.items():
                if hasattr(user, field) and field in ('first_name', 'last_name', 'email'):
                    setattr(user, field, value)
                elif hasattr(profile, field):
                    setattr(profile, field, value)
            user.save()
            profile.save()
            AuditLogService().log(
                action=AuditAction.PROFILE_UPDATE,
                user=user,
                resource=f"User: {user.username}",
                details="Profil diperbarui.",
            )
        self.execute_in_transaction(_update)


class LoginHistoryService(BaseService[LoginHistoryRepository]):
    """Service handling login attempt tracking."""

    def __init__(self, repository: LoginHistoryRepository = None) -> None:
        super().__init__(repository or LoginHistoryRepository())

    def record_login_attempt(
        self,
        username: str,
        ip_address: str,
        status: str,
        user_agent: str = '',
        failure_reason: str = '',
        user: Optional[User] = None,
    ):
        """Record a login attempt in history."""
        return self.repository.record_attempt(
            username_attempted=username,
            ip_address=ip_address,
            status=status,
            user_agent=user_agent,
            failure_reason=failure_reason,
            user=user,
        )


class PasswordHistoryService(BaseService[PasswordHistoryRepository]):
    """Service handling password history tracking."""

    def __init__(self, repository: PasswordHistoryRepository = None) -> None:
        super().__init__(repository or PasswordHistoryRepository())

    def record_password(self, user: User, raw_password: str) -> None:
        """Record a password hash in history."""
        self.repository.record_password(user, user.password)

    def is_password_reused(self, user: User, raw_password: str) -> bool:
        """Check if the password was recently used."""
        return self.repository.is_password_reused(user, raw_password)


class AuditLogService(BaseService[AuditLogRepository]):
    """Service handling audit log operations."""

    def __init__(self, repository: AuditLogRepository = None) -> None:
        super().__init__(repository or AuditLogRepository())

    def log(
        self,
        action: str,
        user: Optional[User] = None,
        resource: str = '',
        details: str = '',
        ip_address: Optional[str] = None,
    ):
        """Create an audit log entry."""
        return self.repository.log(
            action=action,
            user=user,
            resource=resource,
            details=details,
            ip_address=ip_address,
        )


class EmailVerificationService(BaseService[EmailVerificationRepository]):
    """Service handling email verification token operations."""

    def __init__(self, repository: EmailVerificationRepository = None) -> None:
        super().__init__(repository or EmailVerificationRepository())

    def create_verification(self, user: User) -> str:
        """Generate and return a new verification token."""
        self.repository.revoke_all(user)
        verification = self.repository.create_for_user(user)
        return verification.token

    def verify_email(self, token: str) -> Optional[User]:
        """Verify an email token and activate the user's email."""
        verification = self.repository.get_valid_token(token)
        if not verification:
            return None

        def _verify():
            verification.verified = True
            verification.save(update_fields=['verified'])
            verification.user.email_verified = True
            verification.user.save(update_fields=['email_verified'])
            AuditLogService().log(
                action=AuditAction.EMAIL_VERIFY,
                user=verification.user,
                resource=f"Email: {verification.user.email}",
                details="Email diverifikasi.",
            )
            return verification.user

        return self.execute_in_transaction(_verify)


class TwoFactorService(BaseService[TwoFactorDeviceRepository]):
    """Service handling two-factor authentication operations."""

    def __init__(self, repository: TwoFactorDeviceRepository = None) -> None:
        super().__init__(repository or TwoFactorDeviceRepository())

    def generate_secret(self) -> str:
        """Generate a new TOTP secret."""
        return secrets.token_hex(20)

    def setup_2fa(self, user: User, device_name: str) -> str:
        """Set up 2FA for a user and return the TOTP secret."""
        secret = secrets.token_hex(20)
        def _setup():
            self.repository.create_device(user=user, name=device_name, secret=secret)
            AuditLogService().log(
                action=AuditAction.TWO_FACTOR_ENABLE,
                user=user,
                resource=f"User: {user.username}",
                details=f"2FA device '{device_name}' ditambahkan.",
            )
        self.execute_in_transaction(_setup)
        return secret

    def verify_token(self, user: User, token: str) -> bool:
        """Verify a TOTP token for a user."""
        device = self.repository.get_by_user(user)
        if not device:
            return False
        return device.verify_token(token)

    def disable_2fa(self, user: User) -> bool:
        """Disable 2FA for a user."""
        device = self.repository.get_by_user(user)
        if not device:
            return False
        def _disable():
            self.repository.delete(device)
            user.two_factor_enabled = False
            user.save(update_fields=['two_factor_enabled'])
            AuditLogService().log(
                action=AuditAction.TWO_FACTOR_DISABLE,
                user=user,
                resource=f"User: {user.username}",
                details="2FA dinonaktifkan.",
            )
        self.execute_in_transaction(_disable)
        return True


class UserProfileService(BaseService[UserProfileRepository]):
    """Service handling user profile operations."""

    def __init__(self, repository: UserProfileRepository = None) -> None:
        super().__init__(repository or UserProfileRepository())

    def get_or_create_profile(self, user: User):
        """Get or create a user profile."""
        return self.repository.get_or_create(user)

    def update_avatar(self, user: User, avatar_file) -> None:
        """Update the user's avatar."""
        profile, _ = self.repository.get_or_create(user)
        profile.avatar = avatar_file
        profile.save(update_fields=['avatar'])
