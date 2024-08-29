# KaSheaCosmetics_subscriptions\urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

app_name = "KaSheaCosmetics_subscriptions"

urlpatterns = []

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
