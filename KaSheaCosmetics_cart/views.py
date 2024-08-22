# KaSheaCosmetics_cart\views.py
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from KaSheaCosmetics_products.models import Product, ProductSize


def shopping_cart(request):
    cart = request.session.get("cart", {})
    cart_items = []

    total = Decimal(0)

    for product_key, item in cart.items():
        size_adjustment = Decimal(item["size_percentage"]) / Decimal(100)
        # Convert price to Decimal before performing the calculation
        adjustment_price = Decimal(item["price"]) * (Decimal(1) + size_adjustment)
        total_price = adjustment_price * item["quantity"]
        total += total_price

        cart_items.append(
            {
                "product_name": item["product_name"],
                "size": item["size"],
                "quantity": item["quantity"],
                "price": round(total_price, 2),
            }
        )

    return render(
        request,
        "cart/shopping_cart.html",
        {"cart_items": cart_items, "total": round(total, 2)},
    )


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Ensure quantity is set properly; default to 1 if missing
    quantity = request.POST.get("quantity")
    if not quantity:
        quantity = 1  # Default to 1 if not provided
    else:
        quantity = int(quantity)

    size_id = request.POST.get("size")
    selected_size = get_object_or_404(ProductSize, id=size_id)

    # Get the cart from the session (or create an empty one if it doesn't exist)
    cart = request.session.get("cart", {})

    product_key = f"{product_id}_{size_id}"

    # If the product is already in the cart, update the quantity
    if product_key in cart:
        cart[product_key]["quantity"] += quantity
    else:
        # Otherwise, add the new product to the cart
        cart[product_key] = {
            "product_id": product_id,
            "product_name": product.name,
            "size": selected_size.size_name,
            "size_id": size_id,
            "price": float(product.price),
            "quantity": quantity,
            "size_percentage": selected_size.added_percentage,
        }

    # Save the updated cart back to the session
    request.session["cart"] = cart

    return redirect("KaSheaCosmetics_cart:shopping-cart")
