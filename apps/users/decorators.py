import logging
import secrets
from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from utils.choices import UserRole, AccountStatus

security_logger = logging.getLogger('security')


def login_required_custom(view_func):
    """Decorator to require authentication and check account status."""
    @wraps(view_func)
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.user.is_authenticated:
            messages.warning(request, "Anda harus login terlebih dahulu.")
            return redirect(f"{reverse('users:login')}?next={request.path}")

        if not request.user.is_active:
            messages.error(request, "Akun Anda tidak aktif.")
            return redirect('users:login')

        if request.user.is_suspended:
            messages.error(request, "Akun Anda ditangguhkan. Hubungi administrator.")
            return redirect('users:login')

        if request.user.is_account_locked:
            messages.error(request, "Akun Anda dikunci sementara karena terlalu banyak percobaan login gagal.")
            return redirect('users:login')

        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(*allowed_roles):
    """Decorator to restrict access based on user role.

    Usage:
        @role_required(UserRole.ADMINISTRATOR, UserRole.SUPERUSER)
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            if not request.user.is_authenticated:
                return redirect(f"{reverse('users:login')}?next={request.path}")

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            user_role = getattr(request.user, 'role', None)
            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)

            ip_addr = request.META.get('REMOTE_ADDR', 'UnknownIP')
            security_logger.warning(
                f"[UNAUTHORIZED ACCESS] User: {request.user.username} (Role: {user_role}) "
                f"tried to access {request.path} from IP: {ip_addr}"
            )
            messages.error(request, "Anda tidak memiliki izin untuk mengakses halaman ini.")
            return redirect('core:home')
        return wrapper
    return decorator


def admin_required(view_func):
    """Decorator to restrict access to administrators and superusers."""
    @wraps(view_func)
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect(f"{reverse('users:login')}?next={request.path}")

        if request.user.is_superuser or request.user.role == UserRole.ADMINISTRATOR:
            return view_func(request, *args, **kwargs)

        ip_addr = request.META.get('REMOTE_ADDR', 'UnknownIP')
        security_logger.warning(
            f"[UNAUTHORIZED ADMIN ACCESS] User: {request.user.username} "
            f"tried to access {request.path} from IP: {ip_addr}"
        )
        messages.error(request, "Hanya administrator yang dapat mengakses halaman ini.")
        return redirect('core:home')
    return wrapper


def email_verified_required(view_func):
    """Decorator to require verified email before accessing a view."""
    @wraps(view_func)
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect(f"{reverse('users:login')}?next={request.path}")

        if not request.user.email_verified:
            messages.warning(request, "Anda harus memverifikasi email terlebih dahulu.")
            return redirect('users:verify_email_notice')

        return view_func(request, *args, **kwargs)
    return wrapper


def guest_only(view_func):
    """Decorator to prevent authenticated users from accessing guest-only pages (login, register)."""
    @wraps(view_func)
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('core:home')
        return view_func(request, *args, **kwargs)
    return wrapper


def force_password_change_required(view_func):
    """Decorator to redirect users who must change their password."""
    @wraps(view_func)
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated and request.user.force_password_change:
            if request.resolver_match.url_name != 'change_password':
                messages.warning(request, "Anda wajib mengganti password sebelum melanjutkan.")
                return redirect('users:change_password')
        return view_func(request, *args, **kwargs)
    return wrapper


def generate_verification_token() -> str:
    """Generate a cryptographically secure token for email verification."""
    return secrets.token_hex(32)
