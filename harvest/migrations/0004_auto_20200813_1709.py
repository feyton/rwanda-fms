# Generated by Django 3.0.6 on 2020-08-13 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('harvest', '0003_auto_20200813_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='harvestingpermit',
            name='date_approved',
            field=models.DateField(blank=True, null=True),
        ),
    ]