from django.contrib import admin
from .models import TransportPermit, Province, District, Sector, Cell, Village, Address

admin.site.register(TransportPermit)
admin.site.register(Province)
admin.site.register(District)
admin.site.register(Sector)
admin.site.register(Cell)
admin.site.register(Village)
admin.site.register(Address)
