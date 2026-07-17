from django.http import HttpRequest, HttpResponse
import logging

security_logger = logging.getLogger('security')

class AuditLoggingMiddleware:
    """Middleware to audit log write actions (POST/PUT/DELETE) and attach client IP address to request users."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # 1. Capture Client IP address securely
        ip_addr = self._get_client_ip(request)
        
        # Attach IP address to user object for downstream mixin logging
        if request.user:
            request.user._ip_address = ip_addr

        response = self.get_response(request)

        # 2. Audit write/modifying actions
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']:
            # Avoid logging sensitive payloads (e.g. passwords). Only log paths, response status, and user
            username = request.user.username if request.user and request.user.is_authenticated else "Anonymous"
            path = request.path
            status = response.status_code
            method = request.method
            
            # Log admin login actions specifically
            if "/admin/login/" in path and method == "POST":
                # Write login attempt details
                security_logger.info(
                    f"[LOGIN ATTEMPT] Username: {request.POST.get('username', 'Unknown')} | IP: {ip_addr} | Status: {status}"
                )
            else:
                security_logger.info(
                    f"[AUDIT] Method: {method} | Path: {path} | User: {username} | IP: {ip_addr} | Status: {status}"
                )

        return response

    def _get_client_ip(self, request: HttpRequest) -> str:
        """Resolve client IP addressing resolving upstream proxies."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        return ip
