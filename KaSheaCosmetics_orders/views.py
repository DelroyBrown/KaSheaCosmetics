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
        print("Invalid payload")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print("Invalid signature")
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print(f"Stripe session: {session}")

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
        amount = session.get("amount_total", 0) / 100
        payment_intent_id = session.get("payment_intent", "")
        session_id = session.get("id")

        try:
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
            print(f"Order created with ID: {order.id}")

            # Retrieve line items using the correct session ID
            line_items = stripe.checkout.Session.list_line_items(session_id)
            print(f"Line items: {line_items}")

            # Retrieve product IDs from metadata
            product_ids = session.get("metadata", {}).get("product_ids", "").split(",")

            # Process each line item to create OrderItem entries
            for idx, item in enumerate(line_items["data"]):
                product_id = product_ids[idx] if idx < len(product_ids) else None
                quantity = item["quantity"]

                print(
                    f"Creating OrderItem for Product ID: {product_id}, Quantity: {quantity}"
                )

                if not product_id:
                    print("Product ID not found in session metadata.")
                    continue

                try:
                    product = Product.objects.get(id=product_id)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                except Product.DoesNotExist:
                    print(f"Product with ID {product_id} does not exist.")

        except Exception as e:
            print(f"Error creating order or order items: {e}")
            return HttpResponse(status=500)

    return HttpResponse(status=200)
