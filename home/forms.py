
from django import forms
from .models import CustomUser

class KYCForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = CustomUser
        fields = ['date_of_birth', 'address', 'citizenship_id', 'mothers_name', 'fathers_name']