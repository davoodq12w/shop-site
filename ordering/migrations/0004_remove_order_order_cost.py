# Generated by Django 5.0.6 on 2024-06-08 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0003_order_order_cost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_cost',
        ),
    ]
