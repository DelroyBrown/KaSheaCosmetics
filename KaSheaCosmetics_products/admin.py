# KaSheaCosmetics_products\admin.py
from django.contrib import admin
from .models import Product, Ingredients, ProductSize, ProductCategory, ShippingOption


class ProductSizeInline(admin.StackedInline):
    model = Product.product_sizes.through  # Through model for the ManyToMany field
    extra = 1  # This will show 1 empty size form by default


class ProductIngredientInline(admin.StackedInline):
    model = Product.ingredients.through  # Through model for the ManyToMany field
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price")
    search_fields = ("name",)
    # filter_horizontal = ("ingredients",)  # Keep the ingredients filter as horizontal
    exclude = (
        "product_sizes",
    )  # Exclude the ManyToMany field from the main form since it's handled by the inline
    inlines = [ProductSizeInline, ProductIngredientInline]  # Add the inline form for sizes


admin.site.register(Ingredients)
admin.site.register(ProductCategory)
admin.site.register(ShippingOption)
admin.site.register(ProductSize)
