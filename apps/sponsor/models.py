from django.db import models
from django.utils import timezone
from utils.mixins import UUIDPrimaryKeyMixin, TimeStampedModel


class Partner(UUIDPrimaryKeyMixin, TimeStampedModel):
    PARTNER_TYPE_CHOICES = [
        ('sponsor', 'Sponsor'),
        ('partner', 'Partner'),
        ('media_partner', 'Media Partner'),
    ]
    TIER_CHOICES = [
        ('platinum', 'Platinum'),
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    logo = models.ImageField(upload_to='sponsor/partners/', blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(max_length=500, blank=True)
    partner_type = models.CharField(
        max_length=20,
        choices=PARTNER_TYPE_CHOICES,
        default='partner'
    )
    tier = models.CharField(
        max_length=20,
        choices=TIER_CHOICES,
        default='silver'
    )
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'

    def __str__(self) -> str:
        return self.name


class Advertisement(UUIDPrimaryKeyMixin, TimeStampedModel):
    AD_TYPE_CHOICES = [
        ('banner', 'Banner'),
        ('sidebar', 'Sidebar'),
        ('popup', 'Popup'),
        ('footer', 'Footer'),
    ]

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='sponsor/ads/', blank=True)
    link_url = models.URLField(max_length=500, blank=True)
    ad_type = models.CharField(
        max_length=20,
        choices=AD_TYPE_CHOICES,
        default='banner'
    )
    position = models.CharField(max_length=50, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'title']
        verbose_name = 'Advertisement'
        verbose_name_plural = 'Advertisements'

    def __str__(self) -> str:
        return self.title

    @property
    def is_active(self) -> bool:
        if not self.active:
            return False
        now = timezone.now()
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True
