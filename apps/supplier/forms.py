from django import forms
from .models import Supplier
from apps.inventory.models import Product

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['SupplierName','ContactInformation','Address']

        def __init__(self, *args, **kwargs):
            super(SupplierForm, self).__init__(*args, **kwargs)
            # Make ContactInformation and Address not required
            self.fields['ContactInformation'].required = False
            self.fields['Address'].required = False

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['productName', 'description', 'price', 'expireyDate', 'categoryID']
# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['OrderDate', 'ProductName', 'Quantity', 'UnitPrice']
#         widgets = {
#             'TotalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
#         }


