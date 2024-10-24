# KaSheaCosmetics_products\views.py
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductSize, ProductReview, ProductCategory
from .forms import ProductReviewForm
from KaSheaCosmetics_subscriptions.models import CustomerEmails


def product_list(request):
    # Grab all the products, because that’s what we’re here for
    products = Product.objects.all()

    # Fetch all the product categories while we’re at it
    product_categories = ProductCategory.objects.all()

    # For each category, find all the products that belong in that category
    for category in product_categories:
        # Link up the products to their respective category, like a matchmaking service for items
        category.products = Product.objects.filter(category=category)

    # Finally, we’re throwing all this data into the template and calling it a day
    return render(
        request,
        "products/products_list.html",
        {
            "products": products,  # Passing the whole product gang
            "product_categories": product_categories,  # And their lovely categories
        },
    )


def product_detail(request, product_id):
    # Grab the product by its ID, and 404 if it doesn’t exist (no product, no page)
    product = get_object_or_404(Product, id=product_id)

    # Get all available sizes for the product, because options matter
    sizes = product.product_sizes.all()

    # Fetch the approved reviews for the product, ordered by most recent
    product_reviews = product.product_reviews.filter(approved=True).order_by(
        "-created_at"
    )

    # Count how many reviews we’ve got to show it later
    review_count = product_reviews.count()

    # Set up a star range (1-5) for the rating display, because people love stars
    star_range = range(5)

    # If the user submitted a review via POST, handle the form submission
    if request.method == "POST":
        form = ProductReviewForm(request.POST, request.FILES)
        # Check if the form is valid, 'cause we don’t want junk data
        if form.is_valid():
            product_review = form.save(commit=False)  # Don’t save just yet
            product_review.product = product  # Link the review to this product
            product_review.save()  # Now save it to the database

            # If the review includes an email, store that email for later contact
            if product_review.email:
                CustomerEmails.objects.get_or_create(
                    product=product,
                    email=product_review.email,
                    defaults={"name": product_review.name},
                )

            # Redirect back to the product detail page after saving the review
            return redirect(
                "KaSheaCosmetics_products:product_detail", product_id=product_id
            )
    else:
        # If it’s a GET request, just give them an empty review form
        form = ProductReviewForm()

    # Finally, render the product detail page with all the data we've collected
    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,  # The product info
            "sizes": sizes,  # Available product sizes
            "form": form,  # Review form (empty or with data)
            "product_reviews": product_reviews,  # All approved reviews
            "review_count": review_count,  # Total number of reviews
            "star_range": star_range,  # The star rating range (1-5)
        },
    )


def calculate_discounted_price(product, quantity, size_percentage):
    # Grab the base price of the product, 'cause that’s where it all starts
    base_price = product.price

    # Turn the size percentage into a decimal so we can actually do math with it
    size_adjustment = Decimal(size_percentage) / Decimal(100)

    # Adjust the base price depending on the size, bigger size = bigger price
    adjusted_price = base_price * (Decimal(1) + size_adjustment)

    # If they’re buying 2, throw them a bone with 10% off
    if quantity == 2:
        discount = Decimal(0.10)  # 10% off if you buy 2—I'm generous like that
    # Same deal if they buy 3, because why not?
    elif quantity == 3:
        discount = Decimal(0.10)  # Still 10% off—I'm sticking to it
    # And yeah, let’s keep it going for 4
    elif quantity == 4:
        discount = Decimal(0.10)  # Yep, you guessed it: 10% off
    # Otherwise, no discount for you!
    else:
        discount = Decimal(0)

    # Time to do the math: size-adjusted price, times quantity, minus discount
    discounted_price = adjusted_price * quantity * (Decimal(1) - discount)

    # Finally, round it to 2 decimal places, 'cause nobody likes a price like £19.87492
    return round(discounted_price, 2)


# AJAX view to return the updated price
def update_price(request):
    # Get the product ID from the request because we need to know what we're pricing
    product_id = request.GET.get("product_id")

    # Get the quantity, default to 1 if they’re not saying how many
    quantity = int(request.GET.get("quantity", 1))

    # Get the size percentage, default to 0 if they didn’t specify (standard size, no surprises)
    size_percentage = Decimal(request.GET.get("size_percentage", 0))

    # Fetch the product, and if it doesn't exist, we'll just 404 this thing
    product = get_object_or_404(Product, id=product_id)

    # Now, calculate that sweet discounted price based on the product, quantity, and size
    discounted_price = calculate_discounted_price(product, quantity, size_percentage)

    # Return the final price in JSON form—because we’re fancy like that
    return JsonResponse({"price": discounted_price})
