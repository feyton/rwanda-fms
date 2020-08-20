from django import forms

from permit.models import Cell, District, Sector

from .models import (ConstructionSpecies, Forest, HarvestingPermit,
                     HPRequestor, TimberSpecies)


class ConstructionSpeciesForm(forms.ModelForm):

    class Meta:
        model = ConstructionSpecies
        fields = ("species", 'width', 'height', 'number')

class TimberSpeciesForm(forms.ModelForm):
    
    class Meta:
        model = TimberSpecies
        fields = ("species",'width', 'height', 'price')


class ForestForm(forms.ModelForm):

    class Meta:
        model = Forest
        fields = ("name", 'owner', 'area', 'upi',
                  'distance', 'f_province', 'f_district', 'f_sector', 'f_cell')


class HPermitForm(forms.ModelForm):
    class Meta:
        model = HarvestingPermit
        fields = ['start_date', 'end_date']


class HPRequestorForm(forms.ModelForm):

    class Meta:
        model = HPRequestor
        fields = '__all__'
        widgets = {
            'nid': forms.TextInput(attrs={'class': 'nid-input'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['r_district'].queryset = District.objects.none()
        self.fields['r_sector'].queryset = Sector.objects.none()
        self.fields['r_cell'].queryset = Cell.objects.none()
        #self.fields['r_village'].queryset = Village.objects.none()

        if 'r_province' in self.data:
            try:
                p_id = int(self.data.get('r_province'))
                self.fields['r_district'].queryset = District.objects.filter(
                    province_id=p_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['r_district'].queryset = self.instance.r_province.districts.order_by(
                'name')
        if 'r_district' in self.data:
            try:
                d_id = int(self.data.get('r_district'))
                self.fields['r_sector'].queryset = Sector.objects.filter(
                    district_id=d_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['r_sector'].queryset = self.instance.r_district.sectors.order_by(
                'name')
        if 'r_sector' in self.data:
            try:
                d_id = int(self.data.get('r_sector'))
                self.fields['r_cell'].queryset = Cell.objects.filter(
                    sector_id=d_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['r_cell'].queryset = self.instance.r_sector.cells.order_by(
                'name')
