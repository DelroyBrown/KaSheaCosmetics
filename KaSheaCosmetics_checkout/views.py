# KaSheaCosmetics_checkout\views.py
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from KaSheaCosmetics_cart.views import CART_SESSION_KEY
from KaSheaCosmetics_products.models import Product


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request):
    cart = request.session.get(CART_SESSION_KEY, {})
    line_items = []

    for product_key, item in cart.items():
        product = Product.objects.get(id=item["product_id"])
        line_items.append(
            {
                "price_data": {
                    "currency": "gbp",
                    "prodict_data": {
                        "name": product_name,
                    },
                    "unit_amount": int(product.price * 100),
                },
                "quantity": item["quantity"],
            }
        )
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
    )
    return JsonResponse({"id": session.id})


def checkout_success(request):
    return render(request, "checkout/checkout_success.html")


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhok.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

    return HttpResponse(status=200)
