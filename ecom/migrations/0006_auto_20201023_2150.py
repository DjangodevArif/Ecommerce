# Generated by Django 3.1 on 2020-10-23 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0005_auto_20201023_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
