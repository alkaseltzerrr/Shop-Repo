from django import forms
from .models import Owner, Store, Employee

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['full_name', 'contact_information', 'password', 'email_id']


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['store_name', 'store_address', 'contact_information', 'owner']



class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'role', 'email', 'gender', 'age']

# class LoginForm(forms.Form):  # Changed from ModelForm to Form
#     email_id = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)