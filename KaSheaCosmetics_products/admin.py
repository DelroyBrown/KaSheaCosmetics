from django.contrib import admin
from .models import Product, ProductCategory, ShippingOption

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ShippingOption)
