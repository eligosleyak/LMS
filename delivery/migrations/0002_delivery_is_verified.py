# Generated by Django 5.0.3 on 2024-03-16 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
