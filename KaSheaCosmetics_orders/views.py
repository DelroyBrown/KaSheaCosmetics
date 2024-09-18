# KaSheaCosmetics_orders\views.py
import stripe
import logging
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem
from KaSheaCosmetics_products.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.exception("Invalid payload")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.exception("Invalid signature")
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        logger.debug(f"Stripe session: {session}")

        # Get session details
        customer_name = session.get("shipping_details", {}).get("name", "")
        email = session.get("customer_details", {}).get("email", "")
        shipping_address = (
            session.get("shipping_details", {}).get("address", {}).get("line1", "")
        )
        shipping_city = (
            session.get("shipping_details", {}).get("address", {}).get("city", "")
        )
        shipping_postcode = (
            session.get("shipping_details", {})
            .get("address", {})
            .get("postal_code", "")
        )
        shipping_country = (
            session.get("shipping_details", {}).get("address", {}).get("country", "")
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
        except Exception as e:
            logger.exception("Error creating order: %s", e)
            return HttpResponse(status=500)

        # Get line items and create OrderItems
        try:
            line_items = stripe.checkout.Session.list_line_items(session["id"])
            logger.debug(f"Line items: {line_items}")

            for item in line_items["data"]:
                description = item.get("description", "")
                logger.debug(f"Line item description: {description}")

                # Extract product_id from description
                product_id = None
                if description and "Product ID:" in description:
                    product_id = description.split("Product ID:")[1].strip()

                if not product_id:
                    logger.error("Product ID not found in line item description.")
                    continue

                product = Product.objects.get(id=product_id)
                quantity = item["quantity"]

                # Save each product in the order
                OrderItem.objects.create(
                    order=order, product=product, quantity=quantity
                )
        except Exception as e:
            logger.exception("Error creating order items: %s", e)
            return HttpResponse(status=500)

    return HttpResponse(status=200)
