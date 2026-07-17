from typing import Optional, List
from django.db.models import QuerySet
from django.utils import timezone

from utils.repositories import BaseRepository
from apps.users.models import (
    User, UserProfile, LoginHistory, PasswordHistory,
    AuditLog, EmailVerification, TwoFactorDevice,
)
from django.core.exceptions import ObjectDoesNotExist


class UserRepository(BaseRepository[User]):
    """Repository handling database operations for the User model."""

    model = User

    def get_by_username(self, username: str) -> Optional[User]:
        """Retrieve user by exact username."""
        try:
            return self.model.objects.get(username=username)
        except ObjectDoesNotExist:
            return None

    def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve user by exact email (case-insensitive)."""
        try:
            return self.model.objects.get(email__iexact=email)
        except ObjectDoesNotExist:
            return None

    def list_active(self) -> List[User]:
        """Fetch all active users."""
        return list(self.model.objects.filter(is_active=True))

    def list_by_role(self, role: str) -> List[User]:
        """Fetch all users with the specified role."""
        return list(self.model.objects.filter(role=role))

    def search(self, query: str) -> QuerySet:
        """Search users by username, email, or name."""
        return self.model.objects.filter(
            models.Q(username__icontains=query) |
            models.Q(email__icontains=query) |
            models.Q(first_name__icontains=query) |
            models.Q(last_name__icontains=query)
        )

    def update_last_activity(self, user: User) -> None:
        """Update the user's last activity timestamp."""
        user.last_activity = timezone.now()
        user.save(update_fields=['last_activity'])


class UserProfileRepository(BaseRepository[UserProfile]):
    """Repository handling database operations for the UserProfile model."""

    model = UserProfile

    def get_by_user(self, user: User) -> Optional[UserProfile]:
        """Retrieve profile by user instance."""
        try:
            return self.model.objects.get(user=user)
        except ObjectDoesNotExist:
            return None

    def get_or_create(self, user: User) -> tuple:
        """Get existing profile or create a new one."""
        return self.model.objects.get_or_create(user=user)


class LoginHistoryRepository(BaseRepository[LoginHistory]):
    """Repository handling database operations for the LoginHistory model."""

    model = LoginHistory

    def record_attempt(
        self,
        username_attempted: str,
        ip_address: str,
        status: str,
        user_agent: str = '',
        failure_reason: str = '',
        user: Optional[User] = None,
    ) -> LoginHistory:
        """Record a login attempt."""
        return self.create(
            user=user,
            username_attempted=username_attempted,
            ip_address=ip_address,
            user_agent=user_agent,
            status=status,
            failure_reason=failure_reason,
        )

    def get_user_history(self, user: User, limit: int = 50) -> List[LoginHistory]:
        """Fetch recent login history for a specific user."""
        return list(self.model.objects.filter(user=user)[:limit])

    def get_recent_by_username(self, username: str, limit: int = 10) -> List[LoginHistory]:
        """Fetch recent login attempts for a username."""
        return list(self.model.objects.filter(username_attempted=username)[:limit])


class PasswordHistoryRepository(BaseRepository[PasswordHistory]):
    """Repository handling database operations for the PasswordHistory model."""

    model = PasswordHistory

    def record_password(self, user: User, hashed_password: str) -> PasswordHistory:
        """Record a password in history."""
        return self.create(user=user, password=hashed_password)

    def get_recent_passwords(self, user: User, limit: int = 5) -> List[PasswordHistory]:
        """Fetch the most recent passwords for a user."""
        return list(self.model.objects.filter(user=user)[:limit])

    def is_password_reused(self, user: User, raw_password: str, limit: int = 5) -> bool:
        """Check if a password hash matches any recently stored password."""
        from django.contrib.hashers import check_password
        recent = self.model.objects.filter(user=user)[:limit]
        for entry in recent:
            if check_password(raw_password, entry.password):
                return True
        return False


class AuditLogRepository(BaseRepository[AuditLog]):
    """Repository handling database operations for the AuditLog model."""

    model = AuditLog

    def log(
        self,
        action: str,
        user: Optional[User] = None,
        resource: str = '',
        details: str = '',
        ip_address: Optional[str] = None,
    ) -> AuditLog:
        """Create an audit log entry."""
        return self.create(
            user=user,
            action=action,
            resource=resource,
            details=details,
            ip_address=ip_address,
        )

    def get_user_logs(self, user: User, limit: int = 100) -> List[AuditLog]:
        """Fetch audit logs for a specific user."""
        return list(self.model.objects.filter(user=user)[:limit])

    def get_by_action(self, action: str, limit: int = 100) -> List[AuditLog]:
        """Fetch audit logs filtered by action type."""
        return list(self.model.objects.filter(action=action)[:limit])


class EmailVerificationRepository(BaseRepository[EmailVerification]):
    """Repository handling database operations for the EmailVerification model."""

    model = EmailVerification

    def get_valid_token(self, token: str) -> Optional[EmailVerification]:
        """Retrieve an unexpired, unverified token."""
        try:
            obj = self.model.objects.get(token=token)
            if obj.is_valid:
                return obj
            return None
        except ObjectDoesNotExist:
            return None

    def create_for_user(self, user: User, expires_hours: int = 48) -> EmailVerification:
        """Generate and save a new verification token for the user."""
        token = EmailVerification.generate_token()
        expires_at = timezone.now() + timezone.timedelta(hours=expires_hours)
        return self.create(user=user, token=token, expires_at=expires_at)

    def revoke_all(self, user: User) -> None:
        """Mark all existing tokens for a user as verified (invalidated)."""
        self.model.objects.filter(user=user, verified=False).update(verified=True)


class TwoFactorDeviceRepository(BaseRepository[TwoFactorDevice]):
    """Repository handling database operations for the TwoFactorDevice model."""

    model = TwoFactorDevice

    def get_by_user(self, user: User) -> Optional[TwoFactorDevice]:
        """Retrieve the primary 2FA device for a user."""
        try:
            return self.model.objects.get(user=user, is_primary=True)
        except ObjectDoesNotExist:
            return None

    def get_all_by_user(self, user: User) -> List[TwoFactorDevice]:
        """Retrieve all 2FA devices for a user."""
        return list(self.model.objects.filter(user=user))

    def create_device(self, user: User, name: str, secret: str) -> TwoFactorDevice:
        """Create a new 2FA device for a user."""
        existing = self.model.objects.filter(user=user).exists()
        return self.create(user=user, name=name, secret=secret, is_primary=not existing)
