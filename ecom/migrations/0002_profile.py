# Generated by Django 3.1 on 2020-10-22 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecom', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='')),
                ('phone_num', models.IntegerField(max_length=11)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('district', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('address', models.TextField(max_length=50)),
                ('extra_info', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
