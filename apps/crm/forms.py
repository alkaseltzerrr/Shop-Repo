from django import forms
from .models import Customer, LoyaltyProgram

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customername', 'contactinformation','loyaltypoints']

        # def __init__(self, *args, **kwargs):
        #     super(CustomerForm, self).__init__(*args, **kwargs)
        #     self.fields['loyaltypoints'].required = False

class LoyaltyProgramForm(forms.ModelForm):
    class Meta:
        model = LoyaltyProgram
        fields = ['customer', 'loyaltytype', 'pointsaccumulated']