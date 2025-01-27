# KaSheaCosmetics_home\admin.py
from django.contrib import admin
from KaSheaCosmetics_home.CommonModels.models import specialOffer, TopBannerMessage
from unfold.admin import ModelAdmin


@admin.register(TopBannerMessage)
class TopBannerMessageAdmin(ModelAdmin):
    list_display = ('banner_name', 'banner_description', 'created_at')


admin.site.register(specialOffer)
