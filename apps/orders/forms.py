from django import forms
from .models import order, orderDetail

class OrderForm(forms.ModelForm):
    class Meta:
        model = order
        fields = ['OrderDate', 'TotalAmount']  # Add SupplierID once it's defined

class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = orderDetail
        fields = ['OrderID', 'Quantity', 'UnitPrice']  # Add ProductID once it's defined
