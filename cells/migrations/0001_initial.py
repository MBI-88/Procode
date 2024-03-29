# Generated by Django 4.1 on 2022-08-29 20:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileUserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=8)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='user/%Y/%m/%d')),
                ('address', models.CharField(max_length=200, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='ShopCellModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=150)),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True, db_index=True)),
                ('price', models.FloatField(max_length=6)),
                ('image', models.ImageField(blank=True, null=True, upload_to='smartphone/%Y/%m/%d')),
                ('description', models.TextField(max_length=1000, null=True)),
                ('owner_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopcell', to=settings.AUTH_USER_MODEL)),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cells.profileusermodel')),
            ],
            options={
                'ordering': ['-updated_date'],
            },
        ),
    ]
