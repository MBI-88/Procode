# Generated by Django 4.0.4 on 2022-06-08 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cells', '0006_alter_shopingcell_model_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileuser',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
