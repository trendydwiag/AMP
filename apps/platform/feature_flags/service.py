import logging
from typing import Optional
from django.core.cache import cache
from .models import FeatureFlag, FeatureFlagPartner

logger = logging.getLogger('platform')

CACHE_TTL = 300  # 5 minutes
CACHE_PREFIX = 'feature_flag:'


class FeatureFlagService:
    """Service for checking and managing feature flags.

    Uses caching to avoid repeated DB queries.
    """

    def is_enabled(self, key: str, partner=None) -> bool:
        """Check if a feature flag is enabled for a given partner."""
        cache_key = f"{CACHE_PREFIX}{key}:{partner.pk if partner else 'global'}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            flag = FeatureFlag.objects.get(key=key)
        except FeatureFlag.DoesNotExist:
            logger.debug(f"Feature flag '{key}' not found, defaulting to False")
            return False

        result = flag.is_available_for_partner(partner)
        cache.set(cache_key, result, CACHE_TTL)
        return result

    def get_config(self, key: str, partner=None) -> dict:
        """Get feature configuration, merging global and partner-specific config."""
        try:
            flag = FeatureFlag.objects.get(key=key)
        except FeatureFlag.DoesNotExist:
            return {}

        config = dict(flag.config)

        if partner:
            try:
                override = FeatureFlagPartner.objects.get(
                    flag=flag, partner=partner
                )
                config.update(override.config)
            except FeatureFlagPartner.DoesNotExist:
                pass

        return config

    def get_enabled_features(self, partner=None) -> list[str]:
        """Get all enabled feature keys for a partner."""
        flags = FeatureFlag.objects.filter(is_enabled=True)
        return [
            flag.key for flag in flags
            if flag.is_available_for_partner(partner)
        ]

    def enable(self, key: str, changed_by=None) -> bool:
        """Enable a global feature flag."""
        try:
            flag = FeatureFlag.objects.get(key=key)
            old_value = {'is_enabled': flag.is_enabled}
            flag.is_enabled = True
            flag.save(update_fields=['is_enabled', 'updated_at'])
            self._log_change(flag, 'ENABLED', old_value, {'is_enabled': True}, changed_by)
            cache.delete(f"{CACHE_PREFIX}{key}:global")
            return True
        except FeatureFlag.DoesNotExist:
            return False

    def disable(self, key: str, changed_by=None) -> bool:
        """Disable a global feature flag."""
        try:
            flag = FeatureFlag.objects.get(key=key)
            old_value = {'is_enabled': flag.is_enabled}
            flag.is_enabled = False
            flag.save(update_fields=['is_enabled', 'updated_at'])
            self._log_change(flag, 'DISABLED', old_value, {'is_enabled': False}, changed_by)
            cache.delete(f"{CACHE_PREFIX}{key}:global")
            return True
        except FeatureFlag.DoesNotExist:
            return False

    def set_for_partner(self, key: str, partner, enabled: bool, changed_by=None) -> bool:
        """Set a feature flag for a specific partner."""
        try:
            flag = FeatureFlag.objects.get(key=key)
            override, created = FeatureFlagPartner.objects.update_or_create(
                flag=flag,
                partner=partner,
                defaults={
                    'is_enabled': enabled,
                }
            )
            cache.delete(f"{CACHE_PREFIX}{key}:{partner.pk}")
            self._log_change(
                flag, f'PARTNER_{"ENABLED" if enabled else "DISABLED"}',
                {}, {'partner': str(partner), 'enabled': enabled}, changed_by
            )
            return True
        except FeatureFlag.DoesNotExist:
            return False

    def clear_cache(self, key: str = None):
        """Clear feature flag cache."""
        if key:
            # Clear all partner variations - use pattern delete
            cache.delete_pattern(f"{CACHE_PREFIX}{key}:*")
        else:
            cache.delete_pattern(f"{CACHE_PREFIX}*")

    def _log_change(self, flag, action, old_value, new_value, changed_by):
        from .models import FeatureFlagLog
        FeatureFlagLog.objects.create(
            flag=flag,
            action=action,
            old_value=old_value,
            new_value=new_value,
            changed_by=changed_by,
        )
