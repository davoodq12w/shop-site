# Generated by Django 5.0.6 on 2024-06-29 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0011_reject_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['-created']},
        ),
        migrations.RemoveIndex(
            model_name='image',
            name='ordering_im_title_071464_idx',
        ),
        migrations.RemoveField(
            model_name='image',
            name='title',
        ),
    ]