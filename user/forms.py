from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from permit.models import Cell, Sector

from .models import Profile

User = get_user_model()


class CreateUserForm(UserCreationForm):
    """
    New User Form. Requires password confirmation.
    """
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UpdateProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sector'].queryset = Sector.objects.none()
        self.fields['cell'].queryset = Cell.objects.none()
        if 'district' in self.data:
            try:
                d_id = int(self.data.get('district'))
                self.fields['sector'].queryset = Sector.objects.filter(
                    district_id=d_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.district is not None:
            self.fields['sector'].queryset = self.instance.district.sectors.order_by(
                'name')
        if 'sector' in self.data:
            try:
                d_id = int(self.data.get('sector'))
                self.fields['cell'].queryset = Cell.objects.filter(
                    sector_id=d_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.sector is not None:
            self.fields['cell'].queryset = self.instance.sector.cells.order_by(
                'name')
    class Meta:
        model = Profile
        fields = ['image', 'biography', 'district', 'sector', 'cell']
        widgets = {
            'biography': forms.Textarea(attrs={'rows': 3, 'cols': 60}),
        }


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
