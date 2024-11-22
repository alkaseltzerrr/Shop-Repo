from django import forms
from .models import Sale, SaleDetail

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['SaleDate', 'Employee', 'Customer', 'TotalAmount']

class SaleDetailForm(forms.ModelForm):
    class Meta:
        model = SaleDetail
        fields = ['SaleID', 'ProductID', 'Quantity', 'UnitPrice', 'PaymentType']
