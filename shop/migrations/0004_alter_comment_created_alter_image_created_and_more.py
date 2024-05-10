# Generated by Django 5.0.4 on 2024-05-28 13:23

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_comment_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='created',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='created',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='update',
            field=django_jalali.db.models.jDateTimeField(auto_now=True),
        ),
    ]
