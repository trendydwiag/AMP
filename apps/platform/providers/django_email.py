import logging
from typing import Any, Dict, List
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail, EmailMessage
from .base import EmailProvider, ProviderResult

logger = logging.getLogger('platform')


class DjangoEmailProvider(EmailProvider):
    """Default Django email backend provider."""

    name = 'django'
    description = 'Django SMTP email backend (default)'

    def __init__(self):
        self.from_email = ''
        self.use_tls = True
        self.host = ''
        self.port = 587

    def configure(self, config: Dict[str, Any]) -> None:
        self.from_email = config.get(
            'from_email',
            getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
        )
        self.host = config.get('email_host', getattr(settings, 'EMAIL_HOST', ''))
        self.port = config.get('email_port', getattr(settings, 'EMAIL_PORT', 587))
        self.use_tls = config.get('email_use_tls', getattr(settings, 'EMAIL_USE_TLS', True))

    def send(self, to: str, subject: str, body: str, **kwargs) -> ProviderResult:
        try:
            result = send_mail(
                subject=subject,
                message=body,
                from_email=self.from_email,
                recipient_list=[to],
                fail_silently=False,
            )
            return ProviderResult(
                success=result == 1,
                data={'sent_count': result},
                provider_name=self.name
            )
        except Exception as e:
            logger.error(f"Email send error: {e}")
            return ProviderResult(success=False, error=str(e), provider_name=self.name)

    def send_html(self, to: str, subject: str, html_body: str, **kwargs) -> ProviderResult:
        try:
            msg = EmailMessage(
                subject=subject,
                body=html_body,
                from_email=self.from_email,
                to=[to],
            )
            msg.content_subtype = 'html'
            result = msg.send(fail_silently=False)
            return ProviderResult(
                success=result == 1,
                data={'sent': result == 1},
                provider_name=self.name
            )
        except Exception as e:
            logger.error(f"HTML email send error: {e}")
            return ProviderResult(success=False, error=str(e), provider_name=self.name)

    def send_bulk(self, recipients: List[Dict[str, Any]], subject: str, body: str, **kwargs) -> ProviderResult:
        try:
            messages = []
            for recipient in recipients:
                to_email = recipient.get('email', '')
                personal_body = recipient.get('body', body)
                messages.append((
                    subject,
                    personal_body,
                    self.from_email,
                    [to_email],
                ))
            result = send_mass_mail(messages, fail_silently=False)
            return ProviderResult(
                success=True,
                data={'sent_count': result},
                provider_name=self.name
            )
        except Exception as e:
            logger.error(f"Bulk email error: {e}")
            return ProviderResult(success=False, error=str(e), provider_name=self.name)

    def health_check(self) -> ProviderResult:
        try:
            return ProviderResult(
                success=True,
                data={'host': self.host, 'port': self.port, 'tls': self.use_tls},
                provider_name=self.name
            )
        except Exception as e:
            return ProviderResult(success=False, error=str(e), provider_name=self.name)
