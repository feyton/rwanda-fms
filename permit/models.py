from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from .utils import permit_code, start_date_default, end_date_default
from django.core.exceptions import ValidationError
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
        Sector, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=200, blank=False,
                            null=False, unique=False)

    def __str__(self):
        return self.name


class Village(models.Model):
    code = models.CharField(max_length=2, blank=True, null=True)
    cell = models.ForeignKey(
        Cell, on_delete=models.CASCADE, blank=False, null=False)
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


class Requestor(models.Model):
    names = models.CharField(
        _('Amazina'), max_length=255, blank=False, null=False)
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True)
    nid = models.CharField(_('Indangamuntu'), max_length=16, blank=True)
    r_province = models.ForeignKey(
        _('Intara'), Province, on_delete=models.CASCADE)
    r_district = models.ForeignKey(District, on_delete=models.CASCADE)
    r_sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    r_cell = models.ForeignKey(
        Cell, on_delete=models.SET_NULL, null=True)
    r_village = models.ForeignKey(
        Village, on_delete=models.SET_NULL, null=True)


class TransportVehicle(models.Model):
    vehicle = models.CharField(max_length=20)
    plate = models.CharField(max_length=10)
    max_q = models.PositiveIntegerField(blank=True, null=True)
    driver = models.CharField(max_length=255)
    driver_tel = models.CharField(max_length=255)

    def __str__(self):
        return self.driver


class OriginLocation(models.Model):
    code = models.CharField(max_length=30, blank=True,
                            null=True, editable=False)
    l_province = models.ForeignKey(Province, on_delete=models.CASCADE)
    l_district = models.ForeignKey(District, on_delete=models.CASCADE)
    l_sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    l_cell = models.ForeignKey(
        Cell, null=True,  on_delete=models.SET_NULL)
    l_village = models.ForeignKey(
        Village, null=True,  on_delete=models.SET_NULL)

    def __str__(self):
        return self.code

    def code_gen(self):
        code = '%s/%s/%s' % (self.l_province.code,
                             self.l_district.code, self.l_sector.code)
        if self.l_cell:
            code = '%s/%s/%s/%s/' % (self.province.code,
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


class TransportPermit(models.Model):
    date = timezone.now()
    code = models.CharField(_('Nomero'), max_length=255, blank=True,
                            null=True, editable=False)
    category = models.ForeignKey(
        Category, on_delete=models.SET_DEFAULT, default=1)
    requestor = models.ForeignKey(
        Requestor, on_delete=models.SET_NULL, null=True)
    vehicle = models.ForeignKey(TransportVehicle, on_delete=models.CASCADE, )
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
        Mayor, on_delete=models.SET_DEFAULT, blank=True, null=True)

    class Meta:
        verbose_name = "transport permit"
        verbose_name_plural = 'transaport permits'

    def __str__(self):
        return "%s <%s>" % (self.name, self.code)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = permit_code()
        super().save(*args, **kwargs)


class HarvestingPermit(models.Model):
    pass
