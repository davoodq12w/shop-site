# Generated by Django 5.0.4 on 2024-05-30 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_comment_created_alter_image_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rate',
            field=models.IntegerField(),
        ),
    ]