# Generated by Django 3.1 on 2020-10-28 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0014_refundrequest'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coupon',
            options={'verbose_name': 'Discount code'},
        ),
        migrations.AddField(
            model_name='profile',
            name='stripe_customer',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
