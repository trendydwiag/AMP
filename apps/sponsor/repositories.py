from typing import Optional, List
from django.utils import timezone
from utils.repositories import BaseRepository
from .models import Partner, Advertisement


class PartnerRepository(BaseRepository):
    model = Partner

    def get_active(self):
        return self.model.objects.filter(active=True)

    def get_featured(self):
        return self.model.objects.filter(featured=True, active=True)

    def get_by_type(self, partner_type: str):
        return self.model.objects.filter(partner_type=partner_type, active=True)

    def get_by_tier(self, tier: str):
        return self.model.objects.filter(tier=tier, active=True)

    def get_by_slug(self, slug: str) -> Optional[Partner]:
        try:
            return self.model.objects.get(slug=slug)
        except self.model.DoesNotExist:
            return None


class AdvertisementRepository(BaseRepository):
    model = Advertisement

    def get_active(self):
        now = timezone.now()
        return self.model.objects.filter(
            active=True
        ).filter(
            start_date__isnull=True
        ) | self.model.objects.filter(
            active=True,
            start_date__lte=now
        ).filter(
            end_date__isnull=True
        ) | self.model.objects.filter(
            active=True,
            start_date__lte=now,
            end_date__gte=now
        )

    def get_by_type(self, ad_type: str):
        return self.model.objects.filter(ad_type=ad_type, active=True)

    def get_by_position(self, position: str):
        return self.model.objects.filter(position__iexact=position, active=True)

    def increment_impressions(self, ad_id) -> Optional[Advertisement]:
        ad = self.get_by_id(ad_id)
        if ad:
            self.model.objects.filter(pk=ad_id).update(impressions=models.F('impressions') + 1)
            ad.refresh_from_db()
            return ad
        return None

    def increment_clicks(self, ad_id) -> Optional[Advertisement]:
        ad = self.get_by_id(ad_id)
        if ad:
            self.model.objects.filter(pk=ad_id).update(clicks=models.F('clicks') + 1)
            ad.refresh_from_db()
            return ad
        return None
