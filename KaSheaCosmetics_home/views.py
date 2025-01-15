# KaSheaCosmetics_home\views.py
from django.shortcuts import render
from KaSheaCosmetics_products.models import Product


def home(request):
    you_must_try_products = Product.objects.filter(you_must_try=True)
    context = {"you_must_try_products": you_must_try_products}
    return render(request, "home/home.html", context)
