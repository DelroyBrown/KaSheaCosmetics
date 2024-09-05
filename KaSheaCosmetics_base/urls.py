# KaSheaCosmetics_base\urls.py
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

app_name = "KaSheaCosmetics_base"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("KaSheaCosmetics_home.urls")),
    path("", include("KaSheaCosmetics_products.urls")),
    path("", include("KaSheaCosmetics_cart.urls")),
    path("", include("KaSheaCosmetics_subscriptions.urls")),
    path("", include("KaSheaCosmetics_checkout.urls")),
    path("orders/", include("KaSheaCosmetics_orders.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
