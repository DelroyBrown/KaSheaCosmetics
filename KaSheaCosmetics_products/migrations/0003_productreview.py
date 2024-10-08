# Generated by Django 5.1 on 2024-08-29 12:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KaSheaCosmetics_products', '0002_defaultshippingcost_alter_product_shipping_option'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
                ('email', models.EmailField(blank=True, default='', max_length=100, null=True)),
                ('product_rating', models.PositiveIntegerField()),
                ('review_title', models.CharField(default='', max_length=100)),
                ('review_content', models.TextField(default='', max_length=2000)),
                ('image', models.ImageField(blank=True, null=True, upload_to='review-images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_reviews', to='KaSheaCosmetics_products.product')),
            ],
        ),
    ]
