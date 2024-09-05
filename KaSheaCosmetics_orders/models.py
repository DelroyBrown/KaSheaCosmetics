# KaSheaCosmetics_orders\models.py
from django.db import models
from KaSheaCosmetics_products.models import Product


class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    email = models.EmailField()
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=255)
    shipping_postcode = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)
    stripe_payment_intent_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
