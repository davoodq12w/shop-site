# Generated by Django 5.0.4 on 2024-05-27 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='name_of_receiver',
            new_name='receiver_name',
        ),
    ]