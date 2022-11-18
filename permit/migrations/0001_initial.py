# Generated by Django 3.0.8 on 2020-07-27 13:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import permit.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cell', models.CharField(max_length=255)),
                ('sector', models.CharField(max_length=255)),
                ('district', models.CharField(max_length=255)),
                ('province', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Mayor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TransportPermit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('names', models.CharField(max_length=255, verbose_name='names')),
                ('address', models.CharField(max_length=255, verbose_name='address')),
                ('nid', models.CharField(blank=True, max_length=16, verbose_name='nid')),
                ('quantity', models.PositiveIntegerField()),
                ('from_location', models.CharField(max_length=255)),
                ('to_location', models.CharField(max_length=255)),
                ('forest_owner', models.CharField(max_length=255)),
                ('transport_vehicle', models.CharField(max_length=20)),
                ('vehicle_plate', models.CharField(max_length=10)),
                ('vehicle_max_q', models.PositiveIntegerField(blank=True, null=True)),
                ('driver', models.CharField(max_length=255)),
                ('driver_tel', models.CharField(max_length=255)),
                ('start_date', models.DateField(default=permit.utils.start_date_default)),
                ('end_date', models.DateField(default=permit.utils.end_date_default)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('approved_by', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='permit.Mayor')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='permit.Address')),
                ('prepared_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'transport permit',
                'verbose_name_plural': 'transaport permits',
            },
        ),
    ]