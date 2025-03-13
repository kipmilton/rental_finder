from django import forms
from .models import Rental

class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['name', 'phone_number', 'email', 'house_type', 'location', 'apartment_name', 'monthly_cost']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'house_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'apartment_name': forms.TextInput(attrs={'class': 'form-control'}),
            'monthly_cost': forms.NumberInput(attrs={'class': 'form-control'}),
        }