# Generated by Django 5.1 on 2024-10-02 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KaSheaCosmetics_products', '0003_productreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='category_url',
            field=models.SlugField(default='', max_length=100),
        ),
    ]
