from django import forms
from django.contrib.auth.models import User
from .models import MemberProfile, WeightLog, ExerciseLog, Attendance, Payment, DietPlan

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ['full_name', 'date_of_birth', 'phone_number', 'initial_weight_kg', 'fees_per_month', 'one_time_deposit']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control d-inline-block w-auto'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control d-inline-block w-auto'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control d-inline-block w-auto'}),
            'initial_weight_kg': forms.NumberInput(attrs={'class': 'form-control d-inline-block w-auto'}),
            'fees_per_month': forms.NumberInput(attrs={'class': 'form-control d-inline-block w-auto'}),
            'one_time_deposit': forms.NumberInput(attrs={'class': 'form-control d-inline-block w-auto'}),
        }

class WeightLogForm(forms.ModelForm):
    class Meta:
        model = WeightLog
        fields = ['date', 'weight_kg']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class ExerciseLogForm(forms.ModelForm):
    class Meta:
        model = ExerciseLog
        fields = ['date', 'exercise', 'sets', 'reps', 'weight_lifted_kg', 'duration_minutes', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['date', 'present']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_type', 'amount_paid', 'payment_date', 'month_paid_for']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'month_paid_for': forms.DateInput(attrs={'type': 'date'}),
        }

class DietPlanForm(forms.ModelForm):
    class Meta:
        model = DietPlan
        fields = ['title', 'breakfast', 'lunch', 'dinner', 'snacks', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Summer Shredding Plan'}),
            'breakfast': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'lunch': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'dinner': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'snacks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class CSVImportForm(forms.Form):
    csv_file = forms.FileField(
        label="Select a CSV File",
        help_text="The CSV should contain headers: username, email, full_name, phone_number, initial_weight_kg, fees_per_month",
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
