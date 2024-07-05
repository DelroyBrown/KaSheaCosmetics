# KaSheaCosmetics_base/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

app_name = 'KaSheaCosmetics_base'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('KaShea_home.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
