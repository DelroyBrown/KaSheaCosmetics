# KaSheaCosmetics_cart\admin.py
from django.contrib import admin
from .models import ShippingLocation
from KaSheaCosmetics_products.models import DefaultShippingCost


@admin.register(ShippingLocation)
class ShippingLocationAdmin(admin.ModelAdmin):
    list_display = ("city", "shipping_cost")
    search_fields = ("city",)


@admin.register(DefaultShippingCost)
class DefaultShippingCostAdmin(admin.ModelAdmin):
    list_display = ("cost",)
    search_fields = ("cost",)
