from django.shortcuts import render, get_object_or_404, redirect
from .models import order, orderDetail
from .forms import OrderForm, OrderDetailForm


def order_list(request):
    orders = order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'order_form.html', {'form': form})

def order_update(request, pk):
    order_instance = get_object_or_404(order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order_instance)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order_instance)
    return render(request, 'order_form.html', {'form': form})

def order_delete(request, pk):
    order_instance = get_object_or_404(order, pk=pk)
    if request.method == 'POST':
        order_instance.delete()
        return redirect('order_list')
    return render(request, 'order_confirm_delete.html', {'order': order_instance})

# CRUD for OrderDetail

def order_detail_list(request, order_id):
    order_instance = get_object_or_404(order, pk=order_id)
    order_details = orderDetail.objects.filter(OrderID=order_instance)
    return render(request, 'order_detail_list.html', {'order': order_instance, 'order_details': order_details})

def order_detail_create(request, order_id):
    order_instance = get_object_or_404(order, pk=order_id)
    if request.method == 'POST':
        form = OrderDetailForm(request.POST)
        if form.is_valid():
            order_detail = form.save(commit=False)
            order_detail.OrderID = order_instance
            order_detail.save()
            return redirect('order_detail_list', order_id=order_id)
    else:
        form = OrderDetailForm()
    return render(request, 'order_detail_form.html', {'form': form, 'order_id': order_id})


def order_detail_update(request, pk):
    order_detail = get_object_or_404(orderDetail, pk=pk)
    if request.method == 'POST':
        form = OrderDetailForm(request.POST, instance=order_detail)
        if form.is_valid():
            form.save()
            return redirect('order_detail_list', order_id=order_detail.OrderID.pk)
    else:
        form = OrderDetailForm(instance=order_detail)
    return render(request, 'order_detail_form.html', {'form': form, 'order_id': order_detail.OrderID.pk})

def order_detail_delete(request, pk):
    order_detail = get_object_or_404(orderDetail, pk=pk)
    order_id = order_detail.OrderID.pk
    if request.method == 'POST':
        order_detail.delete()
        return redirect('order_detail_list', order_id=order_id)
    return render(request, 'order_detail_confirm_delete.html', {'order_detail': order_detail})