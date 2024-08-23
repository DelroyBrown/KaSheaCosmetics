# KaSheaCosmetics_cart\views.py
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from KaSheaCosmetics_cart.models import ShippingLocation
from KaSheaCosmetics_products.models import Product, ProductSize, DefaultShippingCost
from KaSheaCosmetics_products.views import calculate_discounted_price


CART_SESSION_KEY = "cart"


# Helper function to validate quantity
def validate_quantity(quantity):
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        return quantity
    except (ValueError, TypeError):
        return None


def shopping_cart(request):
    cart = request.session.get(CART_SESSION_KEY, {})
    cart_items = []
    total = Decimal(0)
    shipping_cost = Decimal(0)
    subtotal = Decimal(0)
    shipping_city = request.GET.get("shipping_city", "")

    # Initialize default shipping cost at the start
    default_shipping = None

    # Optimize query by fetching all products at once
    product_ids = [item["product_id"] for item in cart.values()]
    products = Product.objects.filter(id__in=product_ids)
    products_dict = {product.id: product for product in products}

    for product_key, item in cart.items():
        product = products_dict.get(item["product_id"])

        if product:
            # Apply the discount calculation here for each cart item
            discounted_price = calculate_discounted_price(
                product, item["quantity"], item["size_percentage"]
            )

            subtotal += discounted_price  # Add product prices to subtotal
            total += discounted_price  # Add to total as well

            # Get the shipping cost for each product
            product_shipping_cost = (
                product.get_shipping_cost()
            )  # Use the get_shipping_cost method

            cart_items.append(
                {
                    "product_name": item["product_name"],
                    "size": item["size"],
                    "quantity": item["quantity"],
                    "price": discounted_price,
                    "image_url": product.image_1.url,
                    "product_id": item["product_id"],
                    "product_key": product_key,
                    "shipping_cost": product_shipping_cost,
                }
            )

    # Check if a shipping city is provided and get the corresponding cost
    if shipping_city:
        try:
            shipping_location = ShippingLocation.objects.get(city__iexact=shipping_city)
            shipping_cost = shipping_location.shipping_cost
        except ShippingLocation.DoesNotExist:
            messages.error(
                request, f"No shipping option available for {shipping_city}."
            )
    else:
        # If no city is provided, fetch the default shipping cost
        default_shipping = DefaultShippingCost.objects.first()
        if default_shipping:
            shipping_cost = default_shipping.cost

    # Add shipping cost to the total
    total += shipping_cost

    # Pass the subtotal, total, and shipping cost to the template
    return render(
        request,
        "cart/shopping_cart.html",
        {
            "cart_items": cart_items,
            "total": round(total, 2),
            "subtotal": round(subtotal, 2),
            "shipping_cost": round(shipping_cost, 2),
            "shipping_city": shipping_city,
            "default_shipping": (
                default_shipping.cost if default_shipping else None
            ),  # Pass default shipping cost, if available
        },
    )


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    quantity = validate_quantity(request.POST.get("quantity", 1))
    if quantity is None:
        messages.error(request, "Invalid quantity")
        return redirect(
            "KaSheaCosmetics_products:product_detail", product_id=product_id
        )

    size_id = request.POST.get("size")
    selected_size = get_object_or_404(ProductSize, id=size_id)

    cart = request.session.get(CART_SESSION_KEY, {})
    product_key = f"{product_id}_{size_id}"

    # Convert Decimal to float before saving it to session
    price = float(product.price)

    if product_key in cart:
        cart[product_key]["quantity"] = quantity
    else:
        cart[product_key] = {
            "product_id": product_id,
            "product_name": product.name,
            "size": selected_size.size_name,
            "size_id": size_id,
            "price": price,  # Store as float
            "quantity": quantity,
            "size_percentage": selected_size.added_percentage,
        }

    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True  # Ensure the session is saved

    return redirect("KaSheaCosmetics_cart:shopping-cart")


def update_cart_quantity(request):
    if request.method == "POST":
        product_key = request.POST.get("product_key")
        new_quantity = request.POST.get("quantity")

        if not product_key or new_quantity is None:
            messages.error(request, "Invalid product or quantity")
            return redirect("KaSheaCosmetics_cart:shopping-cart")

        new_quantity = validate_quantity(new_quantity)
        if new_quantity is None:
            messages.error(request, "Invalid quantity")
            return redirect("KaSheaCosmetics_cart:shopping-cart")

        cart = request.session.get(CART_SESSION_KEY, {})

        if product_key not in cart:
            messages.error(request, "Product not found in cart")
            return redirect("KaSheaCosmetics_cart:shopping-cart")

        # Update the quantity
        cart[product_key]["quantity"] = new_quantity
        request.session.modified = True  # Force the session to save

    return redirect("KaSheaCosmetics_cart:shopping-cart")


def delete_from_cart(request):
    if request.method == "POST":
        product_key = request.POST.get("product_key")

        if not product_key:
            messages.error(request, "Invalid product key")
            return redirect("KaSheaCosmetics_cart:shopping-cart")

        cart = request.session.get(CART_SESSION_KEY, {})

        if product_key in cart:
            del cart[product_key]
            request.session.modified = True
            messages.success(request, "Item Removed From Cart.")
        else:
            messages.error(request, "Product not found in cart.")

    return redirect("KaSheaCosmetics_cart:shopping-cart")
