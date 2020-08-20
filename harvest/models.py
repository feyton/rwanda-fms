from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .utils import permit_code

User = get_user_model()


class HPRequestor(models.Model):
    cats = ((1, 'Leta'), (2, 'Akarere'), (3, 'Umurenge'), (4, 'Umuturage'))
    category = models.IntegerField(
        _('Usaba'), choices=cats, default=4)
    names = models.CharField(
        _('Amazina'), max_length=255, blank=False, null=False)
    nid = models.CharField(
        _('Indangamuntu'), max_length=21, blank=True, null=True)
    telephone = models.CharField(
        _('telephone'), max_length=15, blank=True, null=True)
    r_province = models.ForeignKey(
        'permit.Province', on_delete=models.SET, null=True, verbose_name='Intara')
    r_district = models.ForeignKey(
        'permit.District', on_delete=models.SET, null=True, verbose_name='Akarere')
    r_sector = models.ForeignKey(
        'permit.Sector', on_delete=models.SET, null=True, verbose_name='Umurenge')
    r_cell = models.ForeignKey(
        'permit.Cell', on_delete=models.SET_NULL, null=True, verbose_name='Akagali')

    def __str__(self):
        return self.names


class TimberSpecies(models.Model):
    species = models.CharField(max_length=255, blank=False, null=False)
    width = models.FloatField(blank=True, null=True, default=13,
                              help_text='Andika ubugari muri centimeter', verbose_name='Umurambararo')
    height = models.FloatField(blank=True, null=True, default=15,
                               help_text='Andika uburebure muri metero', verbose_name='Uburebure')
    price = models.PositiveIntegerField(blank=True, null=True)


class ConstructionSpecies(models.Model):
    # ibiti bishingwa
    species = models.CharField(max_length=255, blank=True, null=False)
    width = models.FloatField(blank=True, null=True, default=13,
                              help_text='Andika ubugari muri centimeter', verbose_name='Umurambararo')
    height = models.FloatField(blank=True, null=True, default=15,
                               help_text='Andika uburebure muri metero', verbose_name='Uburebure')
    number = models.PositiveIntegerField(blank=True)


class Forest(models.Model):
    construction_species = models.ManyToManyField(
        ConstructionSpecies, blank=True, related_name='forests')
    timber_species = models.ManyToManyField(TimberSpecies, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    owner = models.CharField(max_length=255)
    area = models.FloatField()
    upi = models.CharField(max_length=10, blank=True, null=True)
    distance = models.FloatField(blank=True)
    # Address
    f_province = models.ForeignKey(
        'permit.Province', on_delete=models.SET, null=True, verbose_name='Intara')
    f_district = models.ForeignKey(
        'permit.District', on_delete=models.SET, null=True, verbose_name='Akarere')
    f_sector = models.ForeignKey(
        'permit.Sector', on_delete=models.SET, null=True, verbose_name='Umurenge')
    f_cell = models.ForeignKey(
        'permit.Cell', on_delete=models.SET_NULL, null=True, verbose_name='Akagali')

    def __str__(self):
        return self.name

    def address(self):
        return "%s, %s, %s" % (self.f_cell, self.f_sector, self.f_district)


class FonerwaTaxes(models.Model):
    amount = models.FloatField(blank=True, null=True)
    bank = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    date = models.DateField(auto_now=False, default=timezone.now)

    def __str__(self):
        return self.amount


class DistrictTaxes(models.Model):
    amount = models.FloatField(blank=False)
    bank = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    date = models.DateField(auto_now=False, default=timezone.now)

    def __str__(self):
        return self.amount


class HarvestingGuidelines(models.Model):
    code = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=False, null=False)
    summary = models.TextField(auto_created=True, blank=True)

    def __str__(self):
        return self.code


class HarvestingPermit(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True)
    requestor = models.ForeignKey(
        HPRequestor, verbose_name='Usaba', null=True, related_name='permits', on_delete=models.SET_NULL)
    dfnro = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    forest = models.ForeignKey(Forest, on_delete=models.SET_NULL, null=True)
    guidelines = models.ManyToManyField(HarvestingGuidelines, blank=True)
    start_date = models.DateField(auto_now_add=False)
    end_date = models.DateField(auto_now_add=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    date_approved = models.DateField(auto_now=False, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("harvesting_permit_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = permit_code()
        super().save(*args, **kwargs)
