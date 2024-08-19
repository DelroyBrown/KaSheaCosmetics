# KaSheaCosmetics_home\urls.py
from django.urls import path
from . import views

app_name = "KaSheaCosmetics_home"

urlpatterns = [
    path("", views.home, name="home"),
]
