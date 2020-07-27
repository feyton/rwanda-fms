from django import forms
from .models import TransportPermit


class TransportPermitForm(forms.ModelForm):
    class Meta:
        model = TransportPermit
        fields = '__all__'
