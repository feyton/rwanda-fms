from django.contrib import admin

from .models import (Address, Category, Cell, District, Province, Sector,
                     TransportPermit, Village, Mayor, Requestor)

admin.site.register(TransportPermit)
admin.site.register(Province)
admin.site.register(District)
admin.site.register(Sector)
admin.site.register(Cell)
admin.site.register(Village)
admin.site.register(Address)
admin.site.register(Category)
admin.site.register(Mayor)
admin.site.register(Requestor)
