from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from utils.choices import UserRole
import logging

security_logger = logging.getLogger('security')

class RoleRequiredMixin(UserPassesTestMixin):
    """View mixin to restrict access based on a list of approved UserRole choices."""

    allowed_roles: list[UserRole] = []

    def test_func(self) -> bool:
        user = self.request.user
        if not user.is_authenticated:
            return False

        # Superusers bypass all permission checks
        if user.is_superuser:
            return True

        # Check if user role matches allowed roles
        user_role = getattr(user, 'role', None)
        if user_role in self.allowed_roles:
            return True

        # Log unauthorized access attempts
        ip_addr = self.request.META.get('REMOTE_ADDR', 'UnknownIP')
        security_logger.warning(
            f"[UNAUTHORIZED ACCESS ATTEMPT] User: {user.username} (Role: {user_role}) "
            f"tried to access {self.request.path} from IP: {ip_addr}"
        )
        return False

    def handle_no_permission(self) -> None:
        """Raise a 403 Forbidden exception to render the custom 403 error page."""
        raise PermissionDenied("Anda tidak memiliki izin untuk mengakses halaman ini.")
