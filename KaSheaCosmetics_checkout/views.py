# KaSheaCosmetics_checkout\views.py
import stripe
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from KaSheaCosmetics_cart.views import CART_SESSION_KEY
from KaSheaCosmetics_products.models import Product
from KaSheaCosmetics_products.views import calculate_discounted_price


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request):
    cart = request.session.get(CART_SESSION_KEY, {})
    line_items = []
    product_ids = []
    size_ids = []  # To store size IDs

    # Retrieve the dynamic shipping cost from session
    shipping_cost = request.session.get("shipping_cost", 0)

    # Iterate through each item in the cart
    for product_key, item in cart.items():
        product = Product.objects.get(id=item["product_id"])

        # Calculate the discounted price
        discounted_total_price = calculate_discounted_price(
            product, item["quantity"], item["size_percentage"]
        )
        price_per_item = discounted_total_price / item["quantity"]
        unit_amount = int(price_per_item * 100)

        # Add product and size IDs for metadata
        product_ids.append(str(product.id))
        size_ids.append(str(item.get("size_id", "")))  # Capture size_id if available

        # Create line item for Stripe Checkout
        line_items.append(
            {
                "price_data": {
                    "currency": "gbp",
                    "product_data": {
                        "name": product.name,
                        "description": f"Product ID: {product.id}",
                    },
                    "unit_amount": unit_amount,
                },
                "quantity": item["quantity"],
            }
        )

    # Add shipping as a separate line item
    if shipping_cost > 0:
        line_items.append(
            {
                "price_data": {
                    "currency": "gbp",
                    "product_data": {"name": "Shipping"},
                    "unit_amount": int(shipping_cost * 100),
                },
                "quantity": 1,
            }
        )

    # Store product and size IDs as comma-separated metadata
    session_metadata = {
        "product_ids": ",".join(product_ids),
        "size_ids": ",".join(size_ids),
    }

    # Create the Stripe Checkout session
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse("KaSheaCosmetics_checkout:checkout_success")
        ),
        cancel_url=request.build_absolute_uri(
            reverse("KaSheaCosmetics_cart:shopping-cart")
        ),
        billing_address_collection="required",
        shipping_address_collection={"allowed_countries": ["GB"]},
        metadata=session_metadata,  # Attach metadata
    )

    return JsonResponse({"id": session.id})


def checkout_success(request):
    if CART_SESSION_KEY in request.session:
        del request.session[CART_SESSION_KEY]
        request.session.modified = True

    return render(request, "checkout/checkout_success.html")
