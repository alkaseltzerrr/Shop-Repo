from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Employee, Purchase
from decimal import Decimal

class AdminRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    emergency_contact = forms.CharField(required=True)
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_staff = True
        user.is_superuser = True
        
        if commit:
            user.save()
            profile_picture = self.cleaned_data.get('profile_picture')
            Employee.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                role='MANAGER',
                active=True,
                address=self.cleaned_data['address'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                emergency_contact=self.cleaned_data['emergency_contact'],
                salary=Decimal('5000.00'),
                profile_picture=profile_picture
            )
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'})
        }

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            if profile_picture.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file too large ( > 5MB )")
            return profile_picture

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['supplier', 'product', 'quantity', 'unit_price']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'}),
        }
