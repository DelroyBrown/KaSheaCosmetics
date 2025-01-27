from django.db import models


class TopBannerMessage(models.Model):
    banner_name = models.CharField(max_length=50, blank=False, null=False, default="")
    banner_description = models.TextField(max_length=500, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.banner_name


class specialOffer(models.Model):
    offer_name = models.CharField(max_length=50, blank=False, null=False, default="")
    offer_description = models.TextField(
        max_length=1000, blank=False, null=False, default=""
    )
    image = models.ImageField(
        upload_to="special-offer-images",
        blank=False,
        null=False,
        help_text="This will be your main image.",
    )

    def __str__(self):
        return self.offer_name
