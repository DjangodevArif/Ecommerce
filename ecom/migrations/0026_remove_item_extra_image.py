# Generated by Django 3.1 on 2020-11-11 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0025_auto_20201110_1123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='extra_image',
        ),
    ]
