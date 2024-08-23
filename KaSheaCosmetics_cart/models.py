from django.db import models


class ShippingLocation(models.Model):
    city = models.CharField(max_length=100, unique=True)
    shipping_cost = models.DecimalField(max_digits=6, decimal_places=2)

    def __srr__(self):
        return f"{self.city} - £{self.shipping_cost}"
