# Generated by Django 5.1 on 2025-01-27 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100, unique=True)),
                ('shipping_cost', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
    ]
