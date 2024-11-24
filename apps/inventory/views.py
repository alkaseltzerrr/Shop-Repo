from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Inventory, Category
from .forms import ProductForm, InventoryForm, CategoryForm, CombinedProductInventoryForm
from datetime import date

# Product Views
# READ: List all products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

# CREATE: Add a new product
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form})

# UPDATE: Update a product
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form})

# DELETE: Delete a product
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})

#===================================================================================================================
# Category Views
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'inventory/category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'inventory/category_form.html', {'form': form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'inventory/category_form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'inventory/category_confirm_delete.html', {'category': category})


#===================================================================================================================
# Inventory views
def inventory_list(request):
    inventory = Inventory.objects.all()
    inventory_data = []

    for item in inventory:
        inventory_data.append({
            'pk': item.pk,
            'productName': item.productID.productName,
            'quantity': item.quantity,
            'price': item.productID.price
        })

    form = InventoryForm()  # Add this line to pass the form to the template
    return render(request, 'inventory/inventory_list.html', {'inventory_data': inventory_data, 'form': form})

def inventory_create(request):
    if request.method == 'POST':
        form = CombinedProductInventoryForm(request.POST)
        if form.is_valid():
            # Save Product
            product = Product(
                productName=form.cleaned_data['productName'],#
                description=form.cleaned_data['description'],
                price=form.cleaned_data['price'],#
                expireyDate=form.cleaned_data['expireyDate'],
                categoryID=form.cleaned_data['categoryID']
            )
            product.save()

            # Save Inventory
            inventory = Inventory(
                productID=product,
                quantity=form.cleaned_data['quantity'],#
                lastUpdate=form.cleaned_data['lastUpdate']#
            )
            inventory.save()

            return redirect('inventory_list')
    else:
        form = CombinedProductInventoryForm()
    return render(request, 'inventory/inventory_form.html', {'form': form})

def inventory_update(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    product = inventory.productID

    if request.method == 'POST':
        form = CombinedProductInventoryForm(request.POST)
        if form.is_valid():
            # Update Product
            product.productName = form.cleaned_data['productName']
            product.description = form.cleaned_data['description']
            product.price = form.cleaned_data['price']
            product.expireyDate = form.cleaned_data['expireyDate']
            product.categoryID = form.cleaned_data['categoryID']
            product.save()

            # Update Inventory
            inventory.quantity = form.cleaned_data['quantity']
            inventory.lastUpdate = form.cleaned_data['lastUpdate']
            inventory.save()

            return redirect('inventory_list')
    else:
        initial_data = {
            'productName': product.productName,
            'description': product.description,
            'price': product.price,
            'expireyDate': product.expireyDate,
            'categoryID': product.categoryID,
            'quantity': inventory.quantity,
            'lastUpdate': inventory.lastUpdate,
        }
        form = CombinedProductInventoryForm(initial=initial_data)

    return render(request, 'inventory/inventory_form.html', {'form': form})

def inventory_delete(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        inventory.delete()
        return redirect('inventory_list')
    return render(request, 'inventory/inventory_confirm_delete.html', {'inventory': inventory})

# Expiry classes


def near_expiry(request):
    inventory = Inventory.objects.all()
    near_expiry_data = []

    for item in inventory:
        days_left = (item.productID.expireyDate - date.today()).days
        if days_left < 0:
            days_left = "expired"
        near_expiry_data.append({
            'productID': item.productID.productID,
            'productName': item.productID.productName,
            'quantity': item.quantity,
            'days_left': days_left
        })

    return render(request, 'inventory/near_expiry.html', {'near_expiry_data': near_expiry_data})
