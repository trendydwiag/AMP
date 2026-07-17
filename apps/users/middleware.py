from datetime import timedelta

from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse
from django.utils import timezone

from apps.users.repositories import UserRepository, AuditLogRepository
from utils.choices import AuditAction

import logging

security_logger = logging.getLogger('security')


class SessionTimeoutMiddleware:
    """Middleware that automatically logs out users after a period of inactivity."""

    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.timeout_minutes = getattr(settings, 'SESSION_TIMEOUT_MINUTES', 60)

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                last_activity_time = timezone.datetime.fromisoformat(last_activity)
                if timezone.now() - last_activity_time > timedelta(minutes=self.timeout_minutes):
                    security_logger.info(
                        f"[SESSION TIMEOUT] User: {request.user.username} | IP: {request.META.get('REMOTE_ADDR', 'Unknown')}"
                    )
                    logout(request)
                    from django.contrib import messages
                    messages.warning(request, "Sesi Anda telah berakhir karena tidak ada aktivitas.")
                    return HttpResponse(
                        status=302,
                        headers={'Location': f"/akun/masuk/?next={request.path}"},
                    )
            request.session['last_activity'] = timezone.now().isoformat()

        return self.get_response(request)


class LastActivityMiddleware:
    """Middleware that updates user's last_activity timestamp on each request."""

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)

        if request.user.is_authenticated:
            now = timezone.now()
            if not request.user.last_activity or \
               (now - request.user.last_activity).total_seconds() > 60:
                UserRepository().update_last_activity(request.user)

        return response


class TrackLoginMiddleware:
    """Middleware that enhances login tracking with IP and user-agent capture."""

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)

        if request.path == '/akun/masuk/' and request.method == 'POST':
            from apps.users.repositories import LoginHistoryRepository
            from utils.choices import LoginStatus

            username = request.POST.get('username', '')
            ip_addr = self._get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]

            if hasattr(request, '_login_tracked'):
                return response

            if response.status_code == 302:
                login_repo = LoginHistoryRepository()
                user_repo = UserRepository()
                user = user_repo.get_by_username(username)
                login_repo.record_attempt(
                    username_attempted=username,
                    ip_address=ip_addr,
                    status=LoginStatus.SUCCESS,
                    user_agent=user_agent,
                    user=user,
                )
                request._login_tracked = True

        return response

    def _get_client_ip(self, request: HttpRequest) -> str:
        """Resolve client IP address respecting upstream proxies."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '127.0.0.1')
