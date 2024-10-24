from django import forms
from .models import Sale, SaleDetail

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['SaleDate', 'TotalAmount']  # Add EmployeeID and CustomerID if needed

class SaleDetailForm(forms.ModelForm):
    class Meta:
        model = SaleDetail
        fields = ['SaleID', 'Quantity', 'UnitPrice', 'PaymentType']  # Add ProductID if needed
