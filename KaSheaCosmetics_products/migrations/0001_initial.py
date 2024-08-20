# Generated by Django 5.1 on 2024-08-20 14:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient_name', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size_name', models.CharField(default='', max_length=20)),
                ('added_percentage', models.IntegerField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
                ('description', models.TextField(default='')),
                ('size', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('image_1', models.ImageField(upload_to='product-images')),
                ('image_2', models.ImageField(blank=True, null=True, upload_to='product-images')),
                ('image_3', models.ImageField(blank=True, null=True, upload_to='product-images')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.IntegerField()),
                ('product_details', models.TextField(blank=True, default='', null=True)),
                ('how_to_use', models.TextField(blank=True, default='', null=True)),
                ('ingredients', models.ManyToManyField(blank=True, to='KaSheaCosmetics_products.ingredients')),
                ('category', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='KaSheaCosmetics_products.productcategory')),
                ('product_sizes', models.ManyToManyField(to='KaSheaCosmetics_products.productsize')),
                ('shipping_option', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='KaSheaCosmetics_products.shippingoption')),
            ],
        ),
    ]
