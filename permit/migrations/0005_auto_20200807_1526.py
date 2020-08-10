# Generated by Django 3.0.2 on 2020-08-07 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('permit', '0004_auto_20200807_1117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AlterField(
            model_name='originlocation',
            name='l_cell',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='permit.Cell', verbose_name='Akagali'),
        ),
        migrations.AlterField(
            model_name='originlocation',
            name='l_district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='permit.District', verbose_name='Akarere'),
        ),
        migrations.AlterField(
            model_name='originlocation',
            name='l_province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='permit.Province', verbose_name='Intara'),
        ),
        migrations.AlterField(
            model_name='originlocation',
            name='l_sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='permit.Sector', verbose_name='Umurenge'),
        ),
        migrations.AlterField(
            model_name='originlocation',
            name='l_village',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='permit.Village', verbose_name='Umudugudu'),
        ),
        migrations.AlterField(
            model_name='requestor',
            name='nid',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='Indangamuntu'),
        ),
        migrations.AlterField(
            model_name='requestor',
            name='r_cell',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='permit.Cell', verbose_name='Akagali'),
        ),
        migrations.AlterField(
            model_name='requestor',
            name='r_district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET, to='permit.District', verbose_name='Akarere'),
        ),
        migrations.AlterField(
            model_name='requestor',
            name='r_province',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET, to='permit.Province', verbose_name='Intara'),
        ),
        migrations.AlterField(
            model_name='requestor',
            name='r_sector',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET, to='permit.Sector', verbose_name='Umurenge'),
        ),
        migrations.AlterField(
            model_name='requestor',
            name='r_village',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='permit.Village', verbose_name='Umudugudu'),
        ),
    ]
