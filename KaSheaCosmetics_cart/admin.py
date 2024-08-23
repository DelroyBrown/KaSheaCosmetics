from django.contrib import admin
from .models import ShippingLocation


@admin.register(ShippingLocation)
class ShippingLocationAdmin(admin.ModelAdmin):
    list_display = ("city", "shipping_cost")
    search_fields = ("city",)
