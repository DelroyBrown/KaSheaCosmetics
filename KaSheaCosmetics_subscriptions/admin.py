# KaSheaCosmetics_subscriptions\admin.py
from django.contrib import admin
from .models import CustomerEmails


@admin.register(CustomerEmails)
class CustomerEmailsAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "product", "created_at")
    search_fields = ("email", "name", "product__name")
