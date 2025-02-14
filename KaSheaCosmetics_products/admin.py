# KaSheaCosmetics_products\admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline
from .models import (
    Product,
    ProductReview,
    Ingredients,
    ProductSize,
    ProductCategory,
    ShippingOption,
)


class ProductSizeInline(StackedInline):
    model = Product.product_sizes.through
    extra = 1


class ProductIngredientInline(StackedInline):
    model = Product.ingredients.through  # Through model for the ManyToMany field
    extra = 1


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ("name", "category", "price", "you_must_try")
    search_fields = ("name",)
    # filter_horizontal = ("ingredients",)  # Keep the ingredients filter as horizontal
    exclude = (
        "product_sizes",
    )  # Exclude the ManyToMany field from the main form since it's handled by the inline
    readonly_fields = [
        "product_sizes",
    ]
    inlines = [
        ProductSizeInline,
        ProductIngredientInline,
    ]  # Add the inline form for sizes


@admin.register(ProductReview)
class ProductReviewAdmin(ModelAdmin):
    list_display = (
        "approved",
        "product",
        "name",
        "email",
        "product_rating",
        "review_title",
        "review_content",
        "image",
        "created_at",
    )
    readonly_fields = [
        "product",
        "name",
        "email",
        "product_rating",
        "review_title",
        "review_content",
        "image",
        "created_at",
    ]


@admin.register(ProductCategory)
class ProductCategoryAdmin(ModelAdmin):
    list_display = ("category_name",)
    search_fields = ("category_name",)


@admin.register(ShippingOption)
class ShippingOptionAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("cost",)


@admin.register(ProductSize)
class ProductSizeAdmin(ModelAdmin):
    list_display = ("size_name",)
    search_fields = ("added_percentage",)


@admin.register(Ingredients)
class IngredientsAdmin(ModelAdmin):
    list_display = ("ingredient_name",)
    search_fields = ("ingredient_name",)


# admin.site.register(Ingredients)
# admin.site.register(ProductCategory)
# admin.site.register(ShippingOption)
# admin.site.register(ProductSize)
