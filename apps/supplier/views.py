from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Supplier
from .forms import SupplierForm
from apps.inventory.models import Product
from ..inventory.forms import ProductForm


# View to display all suppliers
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier/supplier_list.html', {'suppliers': suppliers})

# View to create a new supplier
def supplier_create(request):
    form = SupplierForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('supplier_list')
    return render(request, 'supplier/supplier_form.html', {'form': form})

# View to update an existing supplier
def supplier_update(request, pk):
    supplier = Supplier.objects.get(pk=pk)
    form = SupplierForm(request.POST or None, instance=supplier)
    if form.is_valid():
        form.save()
        return redirect('supplier_list')
    return render(request, 'supplier/supplier_form.html', {'form': form})

# View to delete a supplier
def supplier_delete(request, pk):
    supplier = Supplier.objects.get(pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'supplier/supplier_confirm_delete.html', {'supplier': supplier})

# View to display all products bought from a supplier
def supplier_product_create(request):
    if request.method == 'POST':
        supplier_form = SupplierForm(request.POST)
        product_form = ProductForm(request.POST)
        if supplier_form.is_valid() and product_form.is_valid():
            supplier = supplier_form.save()
            product = product_form.save(commit=False)
            product.supplier = supplier
            product.save()
            return redirect('supplier_list')
    else:
        supplier_form = SupplierForm()
        product_form = ProductForm()
    return render(request, 'supplier/supplier_product_form.html', {
        'supplier_form': supplier_form,
        'product_form': product_form
    })

#transaction
def buy_view(request):
    if request.method == 'POST':
        supplier_form = SupplierForm(request.POST)
        product_form = ProductForm(request.POST)
        if supplier_form.is_valid() and product_form.is_valid():
            supplier = supplier_form.save()
            product = product_form.save(commit=False)
            product.supplier = supplier
            product.save()

            # Create Sale and SaleDetail
            sale = Sale.objects.create(SaleDate=date.today(), Employee=request.user.employee, Customer=None,
                                       TotalAmount=product.price)
            SaleDetail.objects.create(SaleID=sale, ProductID=product, Quantity=1, UnitPrice=product.price,
                                      PaymentType='Buy')

            return redirect('history')
    else:
        supplier_form = SupplierForm()
        product_form = ProductForm()
    return render(request, 'supplier/supplier_product_form.html', {
        'supplier_form': supplier_form,
        'product_form': product_form
    })
