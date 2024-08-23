# KaSheaCosmetics_products\models.py
from decimal import Decimal
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


class ProductSize(models.Model):
    size_name = models.CharField(blank=False, null=False, max_length=20, default="")
    added_percentage = models.IntegerField(blank=False, null=False, default="")

    def __srt__(self):
        return self.size_name


class Ingredients(models.Model):
    ingredient_name = models.CharField(
        max_length=100, blank=True, null=True, default=""
    )

    def __str__(self):
        return self.ingredient_name


class DefaultShippingCost(models.Model):
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Current default shipping cost: £{self.cost}"


class Product(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, default="")
    description = models.TextField(blank=False, null=False, default="")
    size = models.CharField(max_length=20, blank=True, null=True, default="")
    image_1 = models.ImageField(upload_to="product-images", blank=False, null=False)
    image_2 = models.ImageField(upload_to="product-images", blank=True, null=True)
    image_3 = models.ImageField(upload_to="product-images", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        ProductCategory, blank=False, null=False, default="", on_delete=models.CASCADE
    )
    product_sizes = models.ManyToManyField(ProductSize, blank=False)
    stock = models.IntegerField(blank=False, null=False)
    shipping_option = models.ForeignKey(
        ShippingOption, blank=False, null=False, default=None, on_delete=models.CASCADE
    )
    product_details = models.TextField(blank=True, null=True, default="")
    how_to_use = models.TextField(blank=True, null=True, default="")
    ingredients = models.ManyToManyField(Ingredients, blank=True)

    def get_shipping_cost(self):
        if self.shipping_option:
            return self.shipping_option.cost

        default_shipping = DefaultShippingCost.objects.first()
        return default_shipping.cost if default_shipping else Decimal(0)

    def __str__(self):
        return self.name
