from django import forms

from .models import (Address, Cell, Destination, District, OriginLocation,
                     Requestor, Sector, TransportPermit, TransportVehicle)


class AddPermitForm(forms.ModelForm):
    class Meta:
        model = TransportPermit
        fields = ['category', 'quantity', 'start_date', 'end_date']


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
            self.fields['district'].queryset = self.instance.province.districts.order_by(
                'name')


class RequestorForm(forms.ModelForm):
    class Meta:
        model = Requestor
        exclude = ['address']
        widgets = {
            'nid': forms.TextInput(attrs={'class': 'nid-input'}),
            'telephone': forms.TextInput(attrs={'class': ' tel-number'})
        }

    def __init__(self, *args, **kwargs):
        super(RequestorForm, self).__init__(*args, **kwargs)
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
        # if 'r_cell' in self.data:
        #     try:
        #         d_id = int(self.data.get('r_cell'))
        #         self.fields['r_village'].queryset = Village.objects.filter(
        #             cell_id=d_id).order_by('name')
        #     except (ValueError, TypeError):
        #         pass
        # elif self.instance.pk:
        #     self.fields['r_village'].queryset = self.instance.r_cell.villages.order_by(
        #         'name')


class TransportVehicleForm(forms.ModelForm):
    class Meta:
        model = TransportVehicle
        fields = '__all__'
        widgets = {
            'plate': forms.TextInput(attrs={'class': ' plate'}),
            'driver_tel': forms.TextInput(attrs={'class': ' d-number'})
        }


class OriginForm(forms.ModelForm):
    class Meta:
        model = OriginLocation
        exclude = ['code']

    def __init__(self, *args, **kwargs):
        super(OriginForm, self).__init__(*args, **kwargs)
        self.fields['l_district'].queryset = District.objects.none()
        self.fields['l_sector'].queryset = Sector.objects.none()
        self.fields['l_cell'].queryset = Cell.objects.none()
        #self.fields['l_village'].queryset = Village.objects.none()

        if 'l_province' in self.data:
            try:
                p_id = int(self.data.get('l_province'))
                self.fields['l_district'].queryset = District.objects.filter(
                    province_id=p_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['l_district'].queryset = self.instance.l_province.districts.order_by(
                'name')
        if 'l_district' in self.data:
            try:
                d_id = int(self.data.get('l_district'))
                self.fields['l_sector'].queryset = Sector.objects.filter(
                    district_id=d_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['l_sector'].queryset = self.instance.l_district.sectors.order_by(
                'name')
        if 'l_sector' in self.data:
            try:
                d_id = int(self.data.get('l_sector'))
                self.fields['l_cell'].queryset = Cell.objects.filter(
                    sector_id=d_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['l_cell'].queryset = self.instance.l_sector.cells.order_by(
                'name')
        # if 'l_cell' in self.data:
        #     try:
        #         d_id = int(self.data.get('l_cell'))
        #         self.fields['l_village'].queryset = Village.objects.filter(
        #             cell_id=d_id).order_by('name')
        #     except (ValueError, TypeError):
        #         pass
        # elif self.instance.pk:
        #     self.fields['l_village'].queryset = self.instance.l_cell.villages.order_by(
        #         'name')


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = '__all__'
