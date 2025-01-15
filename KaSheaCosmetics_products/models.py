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
    # This is the name of the category, which is required and can’t be blank
    category_name = models.CharField(
        max_length=100, blank=False, null=False, default=""
    )

    # URL slug for the category, auto-filled if not provided (more on that later)
    category_url = models.SlugField(default="", max_length=100, blank=True, null=True)

    # Override the save method to automatically generate a slug if none is provided
    def save(self, *args, **kwargs):
        # If there's no category URL, create one by slugifying the category name
        if not self.category_url:
            self.category_url = slugify(self.category_name)
        # Call the parent class’s save method to actually save the model
        super().save(*args, **kwargs)

    # Return the category name when printing or displaying this object
    def __str__(self):
        return self.category_name


class ProductSize(models.Model):
    size_name = models.CharField(blank=False, null=False, max_length=20, default="")
    added_percentage = models.IntegerField(blank=False, null=False, default="")

    def __str__(self):
        return self.size_name


class Ingredients(models.Model):
    ingredient_name = models.CharField(
        max_length=100, blank=True, null=True, default=""
    )

    class Meta:
        verbose_name = "Ingredients"
        verbose_name_plural = "Ingredients"

    def __str__(self):
        return self.ingredient_name


class DefaultShippingCost(models.Model):
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Current default shipping cost: £{self.cost}"


class Product(models.Model):
    you_must_try = models.BooleanField(default=False)
    # Name of the product, this is required and can't be blank
    name = models.CharField(max_length=200, blank=False, null=False, default="")
    # Description of the product, also required and can't be blank
    description = models.TextField(blank=False, null=False, default="", help_text="Tell your customers what makes this product awesome! Share its benefits, key ingredients, and how to use it. Keep it simple and clear so they know why they’ll love it.")
    # Optional size field for the product (e.g., "Small", "Large"), defaults to blank
    size = models.CharField(max_length=20, blank=True, null=True, default="", help_text="IGNORE THIS MY DEAR! It'll prepopulate itself.")
    # Main product image, this one is required
    image_1 = models.ImageField(upload_to="product-images", blank=False, null=False, help_text="This will be your main image.")
    # Optional second product image
    image_2 = models.ImageField(upload_to="product-images", blank=True, null=True)
    # Optional third product image
    image_3 = models.ImageField(upload_to="product-images", blank=True, null=True)
    # Price of the product, max 10 digits, 2 decimal places for pennies
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Enter the price for the SMALLEST size")
    # Category of the product, required, ties to the ProductCategory model
    category = models.ForeignKey(
        ProductCategory, blank=False, null=False, default="", on_delete=models.CASCADE, help_text="Pick a category from the dropdown, or, add one using the + button."
    )
    # Many-to-many relationship for product sizes, can't be blank
    product_sizes = models.ManyToManyField(ProductSize, blank=False)
    # Stock quantity for the product, can't be blank
    stock = models.IntegerField(blank=False, null=False)
    # Shipping option for the product, required, tied to the ShippingOption model
    shipping_option = models.ForeignKey(
        ShippingOption, blank=False, null=False, default=None, on_delete=models.CASCADE
    )
    # Optional field for any extra product details (could be features, specs, etc.)
    product_details = models.TextField(blank=True, null=True, default="")
    # Optional field for "How to use" instructions for the product
    how_to_use = models.TextField(blank=True, null=True, default="")
    # Many-to-many relationship for product ingredients, optional
    ingredients = models.ManyToManyField(Ingredients, blank=True)
    # Optional field to store the Stripe product ID for payment integration
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    # String representation of the model, returns the product's name
    def __str__(self):
        return self.name

    # Method to get the shipping cost for the product
    def get_shipping_cost(self):
        if self.shipping_option:
            return self.shipping_option.cost  # Use the product's shipping option

        # Fallback to a default shipping cost if the product doesn't have one
        default_shipping = DefaultShippingCost.objects.first()
        return default_shipping.cost if default_shipping else Decimal(0)

    def get_review_count(self):
        # This counts only the approved views for each product
        return self.product_reviews.filter(approved=True).count()

    # Override the save method to create a Stripe product if it doesn't already exist
    def save(self, *args, **kwargs):
        if not self.stripe_product_id:  # If no Stripe ID, create one
            stripe_product = create_stripe_product(self)
            if stripe_product:
                self.stripe_product_id = (
                    stripe_product.id
                )  # Store the Stripe product ID

        # Call the parent save method to actually save the product to the database
        super().save(*args, **kwargs)


def create_stripe_product(product):
    try:
        # Create the product in Stripe using the product's name and description
        stripe_product = stripe.Product.create(
            name=product.name,
            description=product.description,
        )

        # Now, create the price for the product in Stripe
        stripe_price = stripe.Price.create(
            product=stripe_product.id,
            unit_amount=int(
                product.price * 100
            ),  # Convert price to cents (Stripe uses cents)
            currency="gbp",  # We're dealing with GBP here
        )

        # Save the Stripe product ID to the product in our local database
        product.stripe_product_id = stripe_product.id
        product.save()

        # Return the Stripe product object, in case we need it later
        return stripe_product
    except Exception as e:
        # Something went wrong, print out the error to debug
        print(f"Error creating product or price in Stripe: {e}")
        return None  # Return None if something failed


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
