from django import forms
from .models import Client

class TenantForm(forms.ModelForm):
    # domain_url is removed for subfolder routing
    
    # Fields for the initial admin user
    admin_username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'admin'})
    )
    admin_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Client
        fields = ['name', 'schema_name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "e.g., Bob's Barbell Club"}),
            'schema_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., gym_002 (must be unique, lowercase, no spaces)'}),
        }
