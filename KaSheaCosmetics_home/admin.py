# KaSheaCosmetics_home\admin.py
from unfold.admin import ModelAdmin
from django.contrib import admin
from KaSheaCosmetics_home.CommonModels.models import specialOffer, TopBannerMessage


@admin.register(TopBannerMessage)
class TopBannerMessageAdmin(ModelAdmin):
    list_display = ("banner_name", "banner_description", "created_at")


@admin.register(specialOffer)
class SpecialOfferAdmin(ModelAdmin):
    list_display = ("offer_name", "created_at")
