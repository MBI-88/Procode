# Generated by Django 4.0.4 on 2022-07-08 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cells', '0003_alter_shopingcellmodel_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileusermodel',
            name='address',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
