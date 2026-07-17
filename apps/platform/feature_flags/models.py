import logging
from django.db import models
from django.utils import timezone
from utils.mixins import UUIDPrimaryKeyMixin, TimeStampedModel
from apps.platform.choices import FeatureFlagScope

logger = logging.getLogger('platform')


class FeatureFlag(UUIDPrimaryKeyMixin, TimeStampedModel):
    """Global or partner-specific feature flag.

    Flags control availability of platform features. Can be scoped globally
    (all partners) or to specific partners via FeatureFlagPartner.

    Example flags:
    - podcast, community, ai, advertisement, membership, donation,
      analytics, themes, plugins, live_streaming, newsletter
    """

    key = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique feature key (snake_case)."
    )
    name = models.CharField(
        max_length=200,
        help_text="Display name of the feature."
    )
    description = models.TextField(
        blank=True,
        default=''
    )
    scope = models.CharField(
        max_length=20,
        choices=FeatureFlagScope.choices,
        default=FeatureFlagScope.GLOBAL
    )
    is_enabled = models.BooleanField(
        default=False,
        help_text="Global on/off switch for this feature."
    )
    rollout_percentage = models.PositiveIntegerField(
        default=100,
        help_text="Percentage of partners this feature is enabled for (0-100)."
    )
    config = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional configuration for this feature."
    )
    category = models.CharField(
        max_length=50,
        blank=True,
        default='',
        help_text="Feature category for grouping in UI."
    )
    required_tier = models.CharField(
        max_length=20,
        blank=True,
        default='',
        help_text="Minimum partner tier required. Empty = available to all."
    )

    class Meta:
        verbose_name = 'Fitur'
        verbose_name_plural = 'Fitur'
        ordering = ['category', 'key']

    def __str__(self) -> str:
        status = 'ON' if self.is_enabled else 'OFF'
        return f"{self.name} [{status}]"

    def is_available_for_partner(self, partner=None) -> bool:
        """Check if this feature is available for a specific partner."""
        if not self.is_enabled:
            return False

        # Check tier requirement
        if self.required_tier and partner:
            from apps.platform.choices import PartnerTier
            tier_order = {
                PartnerTier.COMMUNITY: 0,
                PartnerTier.STARTER: 1,
                PartnerTier.PROFESSIONAL: 2,
                PartnerTier.ENTERPRISE: 3,
            }
            partner_level = tier_order.get(partner.tier, 0)
            required_level = tier_order.get(self.required_tier, 0)
            if partner_level < required_level:
                return False

        # Check FeatureFlagPartner table
        if partner:
            try:
                override = FeatureFlagPartner.objects.get(
                    flag=self, partner=partner
                )
                return override.is_enabled
            except FeatureFlagPartner.DoesNotExist:
                pass

        # Check partner_overrides JSON on the partner object
        if partner and hasattr(partner, 'has_feature'):
            partner_override = partner.feature_overrides.get(self.key)
            if partner_override is not None:
                return bool(partner_override)

        return True


class FeatureFlagPartner(UUIDPrimaryKeyMixin, TimeStampedModel):
    """Partner-specific override for a feature flag.

    When a flag is PARTNER-scoped, this table controls which partners
    have the feature enabled/disabled.
    """

    flag = models.ForeignKey(
        FeatureFlag,
        on_delete=models.CASCADE,
        related_name='partner_overrides'
    )
    partner = models.ForeignKey(
        'platform.Partner',
        on_delete=models.CASCADE,
        related_name='feature_flag_overrides'
    )
    is_enabled = models.BooleanField(
        default=True,
        help_text="Override: enable or disable this feature for this partner."
    )
    config = models.JSONField(
        default=dict,
        blank=True,
        help_text="Partner-specific config override."
    )

    class Meta:
        verbose_name = 'Override Fitur Partner'
        verbose_name_plural = 'Override Fitur Partner'
        unique_together = ['flag', 'partner']

    def __str__(self) -> str:
        status = 'ON' if self.is_enabled else 'OFF'
        return f"{self.flag.key} -> {self.partner.name} [{status}]"


class FeatureFlagLog(UUIDPrimaryKeyMixin, TimeStampedModel):
    """Audit log for feature flag changes."""

    flag = models.ForeignKey(
        FeatureFlag,
        on_delete=models.CASCADE,
        related_name='change_logs'
    )
    action = models.CharField(max_length=50)
    old_value = models.JSONField(default=dict, blank=True)
    new_value = models.JSONField(default=dict, blank=True)
    changed_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='feature_flag_changes'
    )
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Log Perubahan Fitur'
        verbose_name_plural = 'Log Perubahan Fitur'
        ordering = ['-changed_at']
