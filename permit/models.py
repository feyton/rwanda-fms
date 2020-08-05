from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from .utils import permit_code, start_date_default, end_date_default

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


class Mayor(models.Model):
    name = models.CharField(max_length=255)


class TransportPermit(models.Model):
    cats = (('AM', 'Amakara'), ('AS', 'Amasiteri'))
    date = timezone.now()
    code = models.CharField(max_length=10)
    names = models.CharField(
        _('names'), max_length=255, blank=False, null=False)
    address = models.CharField(_('address'), max_length=255, blank=False)
    nid = models.CharField(_('nid'), max_length=16, blank=True)
    location = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(blank=False, null=False)
    from_location = models.CharField(max_length=255)
    to_location = models.CharField(max_length=255)
    forest_owner = models.CharField(max_length=255)
    transport_vehicle = models.CharField(max_length=20)
    vehicle_plate = models.CharField(max_length=10)
    vehicle_max_q = models.PositiveIntegerField(blank=True, null=True)
    driver = models.CharField(max_length=255)
    driver_tel = models.CharField(max_length=255)
    start_date = models.DateField(
        auto_now_add=False, default=start_date_default)
    end_date = models.DateField(auto_now_add=False, default=end_date_default)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    prepared_by = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(
        Mayor, default=0, on_delete=models.SET_DEFAULT)

    class Meta:
        verbose_name = "transport permit"
        verbose_name_plural = 'transaport permits'

    def __str__(self):
        return "%s <%s>" % (self.name, self.code)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = permit_code()
        super().save(*args, **kwargs)
