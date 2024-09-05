# KaSheaCosmetics_orders\admin.py
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "customer_name", "email", "amount", "status", "created_at"]
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
