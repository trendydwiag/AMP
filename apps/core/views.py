from django.views.generic import TemplateView
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django.db import connection
import logging

logger = logging.getLogger('django')
security_logger = logging.getLogger('security')


class HomeView(TemplateView):
    """Homepage View showing core system overview or routing to modules."""
    
    template_name = 'core/home.html'


class OfflineView(TemplateView):
    """Offline fallback page served by the service worker."""
    template_name = 'offline.html'


def health_check(request: HttpRequest) -> JsonResponse:
    """Verifies critical system dependencies (PostgreSQL database) and returns system health status."""
    health_status = {
        'status': 'healthy',
        'database': 'operational',
        'timezone': 'operational'
    }
    
    # 1. Test Database Connection
    try:
        connection.ensure_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
    except Exception as e:
        logger.error(f"Health Check Database Failure: {str(e)}")
        health_status['status'] = 'unhealthy'
        health_status['database'] = 'down'

    status_code = 200 if health_status['status'] == 'healthy' else 503
    return JsonResponse(health_status, status=status_code)


# ==========================================
# Custom Error Handlers (Security Aligned)
# ==========================================

def bad_request(request: HttpRequest, exception: Exception = None, template_name: str = '400.html') -> HttpResponse:
    """Render Custom 400 Bad Request Page."""
    logger.warning(f"Bad Request (400): {request.path}")
    response = render(request, template_name, status=400)
    return response


def permission_denied(request: HttpRequest, exception: Exception = None, template_name: str = '403.html') -> HttpResponse:
    """Render Custom 403 Forbidden Page."""
    ip_addr = request.META.get('REMOTE_ADDR', 'UnknownIP')
    security_logger.warning(f"Permission Denied (403): User: {request.user} at {request.path} from IP: {ip_addr}")
    response = render(request, template_name, status=403)
    return response


def page_not_found(request: HttpRequest, exception: Exception = None, template_name: str = '404.html') -> HttpResponse:
    """Render Custom 404 Not Found Page."""
    logger.info(f"Page Not Found (404): {request.path}")
    response = render(request, template_name, status=404)
    return response


def server_error(request: HttpRequest, template_name: str = '500.html') -> HttpResponse:
    """Render Custom 500 Server Error Page."""
    logger.critical(f"Server Error (500) processing request: {request.path}", exc_info=True)
    response = render(request, template_name, status=500)
    return response
