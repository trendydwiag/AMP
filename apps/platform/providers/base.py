from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class ProviderResult:
    """Standard result wrapper for all provider operations."""
    success: bool = True
    data: Any = None
    error: str = ''
    provider_name: str = ''
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseProvider(ABC):
    """Abstract base class for all platform providers.

    Each provider category (streaming, storage, email, etc.)
    implements this interface with concrete logic.
    """

    category: str = ''
    name: str = ''
    description: str = ''

    @abstractmethod
    def configure(self, config: Dict[str, Any]) -> None:
        """Configure the provider with partner-specific settings."""
        ...

    @abstractmethod
    def health_check(self) -> ProviderResult:
        """Check if the provider is reachable and operational."""
        ...

    def get_info(self) -> Dict[str, Any]:
        """Return provider metadata."""
        return {
            'category': self.category,
            'name': self.name,
            'description': self.description,
        }


class StreamingProvider(BaseProvider):
    """Abstract interface for audio streaming providers."""

    category = 'STREAMING'

    @abstractmethod
    def get_stream_url(self) -> ProviderResult:
        """Get the current active stream URL."""
        ...

    @abstractmethod
    def get_now_playing(self) -> ProviderResult:
        """Get current track metadata."""
        ...

    @abstractmethod
    def get_listener_count(self) -> ProviderResult:
        """Get current listener count."""
        ...

    @abstractmethod
    def check_health(self) -> ProviderResult:
        """Check stream health status."""
        ...


class StorageProvider(BaseProvider):
    """Abstract interface for file storage providers."""

    category = 'STORAGE'

    @abstractmethod
    def upload(self, file_obj: Any, path: str, **kwargs) -> ProviderResult:
        """Upload a file to storage."""
        ...

    @abstractmethod
    def delete(self, path: str) -> ProviderResult:
        """Delete a file from storage."""
        ...

    @abstractmethod
    def get_url(self, path: str, **kwargs) -> ProviderResult:
        """Get a public/download URL for a file."""
        ...

    @abstractmethod
    def get_usage(self) -> ProviderResult:
        """Get storage usage statistics."""
        ...

    def get_signed_url(self, path: str, expires_in: int = 3600) -> ProviderResult:
        """Generate a signed/temporary URL. Override in providers that support it."""
        return self.get_url(path)


class EmailProvider(BaseProvider):
    """Abstract interface for email delivery providers."""

    category = 'EMAIL'

    @abstractmethod
    def send(self, to: str, subject: str, body: str, **kwargs) -> ProviderResult:
        """Send an email message."""
        ...

    @abstractmethod
    def send_html(self, to: str, subject: str, html_body: str, **kwargs) -> ProviderResult:
        """Send an HTML email message."""
        ...

    @abstractmethod
    def send_bulk(self, recipients: list[Dict[str, Any]], subject: str, body: str, **kwargs) -> ProviderResult:
        """Send bulk emails."""
        ...


class AIProvider(BaseProvider):
    """Abstract interface for AI/ML service providers."""

    category = 'AI'

    @abstractmethod
    def generate_text(self, prompt: str, **kwargs) -> ProviderResult:
        """Generate text from a prompt."""
        ...

    @abstractmethod
    def summarize(self, text: str, **kwargs) -> ProviderResult:
        """Summarize a piece of text."""
        ...

    @abstractmethod
    def transcribe(self, audio_path: str, **kwargs) -> ProviderResult:
        """Transcribe audio to text."""
        ...

    def translate(self, text: str, target_lang: str = 'id', **kwargs) -> ProviderResult:
        """Translate text to target language."""
        return ProviderResult(
            success=False,
            error='Translation not supported by this provider'
        )


class NotificationProvider(BaseProvider):
    """Abstract interface for push notification providers."""

    category = 'NOTIFICATION'

    @abstractmethod
    def send_push(self, user_id: str, title: str, body: str, **kwargs) -> ProviderResult:
        """Send a push notification to a user."""
        ...

    @abstractmethod
    def send_bulk_push(self, user_ids: list[str], title: str, body: str, **kwargs) -> ProviderResult:
        """Send bulk push notifications."""
        ...

    @abstractmethod
    def send_sms(self, phone: str, message: str, **kwargs) -> ProviderResult:
        """Send an SMS message."""
        ...


class AnalyticsProvider(BaseProvider):
    """Abstract interface for analytics providers."""

    category = 'ANALYTICS'

    @abstractmethod
    def track_event(self, event_name: str, properties: Dict[str, Any], **kwargs) -> ProviderResult:
        """Track a custom analytics event."""
        ...

    @abstractmethod
    def get_pageviews(self, start_date: str, end_date: str, **kwargs) -> ProviderResult:
        """Get pageview data for a date range."""
        ...

    @abstractmethod
    def get_visitor_stats(self, **kwargs) -> ProviderResult:
        """Get visitor statistics."""
        ...

    def get_realtime(self, **kwargs) -> ProviderResult:
        """Get realtime visitor data. Override in providers that support it."""
        return ProviderResult(
            success=False,
            error='Realtime analytics not supported'
        )


class PaymentProvider(BaseProvider):
    """Abstract interface for payment providers (future)."""

    category = 'PAYMENT'

    @abstractmethod
    def create_payment(self, amount: float, currency: str, **kwargs) -> ProviderResult:
        """Create a payment intent."""
        ...

    @abstractmethod
    def verify_payment(self, payment_id: str, **kwargs) -> ProviderResult:
        """Verify a payment status."""
        ...

    def refund(self, payment_id: str, **kwargs) -> ProviderResult:
        """Process a refund. Override in providers that support it."""
        return ProviderResult(
            success=False,
            error='Refund not supported'
        )
