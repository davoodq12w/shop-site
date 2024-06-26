# Generated by Django 5.0.4 on 2024-05-31 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(choices=[('C', 'criticism'), ('P', 'proposal'), ('R', ' report')], max_length=1)),
                ('message', models.TextField()),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]
