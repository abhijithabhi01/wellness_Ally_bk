# Generated by Django 5.0.1 on 2024-03-08 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_order_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='health-profile'),
        ),
    ]
