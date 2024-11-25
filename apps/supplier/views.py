from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Supplier
from ..inventory.forms import ProductForm
#carls imports
from django.contrib import messages
from .forms import SupplierForm, ProductForm
from ..orders.forms import OrderForm, OrderDetailForm
from ..orders.models import order, orderDetail


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



# Transaction view to create a supplier and a product
def supplier_product_create(request):
    if request.method == 'POST':
        supplier_name = request.POST.get('SupplierName').strip().lower()
        supplier = Supplier.objects.filter(SupplierName__iexact=supplier_name).first()

        if not supplier:
            messages.error(request, 'Supplier not registered')
            supplier_form = SupplierForm(request.POST)
            product_form = ProductForm(request.POST)
            order_form = OrderForm(request.POST)
            order_detail_form = OrderDetailForm(request.POST)
        else:
            supplier_form = SupplierForm(request.POST, instance=supplier)
            product_form = ProductForm(request.POST)
            order_form = OrderForm(request.POST)
            order_detail_form = OrderDetailForm(request.POST)

            if supplier_form.is_valid() and product_form.is_valid() and order_form.is_valid() and order_detail_form.is_valid():
                supplier = supplier_form.save()
                product = product_form.save()
                order_instance = order_form.save(commit=False)
                order_instance.SupplierID = supplier
                order_instance.TotalAmount = order_detail_form.cleaned_data['Quantity'] * order_detail_form.cleaned_data['UnitPrice']
                order_instance.save()

                order_detail = order_detail_form.save(commit=False)
                order_detail.OrderID = order_instance
                order_detail.ProductID = product
                order_detail.save()

                return redirect('order_transaction_history')
            else:
                print("Supplier Form Errors:", supplier_form.errors)
                print("Product Form Errors:", product_form.errors)
                print("Order Form Errors:", order_form.errors)
                print("Order Detail Form Errors:", order_detail_form.errors)
    else:
        supplier_form = SupplierForm()
        product_form = ProductForm()
        order_form = OrderForm()
        order_detail_form = OrderDetailForm()

    return render(request, 'supplier_product_form.html', {
        'supplier_form': supplier_form,
        'product_form': product_form,
        'order_form': order_form,
        'order_detail_form': order_detail_form
    })

def order_transaction_history(request):
    orders = order.objects.all()
    order_details = orderDetail.objects.all()
    return render(request, 'order_transaction_history.html', {
        'orders': orders,
        'order_details': order_details
    })




