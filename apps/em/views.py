from django.shortcuts import render, redirect, get_object_or_404

from . import forms
from .models import Owner, Store, Employee
from .forms import OwnerForm, StoreForm, EmployeeForm, RegisterOwnerForm  # , LoginForm
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .forms import LoginForm

# -------------- OWNER CRUD ----------------
def owner_list(request):
    owners = Owner.objects.all()
    owners_data = [owner.to_dict() for owner in owners]
    return render(request, 'owner_list.html', {'owners': owners_data})

def owner_create(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('owner_list')
            except IntegrityError:
                form.add_error('email_id', 'An owner with this email_id already exists.')
    else:
        form = OwnerForm()
    return render(request, 'owner_form.html', {'form': form})

def owner_update(request, pk):
    owner = get_object_or_404(Owner, pk=pk)
    if request.method == 'POST':
        form = OwnerForm(request.POST, request.FILES, instance=owner)
        if form.is_valid():
            try:
                form.save()
                return redirect('owner_list')
            except IntegrityError:
                form.add_error('email_id', 'An owner with this email_id already exists.')
    else:
        form = OwnerForm(instance=owner)
    return render(request, 'owner_form.html', {'form': form})

def owner_delete(request, pk):
    owner = get_object_or_404(Owner, pk=pk)
    if request.method == 'POST':
        owner.delete()
        return redirect('owner_list')
    return render(request, 'owner_confirm_delete.html', {'owner': owner})

# -------------- STORE CRUD ----------------
def store_list(request):
    stores = Store.objects.all()
    return render(request, 'store_list.html', {'stores': stores})

def store_create(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store_list')
    else:
        form = StoreForm()
    return render(request, 'store_form.html', {'form': form})

def store_update(request, pk):
    store = get_object_or_404(Store, pk=pk)
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            return redirect('store_list')
    else:
        form = StoreForm(instance=store)
    return render(request, 'store_form.html', {'form': form})

def store_delete(request, pk):
    store = get_object_or_404(Store, pk=pk)
    if request.method == 'POST':
        store.delete()
        return redirect('store_list')
    return render(request, 'store_confirm_delete.html', {'store': store})

# -------------- EMPLOYEE CRUD ----------------
def employee_list(request):
    employees = Employee.objects.all()
    form = EmployeeForm()
    return render(request, 'employee_list.html', {'employees': employees, 'form': form})

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})

def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_form.html', {'form': form})

def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employee_confirm_delete.html', {'employee': employee})

# -------------- Log in ----------------
def owner_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                owner = Owner.objects.get(email_id=email)
            except Owner.DoesNotExist:
                owner = None

            # Check if owner exists and the password is correct
            if owner and check_password(password, owner.password):
                # Perform login
                request.session['owner_id'] = owner.owner_id  # Store owner in session
                messages.success(request, "Login successful!")
                messages.success(request, f"Welcome, {owner.full_name}!")
                return redirect('home')  # Redirect to owner's list or any other page
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def owner_register(request):
    if request.method == 'POST':
        form = RegisterOwnerForm(request.POST)
        if form.is_valid():
            owner = Owner(
                full_name=form.cleaned_data['full_name'],
                contact_information=form.cleaned_data['contact_information'],
                password=form.cleaned_data['password'],
                email_id=form.cleaned_data['email_id'],
            )
            owner.save()
            store = Store(
                store_name=form.cleaned_data['store_name'],
                store_address=form.cleaned_data['store_address'],
                contact_information=form.cleaned_data['store_contact_information'],
                owner=owner
            )
            store.save()
            return redirect('login')
    else:
        form = RegisterOwnerForm()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'RegisterOwner.html', {'form': form})

    return render(request, 'RegisterOwner.html', {'form': form})