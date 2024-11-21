# KaSheaCosmetics_orders\admin.py
from django.contrib import admin
from .models import Order, OrderItem
from unfold.admin import TabularInline, ModelAdmin


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    


class OrderAdmin(ModelAdmin):
    list_display = [
        "id",
        "customer_name",
        "email",
        "amount",
        "status",
        "created_at"
        ]
    inlines = [OrderItemInline]
    readonly_fields = [
        'customer_name',
        'email',
        'shipping_address',
        'shipping_city',
        'shipping_postcode',
        'shipping_country',
        'amount',
        'status',
        'stripe_payment_intent_id',
    ]


admin.site.register(Order, OrderAdmin)
