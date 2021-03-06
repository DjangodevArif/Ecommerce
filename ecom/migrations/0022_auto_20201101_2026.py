# Generated by Django 3.1 on 2020-11-01 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0021_auto_20201101_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='order',
            field=models.ManyToManyField(blank=True, null=True, to='ecom.CartItem'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='shipping_add',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecom.shippingaddress'),
        ),
        migrations.AlterField(
            model_name='item',
            name='cata',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecom.catagory'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='defult_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecom.shippingaddress'),
        ),
    ]
