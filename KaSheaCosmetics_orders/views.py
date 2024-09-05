# KaSheaCosmetics_orders\views.py
import stripe
import logging
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem
from KaSheaCosmetics_products.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f"Invalid payload: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {e}")
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Get session details
        customer_name = session.get("shipping", {}).get("name", "")
        email = session.get("customer_details", {}).get("email", "")
        shipping_address = (
            session.get("shipping", {}).get("address", {}).get("line1", "")
        )
        shipping_city = session.get("shipping", {}).get("address", {}).get("city", "")
        shipping_postcode = (
            session.get("shipping", {}).get("address", {}).get("postal_code", "")
        )
        shipping_country = (
            session.get("shipping", {}).get("address", {}).get("country", "")
        )
        amount = session.get("amount_total", 0) / 100  # Stripe sends amounts in cents
        payment_intent_id = session.get("payment_intent", "")

        logger.info(f"Processing order for {customer_name} - {email}")

        try:
            # Create the order in your database
            order = Order.objects.create(
                customer_name=customer_name,
                email=email,
                shipping_address=shipping_address,
                shipping_city=shipping_city,
                shipping_postcode=shipping_postcode,
                shipping_country=shipping_country,
                stripe_payment_intent_id=payment_intent_id,
                amount=amount,
                status="Paid",
            )
            logger.info(f"Order created successfully with ID: {order.id}")
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return HttpResponse(status=500)

        # Get line items and create OrderItems
        try:
            line_items = stripe.checkout.Session.list_line_items(session["id"])
            for item in line_items["data"]:
                product_id = item["price"]["product_data"]["metadata"]["product_id"]
                product = Product.objects.get(id=product_id)
                quantity = item["quantity"]

                # Save each product in the order
                OrderItem.objects.create(
                    order=order, product=product, quantity=quantity
                )
                logger.info(f"OrderItem created: {product.name} x {quantity}")
        except Exception as e:
            logger.error(f"Error creating order items: {e}")
            return HttpResponse(status=500)

    return HttpResponse(status=200)