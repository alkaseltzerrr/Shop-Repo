
from django import forms
from django.utils import timezone

from .models import Product, Inventory, Category

# Form for Product
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['productName', 'description', 'price', 'expireyDate', 'categoryID']#gwapo

# Form for Category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['categoryName']

# Form for Inventory
class InventoryForm(forms.ModelForm):
    categoryID = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, label='Category')
    price = forms.FloatField(required=True, label='Price')

    class Meta:
        model = Inventory
        fields = ['productID', 'quantity', 'lastUpdate', 'categoryID', 'price']

class CombinedProductInventoryForm(forms.Form):
    # Fields from ProductForm
    productName = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea, required=False)
    price = forms.FloatField()
    expireyDate = forms.DateField()
    categoryID = forms.ModelChoiceField(queryset=Category.objects.all())

    # Fields from InventoryForm
    quantity = forms.IntegerField()
    lastUpdate = forms.DateField(widget=forms.HiddenInput(), initial=timezone.now)