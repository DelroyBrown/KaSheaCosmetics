# KaSheaCosmetics_subscriptions\models.py
from django.db import models
from KaSheaCosmetics_products.models import Product


class CustomerEmails(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="customer_emails"
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Customer Email"
        verbose_name_plural = "Customer Emails"


    def __str__(self):
        return f"Email from {self.name} regarding {self.product.name}"


