from django import forms
from django.contrib.auth.hashers import make_password
from .models import Owner, Store, Employee

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['full_name', 'contact_information', 'password', 'email_id']

    password = forms.CharField(widget=forms.PasswordInput, label='Password', required=False)

    def save(self, commit=True):
        owner = super().save(commit=False)
        if self.cleaned_data['password']:  # Only update password if provided
            owner.password = make_password(self.cleaned_data['password'])
        if commit:
            owner.save()
        return owner



class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['store_name', 'store_address', 'contact_information', 'owner']



class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'role', 'email', 'gender', 'age', 'store_id']


class LoginForm(forms.Form):
    email = forms.CharField(max_length=50, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

class RegisterOwnerForm(forms.Form):
    full_name = forms.CharField(max_length=50)
    contact_information = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    email_id = forms.EmailField()
    store_name = forms.CharField(max_length=50)
    store_address = forms.CharField(max_length=50)
    store_contact_information = forms.CharField(max_length=50)
