import logging
from typing import Optional, List
from django.db import transaction
from django.db.models import F
from utils.services import BaseService
from .repositories import PartnerRepository, AdvertisementRepository
from .models import Partner, Advertisement

logger = logging.getLogger('sponsor')


class PartnerService(BaseService[PartnerRepository]):
    def __init__(self):
        super().__init__(PartnerRepository())

    def get_active_partners(self):
        return Partner.objects.filter(active=True)

    def get_featured_partners(self):
        return Partner.objects.filter(featured=True, active=True)

    def get_by_type(self, partner_type: str):
        return Partner.objects.filter(partner_type=partner_type, active=True)

    def get_by_tier(self, tier: str):
        return Partner.objects.filter(tier=tier, active=True)

    def get_by_slug(self, slug: str) -> Optional[Partner]:
        return self.repository.get_by_slug(slug)

    @transaction.atomic
    def create_partner(self, **kwargs) -> Partner:
        return self.repository.create(**kwargs)

    @transaction.atomic
    def update_partner(self, partner_id, **kwargs) -> Optional[Partner]:
        partner = self.repository.get_by_id(partner_id)
        if partner:
            return self.repository.update(partner, **kwargs)
        return None

    @transaction.atomic
    def delete_partner(self, partner_id) -> bool:
        partner = self.repository.get_by_id(partner_id)
        if partner:
            return self.repository.delete(partner)
        return False

    @transaction.atomic
    def toggle_active(self, partner_id) -> Optional[Partner]:
        partner = self.repository.get_by_id(partner_id)
        if partner:
            partner.active = not partner.active
            partner.save(update_fields=['active'])
            return partner
        return None

    @transaction.atomic
    def toggle_featured(self, partner_id) -> Optional[Partner]:
        partner = self.repository.get_by_id(partner_id)
        if partner:
            partner.featured = not partner.featured
            partner.save(update_fields=['featured'])
            return partner
        return None


class AdvertisementService(BaseService[AdvertisementRepository]):
    def __init__(self):
        super().__init__(AdvertisementRepository())

    def get_active_ads(self):
        return Advertisement.objects.filter(active=True)

    def get_by_type(self, ad_type: str):
        return Advertisement.objects.filter(ad_type=ad_type, active=True)

    def get_by_position(self, position: str):
        return Advertisement.objects.filter(position__iexact=position, active=True)

    @transaction.atomic
    def create_advertisement(self, **kwargs) -> Advertisement:
        return self.repository.create(**kwargs)

    @transaction.atomic
    def update_advertisement(self, ad_id, **kwargs) -> Optional[Advertisement]:
        ad = self.repository.get_by_id(ad_id)
        if ad:
            return self.repository.update(ad, **kwargs)
        return None

    @transaction.atomic
    def delete_advertisement(self, ad_id) -> bool:
        ad = self.repository.get_by_id(ad_id)
        if ad:
            return self.repository.delete(ad)
        return False

    @transaction.atomic
    def toggle_active(self, ad_id) -> Optional[Advertisement]:
        ad = self.repository.get_by_id(ad_id)
        if ad:
            ad.active = not ad.active
            ad.save(update_fields=['active'])
            return ad
        return None

    @transaction.atomic
    def increment_impressions(self, ad_id) -> Optional[Advertisement]:
        updated = Advertisement.objects.filter(pk=ad_id).update(impressions=F('impressions') + 1)
        if updated:
            return Advertisement.objects.get(pk=ad_id)
        return None

    @transaction.atomic
    def increment_clicks(self, ad_id) -> Optional[Advertisement]:
        updated = Advertisement.objects.filter(pk=ad_id).update(clicks=F('clicks') + 1)
        if updated:
            return Advertisement.objects.get(pk=ad_id)
        return None
