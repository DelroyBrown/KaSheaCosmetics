# KaSheaCosmetics_orders/views.py
import stripe
import logging
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Order, OrderItem
from KaSheaCosmetics_products.models import Product, ProductSize

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
        logger.error("Invalid payload")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error("Invalid signature")
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Retrieve shipping and customer details
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
            # Create the order
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

            # Retrieve line items from Stripe and metadata
            line_items = stripe.checkout.Session.list_line_items(session_id)
            product_ids = session.get("metadata", {}).get("product_ids", "").split(",")
            size_ids = session.get("metadata", {}).get("size_ids", "").split(",")

            # Process each line item to create OrderItem entries
            for idx, item in enumerate(line_items["data"]):
                product_id = product_ids[idx] if idx < len(product_ids) else None
                size_id = size_ids[idx] if idx < len(size_ids) else None
                quantity = item["quantity"]

                if not product_id:
                    logger.error("Product ID not found in session metadata.")
                    continue

                try:
                    # Fetch product and size
                    product = Product.objects.get(id=product_id)
                    size = ProductSize.objects.get(id=size_id) if size_id else None

                    # Create OrderItem with the size
                    OrderItem.objects.create(
                        order=order, product=product, quantity=quantity, size=size
                    )
                except Product.DoesNotExist:
                    logger.error(f"Product with ID {product_id} does not exist.")
                except ProductSize.DoesNotExist:
                    logger.warning(f"Size with ID {size_id} does not exist.")

            # Gather order item details for context
            order_items = OrderItem.objects.filter(order=order)

            # Compute the admin URL for the created order
            relative_admin_url = reverse(
                "admin:KaSheaCosmetics_orders_order_change", args=[order.id]
            )
            admin_change_url = request.build_absolute_uri(
                relative_admin_url
            )  # Optionally, to get a full URL including domain:
            # admin_change_url = request.build_absolute_uri(admin_change_url)

            # Render HTML email content from template
            html_message = render_to_string(
                "orders/email/new_order_email.html",
                {
                    "order": order,
                    "order_items": order_items,
                    "admin_change_url": admin_change_url,
                },
            )

            # Prepare and send the email
            subject = f"New Order #{order.id} Received"
            recipient_list = ["delroybrown.db@gmail.com"]  # Store owner email

            try:
                send_mail(
                    subject,
                    "",  # Plain text version can be left empty or use a fallback text.
                    settings.EMAIL_HOST_USER,
                    recipient_list,
                    fail_silently=False,
                    html_message=html_message,
                )
                logger.info(f"Order confirmation email sent for order {order.id}")
            except Exception as email_error:
                logger.error(
                    f"Failed to send email for order {order.id}: {email_error}"
                )

        except Exception as e:
            logger.error(f"Error creating order or order items: {e}")
            return HttpResponse(status=500)

    return HttpResponse(status=200)
