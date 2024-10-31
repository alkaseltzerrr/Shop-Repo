from django import forms
from .models import Customer, LoyaltyProgram

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customername', 'contactinformation', 'loyaltypoints']

class LoyaltyProgramForm(forms.ModelForm):
    class Meta:
        model = LoyaltyProgram
        fields = ['customer', 'loyaltytype', 'pointsaccumulated']