# KaSheaCosmetics_products\forms.py
from django import forms
from .models import ProductReview


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = [
            "name",
            "email",
            "product_rating",
            "review_title",
            "review_content",
            "image",
        ]
        widgets = {
            "product_rating": forms.RadioSelect(
                choices=[(i, str(i)) for i in range(1, 6)]
            ),
        }
