# Generated by Django 4.0.4 on 2022-07-02 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cells', '0014_alter_shopingcellmodel_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopingcellmodel',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cells.profileusermodel'),
        ),
    ]