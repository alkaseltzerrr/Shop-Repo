from django.shortcuts import render, get_object_or_404, redirect
from .models import Sale, SaleDetail
from .forms import SaleForm, SaleDetailForm


def sale_list(request):
    sales = Sale.objects.all()
    return render(request, 'sale_list.html', {'sales': sales})

def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sale_list')
    else:
        form = SaleForm()
    return render(request, 'sale_form.html', {'form': form})

def sale_update(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect('sale_list')
    else:
        form = SaleForm(instance=sale)
    return render(request, 'sale_form.html', {'form': form})

def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        sale.delete()
        return redirect('sale_list')
    return render(request, 'sale_confirm_delete.html', {'sale': sale})

# CRUD for SaleDetail

def sale_detail_list(request, sale_id):
    sale = get_object_or_404(Sale, pk=sale_id)
    sale_details = SaleDetail.objects.filter(SaleID=sale)
    return render(request, 'sale_detail_list.html', {'sale': sale, 'sale_details': sale_details})

def sale_detail_create(request, sale_id):
    sale_instance = get_object_or_404(Sale, pk=sale_id)
    if request.method == 'POST':
        form = SaleDetailForm(request.POST)
        if form.is_valid():
            sale_detail = form.save(commit=False)
            sale_detail.SaleID = sale_instance
            sale_detail.save()
            return redirect('sale_detail_list', sale_id=sale_id)
    else:
        form = SaleDetailForm()
    return render(request, 'sale_detail_form.html', {'form': form, 'sale_id': sale_id})


def sale_detail_update(request, pk):
    sale_detail = get_object_or_404(SaleDetail, pk=pk)
    if request.method == 'POST':
        form = SaleDetailForm(request.POST, instance=sale_detail)
        if form.is_valid():
            form.save()
            return redirect('sale_detail_list', sale_id=sale_detail.SaleID.pk)
    else:
        form = SaleDetailForm(instance=sale_detail)
    return render(request, 'sale_detail_form.html', {'form': form, 'sale_id': sale_detail.SaleID.pk})

def sale_detail_delete(request, pk):
    sale_detail = get_object_or_404(SaleDetail, pk=pk)
    sale_id = sale_detail.SaleID.pk
    if request.method == 'POST':
        sale_detail.delete()
        return redirect('sale_detail_list', sale_id=sale_id)
    return render(request, 'sale_detail_confirm_delete.html', {'sale_detail': sale_detail})
