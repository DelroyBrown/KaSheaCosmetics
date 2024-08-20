# KaSheaCosmetics_cart\views.py
from django.shortcuts import render


def shopping_cart(request):
    return render(request, "cart/shopping_cart.html")
