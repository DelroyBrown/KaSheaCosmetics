# KaSheaCosmetics_products\urls.py
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path

app_name = "KaSheaCosmetics_products"

urlpatterns = [
    path("products/", views.product_list, name="product_list"),
    path("products/<int:product_id>/", views.product_detail, name="product_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
