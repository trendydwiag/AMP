from django.contrib import admin
from .models import Partner, Advertisement


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'partner_type', 'tier', 'active', 'featured', 'display_order', 'created_at')
    list_filter = ('active', 'featured', 'partner_type', 'tier')
    search_fields = ('name', 'description', 'contact_email')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('display_order', 'active', 'featured')


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'ad_type', 'position', 'impressions', 'clicks', 'active', 'display_order', 'created_at')
    list_filter = ('active', 'ad_type')
    search_fields = ('title', 'position')
    list_editable = ('display_order', 'active')
    date_hierarchy = 'created_at'
