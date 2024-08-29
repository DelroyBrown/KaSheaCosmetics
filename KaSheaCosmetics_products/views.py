# KaSheaCosmetics_products\views.py
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductSize, ProductReview
from .forms import ProductReviewForm
from KaSheaCosmetics_subscriptions.models import CustomerEmails


def product_list(request):
    products = Product.objects.all()
    return render(request, "products/products_list.html", {"products": products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    sizes = product.product_sizes.all()
    product_reviews = product.product_reviews.filter(approved=True).order_by(
        "-created_at"
    )
    review_count = product_reviews.count()
    star_range = range(5)

    if request.method == "POST":
        form = ProductReviewForm(request.POST, request.FILES)
        if form.is_valid():
            product_review = form.save(commit=False)
            product_review.product = product
            product_review.save()

            if product_review.email:  
                CustomerEmails.objects.get_or_create(
                    product=product,
                    email=product_review.email,
                    defaults={"name": product_review.name},
                )

            return redirect(
                "KaSheaCosmetics_products:product_detail", product_id=product_id
            )
    else:
        form = ProductReviewForm()

    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,
            "sizes": sizes,
            "form": form,
            "product_reviews": product_reviews,
            "review_count": review_count,
            "star_range": star_range,
        },
    )


def calculate_discounted_price(product, quantity, size_percentage):
    base_price = product.price

    # Apply size adjustment (percentage increase or decrease)
    size_adjustment = Decimal(size_percentage) / Decimal(100)

    # Adjust base price by the size percentage
    adjusted_price = base_price * (Decimal(1) + size_adjustment)

    # Apply quantity-based discount (if any)
    if quantity == 2:
        discount = Decimal(0.10)  # 10% off for 2 items
    elif quantity == 3:
        discount = Decimal(0.10)  # Same discount for 3 items (adjust as needed)
    elif quantity == 4:
        discount = Decimal(0.10)  # Same discount for 4 items (adjust as needed)
    else:
        discount = Decimal(0)

    # Calculate the final price
    discounted_price = adjusted_price * quantity * (Decimal(1) - discount)

    return round(discounted_price, 2)


# AJAX view to return the updated price
def update_price(request):
    product_id = request.GET.get("product_id")
    quantity = int(request.GET.get("quantity", 1))
    size_percentage = Decimal(request.GET.get("size_percentage", 0))

    product = get_object_or_404(Product, id=product_id)
    discounted_price = calculate_discounted_price(product, quantity, size_percentage)

    return JsonResponse({"price": discounted_price})
