# Generated by Django 5.0.6 on 2024-05-09 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='product_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
