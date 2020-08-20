from django.contrib import admin

from .models import ConstructionSpecies, HarvestingPermit, HPRequestor

admin.site.register(HPRequestor)
admin.site.register(HarvestingPermit)
admin.site.register(ConstructionSpecies)
