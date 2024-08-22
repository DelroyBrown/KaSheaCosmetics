# KaSheaCosmetics_cart\urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = "KaSheaCosmetics_cart"

urlpatterns = [
    path("shopping-cart/", views.shopping_cart, name="shopping-cart"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add-to-cart"),
    path(
        "update-cart-quantity/", views.update_cart_quantity, name="update-cart-quantity"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
