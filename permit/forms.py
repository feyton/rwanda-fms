from django import forms

from .models import (Address, Cell, District, HarvestingPermit, Sector,
                     TransportPermit, Village, )


class AddPermitForm(forms.ModelForm):
    class Meta:
        model = TransportPermit
        fields = '__all__'


class AddHPermitForm(forms.ModelForm):
    class Meta:
        model = HarvestingPermit
        fields = '__all__'


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'].queryset = District.objects.none()
        self.fields['sector'].queryset = Sector.objects.none()

        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['district'].queryset = District.objects.filter(
                    province_id=province_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.province.district_set.order_by(
                'name')
