# KaSheaCosmetics_cart\views.py
from django.http import JsonResponse
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from KaSheaCosmetics_products.models import Product, ProductSize


def shopping_cart(request):
    cart = request.session.get("cart", {})
    cart_items = []

    total = Decimal(0)

    for product_key, item in cart.items():
        product = get_object_or_404(Product, id=item["product_id"])
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
                "image_url": product.image_1.url,
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


def update_cart_quantity(request):
    if request.method == "POST":
        product_key = request.POST.get("product_key")
        new_quantity = request.POST.get("quantity")

        # Debugging logs
        print(f"Product Key: {product_key}, Quantity: {new_quantity}")

        if not product_key or not new_quantity:
            return JsonResponse(
                {"error": "Missing product key or quantity"}, status=400
            )

        try:
            new_quantity = int(new_quantity)
        except ValueError:
            return JsonResponse({"error": "Invalid quantity"}, status=400)

        # Fetch the cart from the session
        cart = request.session.get("cart", {})

        # Ensure the product exists in the cart
        if product_key in cart:
            # Set the new quantity instead of incrementing
            cart[product_key]["quantity"] = new_quantity

            # Recalculate price based on the new quantity and size adjustment
            size_adjustment = Decimal(cart[product_key]["size_percentage"]) / Decimal(
                100
            )
            adjusted_price = Decimal(cart[product_key]["price"]) * (
                Decimal(1) + size_adjustment
            )
            updated_item_price = round(adjusted_price * new_quantity, 2)

            # Recalculate the cart total
            total = Decimal(0)
            for key, item in cart.items():
                size_adjustment = Decimal(item["size_percentage"]) / Decimal(100)
                adjusted_price = Decimal(item["price"]) * (Decimal(1) + size_adjustment)
                total += adjusted_price * item["quantity"]

            # Update the cart in the session
            request.session["cart"] = cart

            # Send back the updated price and cart total
            return JsonResponse(
                {
                    "updated_price": str(updated_item_price),
                    "cart_total": str(round(total, 2)),
                }
            )
    return JsonResponse({"error": "Invalid request"}, status=400)
