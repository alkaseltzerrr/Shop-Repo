from django import forms
from .models import order, orderDetail
from ..inventory.models import Product


class OrderForm(forms.ModelForm):
    class Meta:
        model = order
        fields = ['OrderDate', 'TotalAmount','SupplierID']

class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = orderDetail
        fields = ['OrderID', 'Quantity', 'UnitPrice','ProductID']
