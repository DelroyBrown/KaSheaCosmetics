# KaSheaCosmetics_products\models.py
from django.db import models


class ShippingOption(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    category_name = models.CharField(
        max_length=100, blank=False, null=False, default=""
    )

    def __str__(self):
        return self.category_name


class Product(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, default="")
    description = models.TextField(blank=False, null=False, default="")
    size = models.CharField(max_length=20, blank=True, null=True, default='')
    image_1 = models.ImageField(upload_to="product-images", blank=False, null=False)
    image_2 = models.ImageField(upload_to="product-images", blank=True, null=True)
    image_3 = models.ImageField(upload_to="product-images", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        ProductCategory, blank=False, null=False, default="", on_delete=models.CASCADE
    )
    shipping_option = models.ForeignKey(
        ShippingOption, blank=False, null=False, default="", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
