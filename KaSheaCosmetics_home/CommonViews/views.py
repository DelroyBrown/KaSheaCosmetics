# KaSheaCosmetics_home\CommonViews\views.py
from django.shortcuts import render
from KaSheaCosmetics_home.CommonModels.models import TopBannerMessage


def top_banner_message(request):
    top_banner_message = TopBannerMessage.objects.all()
    return {"top_banner_message": top_banner_message}
