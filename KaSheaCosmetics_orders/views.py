# KaSheaCosmetics_orders/views.py
import stripe
import logging
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
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
        customer_email = session.get("customer_details", {}).get("email", "")
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
                email=customer_email,
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
                    product = Product.objects.get(id=product_id)
                    size = ProductSize.objects.get(id=size_id) if size_id else None

                    OrderItem.objects.create(
                        order=order, product=product, quantity=quantity, size=size
                    )
                except Product.DoesNotExist:
                    logger.error(f"Product with ID {product_id} does not exist.")
                except ProductSize.DoesNotExist:
                    logger.warning(f"Size with ID {size_id} does not exist.")

            # Gather order items for context
            order_items = OrderItem.objects.filter(order=order)

            # Compute the fully qualified admin URL for the created order
            relative_admin_url = reverse(
                "admin:KaSheaCosmetics_orders_order_change", args=[order.id]
            )
            admin_change_url = request.build_absolute_uri(relative_admin_url)

            # Render HTML email content for store owner
            owner_html_message = render_to_string(
                "orders/email/new_order_email.html",
                {
                    "order": order,
                    "order_items": order_items,
                    "admin_change_url": admin_change_url,
                },
            )

            # Send email to store owner
            subject_owner = f"New Order #{order.id} Received"
            recipient_list_owner = ["delroybrown.db@gmail.com"]
            try:
                send_mail(
                    subject_owner,
                    "",  # Fallback text
                    settings.EMAIL_HOST_USER,
                    recipient_list_owner,
                    fail_silently=False,
                    html_message=owner_html_message,
                )
                logger.info(
                    f"Order confirmation email sent for order {order.id} to owner"
                )
            except Exception as email_error:
                logger.error(
                    f"Failed to send email for order {order.id} to owner: {email_error}"
                )

            # Render HTML email content for customer receipt
            customer_html_message = render_to_string(
                "orders/email/customer_receipt_email.html",
                {
                    "order": order,
                    "order_items": order_items,
                },
            )

            # Send email to customer
            subject_customer = f"Your Ka'Shea Cosmetics Receipt"
            recipient_list_customer = [order.email]
            try:
                send_mail(
                    subject_customer,
                    "",  # Fallback text
                    settings.EMAIL_HOST_USER,
                    recipient_list_customer,
                    fail_silently=False,
                    html_message=customer_html_message,
                )
                logger.info(f"Receipt email sent to customer for order {order.id}")
            except Exception as cust_email_error:
                logger.error(
                    f"Failed to send receipt email to customer for order {order.id}: {cust_email_error}"
                )

        except Exception as e:
            logger.error(f"Error creating order or order items: {e}")
            return HttpResponse(status=500)

    return HttpResponse(status=200)
