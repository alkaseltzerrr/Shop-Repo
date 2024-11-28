from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Employee
from decimal import Decimal

class AdminRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    emergency_contact = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_staff = True  # Make user a staff member
        user.is_superuser = True  # Make user a superuser
        
        if commit:
            user.save()
            # Create associated Employee profile
            Employee.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                role='MANAGER',
                active=True,
                address=self.cleaned_data['address'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                emergency_contact=self.cleaned_data['emergency_contact'],
                salary=Decimal('5000.00')
            )
        return user
