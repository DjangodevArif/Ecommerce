# Generated by Django 3.1 on 2020-11-10 05:11

from django.db import migrations, models
import django.db.models.deletion
import ecom.models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0023_auto_20201101_2028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='image',
        ),
        migrations.CreateModel(
            name='ImageItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to=ecom.models.user_img_path)),
                ('item_link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecom.item')),
            ],
        ),
    ]