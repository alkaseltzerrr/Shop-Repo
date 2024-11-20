from django import forms
from .models import Supplier
from apps.inventory.models import Product

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['SupplierName', 'ContactInformation', 'Address']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['productName', 'description', 'price', 'expireyDate', 'categoryID']
