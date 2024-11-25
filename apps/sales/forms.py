from django import forms
from .models import Sale, SaleDetail
from ..crm.models import Customer
from ..em.models import Employee

# imoha ni karl
# class SaleForm(forms.ModelForm):
#     class Meta:
#         model = Sale
#         fields = ['SaleDate', 'Employee', 'Customer', 'TotalAmount']
#
# class SaleDetailForm(forms.ModelForm):
#     class Meta:
#         model = SaleDetail
#         fields = ['SaleID', 'ProductID', 'Quantity', 'UnitPrice', 'PaymentType']

#for transaction
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customername', 'contactinformation']




class SaleForm(forms.ModelForm):
    Employee = forms.ModelChoiceField(queryset=Employee.objects.all(), required=True)
    class Meta:
        model = Sale
        fields = ['SaleDate', 'Employee']

class SaleDetailForm(forms.ModelForm):
    class Meta:
        model = SaleDetail
        fields = ['Quantity', 'UnitPrice']
