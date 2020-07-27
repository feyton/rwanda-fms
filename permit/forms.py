from django import forms
from .models import TransportPermit

class AddPermitForm(forms.ModelForm):
    class Meta:
        model = TransportPermit
        fields = '__all__'