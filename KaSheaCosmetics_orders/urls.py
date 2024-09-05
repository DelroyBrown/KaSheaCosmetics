# KaSheaCosmetics_orders\urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import stripe_webhook

app_name = "KaSheaCosmetics_orders"

urlpatterns = [
    path("webhook/stripe/", stripe_webhook, name="stripe-webhook"),
    # path("webhook/", views.stripe_webhook, name="stripe_webhook"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
