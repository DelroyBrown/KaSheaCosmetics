# KaSheaCosmetics_products\models.py
import stripe
from decimal import Decimal
from django.db import models
from django.utils.text import slugify


class ShippingOption(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    category_name = models.CharField(
        max_length=100, blank=False, null=False, default=""
    )
    category_url = models.SlugField(default="", max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.category_url:
            self.category_url = slugify(self.category_name)
        super().save(*args, **kwargs)

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
    stripe_product_id = models.CharField(
        max_length=255, blank=True, null=True
    )  # New field for Stripe product ID

    def get_shipping_cost(self):
        if self.shipping_option:
            return self.shipping_option.cost

        default_shipping = DefaultShippingCost.objects.first()
        return default_shipping.cost if default_shipping else Decimal(0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # If the product is new and does not have a Stripe product ID, create one in Stripe
        if not self.stripe_product_id:
            stripe_product = create_stripe_product(self)
            if stripe_product:
                self.stripe_product_id = stripe_product.id

        super().save(*args, **kwargs)


def create_stripe_product(product):
    try:
        # Create the product in Stripe
        stripe_product = stripe.Product.create(
            name=product.name,
            description=product.description,
        )

        # Create the price for the product in Stripe
        stripe_price = stripe.Price.create(
            product=stripe_product.id,
            unit_amount=int(product.price * 100),  # Convert to cents
            currency="gbp",
        )

        # Store the Stripe product ID in the product model
        product.stripe_product_id = stripe_product.id
        product.save()

        return stripe_product
    except Exception as e:
        print(f"Error creating product or price in Stripe: {e}")
        return None


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_reviews"
    )
    name = models.CharField(blank=False, null=False, max_length=30, default="")
    email = models.EmailField(max_length=100, blank=True, null=True, default="")
    product_rating = models.PositiveIntegerField()
    review_title = models.CharField(max_length=100, blank=False, null=False, default="")
    review_content = models.TextField(
        max_length=2000, blank=False, null=False, default=""
    )
    image = models.ImageField(upload_to="review-images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Product review by {self.name} on {self.product.name}"
