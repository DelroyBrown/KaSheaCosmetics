# KaSheaCosmetics_products\views.py
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Product, ProductSize


def product_list(request):
    products = Product.objects.all()
    return render(request, "products/products_list.html", {"products": products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    sizes = product.product_sizes.all()
    return render(
        request, "products/product_detail.html", {"product": product, "sizes": sizes}
    )


# Function to calculate price with discounts and size adjustment
def calculate_discounted_price(product, quantity, size_percentage):
    base_price = product.price

    # Apply size adjustment (percentage increase or decrease)
    size_adjustment = Decimal(size_percentage) / Decimal(
        100
    )  # size_percentage is already passed as a number

    # Adjust base price by the size percentage
    adjusted_price = base_price * (Decimal(1) + size_adjustment)

    # Apply quantity-based discount (only to adjusted price)
    if quantity == 2:
        discount = Decimal(0.15)  # 15% off for 2 items
    elif quantity == 3:
        discount = Decimal(0.15)  
    elif quantity == 4:
        discount = Decimal(0.15)  
    else:
        discount = Decimal(0)  # No discount for 1 item

    # Calculate final discounted price for the given quantity
    discounted_price = adjusted_price * quantity * (Decimal(1) - discount)

    return round(discounted_price, 2)


# AJAX view to return the updated price
def update_price(request):
    product_id = request.GET.get("product_id")
    quantity = int(request.GET.get("quantity", 1))
    size_percentage = Decimal(
        request.GET.get("size_percentage", 0)
    )  # Get size percentage

    product = get_object_or_404(Product, id=product_id)
    discounted_price = calculate_discounted_price(product, quantity, size_percentage)

    return JsonResponse({"price": discounted_price})
