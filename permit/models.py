from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from .utils import permit_code, start_date_default, end_date_default
from django.core.exceptions import ValidationError
from django.shortcuts import reverse
User = get_user_model()


class Province(models.Model):
    code = models.CharField(max_length=2, blank=True, null=True)
    name = models.CharField(blank=False, null=False, max_length=255)

    def __str__(self):
        return self.name


class District(models.Model):
    code = models.CharField(max_length=2, blank=True, null=True)
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, null=False, blank=False, related_name='districts')
    name = models.CharField(blank=False, null=False, max_length=255)

    def __str__(self):
        return self.name


class Sector(models.Model):
    code = models.CharField(max_length=2, blank=True, null=True)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, blank=False, null=False, related_name='sectors')
    name = models.CharField(max_length=100, unique=False,
                            null=False, blank=False)

    def __str__(self):
        return self.name


class Cell(models.Model):
    code = models.CharField(max_length=2, blank=True, null=True)
    sector = models.ForeignKey(
        Sector, on_delete=models.CASCADE, blank=False, null=False, related_name='cells')
    name = models.CharField(max_length=200, blank=False,
                            null=False, unique=False)

    def __str__(self):
        return self.name


class Village(models.Model):
    code = models.CharField(max_length=2, blank=True, null=True)
    cell = models.ForeignKey(
        Cell, on_delete=models.CASCADE, blank=False, null=False, related_name='villages')
    name = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.name


class Address(models.Model):
    code = models.CharField(max_length=20, blank=True, null=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    cell = models.ForeignKey(
        Cell, null=True, blank=True, on_delete=models.SET_NULL)
    village = models.ForeignKey(
        Village, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.province.name

    def code_gen(self):
        code = '%s/%s/%s' % (self.province.code,
                             self.district.code, self.sector.code)
        if self.cell:
            code = '%s/%s/%s/%s/' % (self.province.code,
                                     self.district.code, self.sector.code, self.cell.code)

        return code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.code_gen()
        super().save(*args, **kwargs)


class Mayor(models.Model):
    name = models.CharField(max_length=255)


class Category(models.Model):
    cats = (('AM', 'Amakara'), ('AS', 'Amasiteri'),
            ('IM', 'Imbaho'), ('IB', 'Ibiti'))
    name = models.CharField(_('Ubwoko'), max_length=2, choices=cats)
    measure = models.CharField(
        _('Urugero'), max_length=50, blank=True, default='Amasiteri')
    minimum = models.IntegerField(_('Ingano ntoya'), default=10)

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name_plural = 'categories'


class Requestor(models.Model):
    names = models.CharField(
        _('Amazina'), max_length=255, blank=False, null=False)
    nid = models.CharField(
        _('Indangamuntu'), max_length=16, blank=True, null=True)
    telephone = models.CharField(
        _('telephone'), max_length=15, blank=True, null=True)
    r_province = models.ForeignKey(
        Province, on_delete=models.SET, null=True, verbose_name='Intara')
    r_district = models.ForeignKey(
        District, on_delete=models.SET, null=True, verbose_name='Akarere')
    r_sector = models.ForeignKey(
        Sector, on_delete=models.SET, null=True, verbose_name='Umurenge')
    r_cell = models.ForeignKey(
        Cell, on_delete=models.SET_NULL, null=True, verbose_name='Akagali')
    r_village = models.ForeignKey(
        Village, on_delete=models.SET_NULL, null=True, verbose_name='Umudugudu')


class TransportVehicle(models.Model):
    cats = (('FS', 'FUSSO'), ('BN', 'BEN'), ('DH', 'DAIHATSU'))
    vehicle = models.CharField(
        _('Ubwoko'), max_length=20, choices=cats, default='FS')
    plate = models.CharField(_('Plake'), max_length=10)
    max_q = models.PositiveIntegerField(
        blank=True, null=True, verbose_name='Ibyo itwara')
    driver = models.CharField(_('Umushoferi'), max_length=255)
    driver_tel = models.CharField(_("Nimero y'umushoferi"), max_length=255)

    def __str__(self):
        return self.driver


class OriginLocation(models.Model):
    code = models.CharField(max_length=30, blank=True,
                            null=True, editable=False)
    l_province = models.ForeignKey(
        Province, on_delete=models.CASCADE, verbose_name='Intara')
    l_district = models.ForeignKey(
        District, on_delete=models.CASCADE, verbose_name='Akarere')
    l_sector = models.ForeignKey(
        Sector, on_delete=models.CASCADE, verbose_name='Umurenge')
    l_cell = models.ForeignKey(
        Cell, null=True, on_delete=models.SET_NULL, verbose_name='Akagali')
    l_village = models.ForeignKey(
        Village, null=True, on_delete=models.SET_NULL, verbose_name='Umudugudu')

    def __str__(self):
        return self.code

    def code_gen(self):
        code = '%s/%s/%s' % (self.l_province.code,
                             self.l_district.code, self.l_sector.code)
        if self.l_cell:
            code = '%s/%s/%s/%s/' % (self.l_province.code,
                                     self.l_district.code, self.l_sector.code, self.l_cell.code)
        return code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.code_gen()
        super().save(*args, **kwargs)


class Destination(models.Model):
    d_province = models.ForeignKey(
        Province, on_delete=models.CASCADE, null=True, blank=True)
    d_district = models.ForeignKey(
        District, on_delete=models.CASCADE, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.d_province and self.location is None:
            raise ValidationError('You must provide a destination')

        elif self.d_province is not None and self.d_district is None:
            raise ValidationError('District is required for full address')
        elif self.d_district and self.location and self.d_province is None:
            self.d_district = None

        super().save(*args, **kwargs)

    def __str__(self):
        if self.location:
            return self.location

        return '%s-%s' % (self.d_province, self.d_district)

    def dest(self):
        if self.d_province:
            return '%s, %s' % (self.d_district, self.d_province)
        else:
            return "%s" % self.location


class TransportPermit(models.Model):
    code = models.CharField(_('Nomero'), max_length=255, blank=True,
                            null=True, editable=False)
    category = models.ForeignKey(
        Category, on_delete=models.SET_DEFAULT, default=1)
    requestor = models.ForeignKey(
        Requestor, on_delete=models.SET_NULL, null=True)
    vehicle = models.ForeignKey(
        TransportVehicle, on_delete=models.CASCADE, null=True)
    origin = models.ForeignKey(
        OriginLocation, on_delete=models.SET_NULL, null=True)
    destination = models.ForeignKey(
        Destination, on_delete=models.SET_NULL, null=True, blank=False)
    quantity = models.PositiveIntegerField(blank=False, null=False)

    start_date = models.DateField(
        auto_now_add=False, default=start_date_default)
    end_date = models.DateField(auto_now_add=False, default=end_date_default)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    prepared_by = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(
        Mayor, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = "transport permit"
        verbose_name_plural = 'transport permits'

    def __str__(self):
        return "%s <%s>" % (self.request.names, self.code)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = permit_code()
        super().save(*args, **kwargs)

    def approved(self):
        if self.approved_by is None:
            raise ValidationError('You must provide an approver')
        else:
            return True

    def get_absolute_url(self):
        return reverse('tp-single-view', kwargs={'pk': self.pk})


class HarvestingPermit(models.Model):
    pass
