# Generated by Django 4.0.4 on 2022-07-08 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cells', '0005_alter_shopingcellmodel_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopingcellmodel',
            name='description',
            field=models.TextField(max_length=300, null=True),
        ),
    ]
