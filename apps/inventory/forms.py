from django import forms
from .models import Product, Inventory, Category

# Form for Product
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['productName', 'description', 'price', 'expireyDate', 'categoryID']

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
