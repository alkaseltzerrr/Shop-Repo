from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, F
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import json
from .models import (
    Category, Product, Supplier, Employee,
    Customer, Purchase, Sale, SaleItem
)

# Dashboard View
@login_required
def dashboard(request):
    # Get today's date
    today = timezone.now().date()
    
    # Calculate statistics
    total_sales_today = Sale.objects.filter(
        sale_date__date=today
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    sales_count_today = Sale.objects.filter(sale_date__date=today).count()
    
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(
        stock_quantity__lte=F('reorder_level')
    )
    low_stock_count = low_stock_products.count()
    
    total_customers = Customer.objects.count()
    new_customers_today = Customer.objects.filter(
        created_at__date=today
    ).count()
    
    pending_orders = Purchase.objects.filter(received=False).count()
    orders_today = Purchase.objects.filter(
        purchase_date__date=today
    ).count()
    
    # Get recent sales
    recent_sales = Sale.objects.select_related('customer').order_by(
        '-sale_date'
    )[:10]
    
    # Prepare sales chart data
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    
    sales_data = []
    dates = []
    
    current_date = start_date
    while current_date <= end_date:
        daily_sales = Sale.objects.filter(
            sale_date__date=current_date
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        sales_data.append(float(daily_sales))
        dates.append(current_date.strftime('%Y-%m-%d'))
        
        current_date += timedelta(days=1)
    
    context = {
        'total_sales_today': total_sales_today,
        'sales_count_today': sales_count_today,
        'total_products': total_products,
        'low_stock_count': low_stock_count,
        'total_customers': total_customers,
        'new_customers_today': new_customers_today,
        'pending_orders': pending_orders,
        'orders_today': orders_today,
        'recent_sales': recent_sales,
        'low_stock_products': low_stock_products[:5],
        'sales_data': json.dumps(sales_data),
        'dates': json.dumps(dates),
    }
    
    return render(request, 'store_ops/dashboard.html', context)

# Product Views
@login_required
def product_list(request):
    products = Product.objects.select_related('category', 'supplier').all()
    categories = Category.objects.all()
    suppliers = Supplier.objects.filter(active=True)
    return render(request, 'store_ops/product_list.html', {
        'products': products,
        'categories': categories,
        'suppliers': suppliers
    })

@login_required
def product_add(request):
    if request.method == 'POST':
        try:
            category = Category.objects.get(id=request.POST.get('category'))
            supplier = Supplier.objects.get(id=request.POST.get('supplier'))
            product = Product.objects.create(
                name=request.POST.get('name'),
                sku=request.POST.get('sku'),
                category=category,
                supplier=supplier,
                description=request.POST.get('description'),
                price=request.POST.get('price'),
                stock_quantity=request.POST.get('stock_quantity', 0),
                reorder_level=request.POST.get('reorder_level', 0)
            )
            messages.success(request, f'Product {product.name} added successfully.')
            return redirect('product_list')
        except Exception as e:
            messages.error(request, f'Error adding product: {str(e)}')
    return redirect('product_list')

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        try:
            category = Category.objects.get(id=request.POST.get('category'))
            supplier = Supplier.objects.get(id=request.POST.get('supplier'))
            product.name = request.POST.get('name')
            product.sku = request.POST.get('sku')
            product.category = category
            product.supplier = supplier
            product.description = request.POST.get('description')
            product.price = request.POST.get('price')
            product.stock_quantity = request.POST.get('stock_quantity')
            product.reorder_level = request.POST.get('reorder_level')
            product.save()
            messages.success(request, f'Product {product.name} updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')
    return redirect('product_list')

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        try:
            name = product.name
            product.delete()
            messages.success(request, f'Product {name} deleted successfully.')
        except Exception as e:
            messages.error(request, f'Error deleting product: {str(e)}')
    return redirect('product_list')

# Inventory Views
@login_required
def inventory(request):
    low_stock = Product.objects.filter(
        stock_quantity__lte=F('reorder_level')
    )
    products = Product.objects.all().order_by('name')
    return render(request, 'store_ops/inventory.html', {
        'products': products,
        'low_stock': low_stock
    })

@login_required
def stock_in(request):
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=request.POST.get('product'))
            quantity = int(request.POST.get('quantity'))
            product.stock_quantity += quantity
            product.save()
            
            Purchase.objects.create(
                product=product,
                supplier=product.supplier,
                quantity=quantity,
                unit_price=float(request.POST.get('unit_price')),
                total_amount=quantity * float(request.POST.get('unit_price')),
                received=True
            )
            messages.success(request, f'Successfully added {quantity} units to {product.name}')
        except Exception as e:
            messages.error(request, f'Error processing stock in: {str(e)}')
    return redirect('inventory')

@login_required
def stock_out(request):
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=request.POST.get('product'))
            quantity = int(request.POST.get('quantity'))
            if product.stock_quantity >= quantity:
                product.stock_quantity -= quantity
                product.save()
                messages.success(request, f'Successfully removed {quantity} units from {product.name}')
            else:
                messages.error(request, f'Insufficient stock for {product.name}')
        except Exception as e:
            messages.error(request, f'Error processing stock out: {str(e)}')
    return redirect('inventory')

@login_required
def adjust_stock(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        try:
            new_quantity = int(request.POST.get('stock_quantity'))
            product.stock_quantity = new_quantity
            product.save()
            messages.success(request, f'Stock adjusted for {product.name}')
        except Exception as e:
            messages.error(request, f'Error adjusting stock: {str(e)}')
    return redirect('inventory')

# Sales Views
@login_required
def sales(request):
    if request.method == 'POST':
        # Process sale form
        pass
    recent_sales = Sale.objects.select_related(
        'customer', 'employee'
    ).order_by('-sale_date')[:50]
    return render(request, 'store_ops/sales.html', {'sales': recent_sales})

@login_required
def process_sale(request):
    if request.method == 'POST':
        try:
            # Create sale record
            customer = None
            if request.POST.get('customer'):
                customer = Customer.objects.get(id=request.POST.get('customer'))
            
            sale = Sale.objects.create(
                customer=customer,
                employee=request.user.employee,
                payment_method=request.POST.get('payment_method'),
                total_amount=0
            )
            
            # Process sale items
            items_data = json.loads(request.POST.get('items'))
            total_amount = 0
            
            for item in items_data:
                product = Product.objects.get(id=item['product_id'])
                quantity = int(item['quantity'])
                
                if product.stock_quantity >= quantity:
                    product.stock_quantity -= quantity
                    product.save()
                    
                    subtotal = quantity * product.price
                    total_amount += subtotal
                    
                    SaleItem.objects.create(
                        sale=sale,
                        product=product,
                        quantity=quantity,
                        unit_price=product.price,
                        subtotal=subtotal
                    )
                else:
                    sale.delete()
                    messages.error(request, f'Insufficient stock for {product.name}')
                    return redirect('sales')
            
            # Update sale total and customer loyalty points
            sale.total_amount = total_amount
            sale.save()
            
            if customer:
                points_earned = int(total_amount)
                customer.loyalty_points += points_earned
                customer.save()
            
            messages.success(request, f'Sale #{sale.id} processed successfully')
            return redirect('sale_details', pk=sale.id)
            
        except Exception as e:
            messages.error(request, f'Error processing sale: {str(e)}')
    return redirect('sales')

@login_required
def sale_details(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'store_ops/sale_details.html', {'sale': sale})

# Customer Views
@login_required
def customer_list(request):
    customers = Customer.objects.all().order_by('first_name', 'last_name')
    return render(request, 'store_ops/customer_list.html', {'customers': customers})

@login_required
def customer_add(request):
    if request.method == 'POST':
        try:
            customer = Customer.objects.create(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address')
            )
            messages.success(request, f'Customer {customer.get_full_name()} added successfully.')
        except Exception as e:
            messages.error(request, f'Error adding customer: {str(e)}')
    return redirect('customer_list')

@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        try:
            customer.first_name = request.POST.get('first_name')
            customer.last_name = request.POST.get('last_name')
            customer.email = request.POST.get('email')
            customer.phone = request.POST.get('phone')
            customer.address = request.POST.get('address')
            customer.loyalty_points = int(request.POST.get('loyalty_points', 0))
            customer.save()
            messages.success(request, f'Customer {customer.get_full_name()} updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating customer: {str(e)}')
    return redirect('customer_list')

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        try:
            name = customer.get_full_name()
            customer.delete()
            messages.success(request, f'Customer {name} deleted successfully.')
        except Exception as e:
            messages.error(request, f'Error deleting customer: {str(e)}')
    return redirect('customer_list')

# Supplier Views
@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all().order_by('name')
    return render(request, 'store_ops/supplier_list.html', {'suppliers': suppliers})

@login_required
def supplier_add(request):
    if request.method == 'POST':
        try:
            supplier = Supplier.objects.create(
                name=request.POST.get('name'),
                contact_person=request.POST.get('contact_person'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                active=request.POST.get('active') == 'on'
            )
            messages.success(request, f'Supplier {supplier.name} added successfully.')
        except Exception as e:
            messages.error(request, f'Error adding supplier: {str(e)}')
    return redirect('supplier_list')

@login_required
def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        try:
            supplier.name = request.POST.get('name')
            supplier.contact_person = request.POST.get('contact_person')
            supplier.email = request.POST.get('email')
            supplier.phone = request.POST.get('phone')
            supplier.address = request.POST.get('address')
            supplier.active = request.POST.get('active') == 'on'
            supplier.save()
            messages.success(request, f'Supplier {supplier.name} updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating supplier: {str(e)}')
    return redirect('supplier_list')

@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        try:
            name = supplier.name
            supplier.delete()
            messages.success(request, f'Supplier {name} deleted successfully.')
        except Exception as e:
            messages.error(request, f'Error deleting supplier: {str(e)}')
    return redirect('supplier_list')

# Employee Views
@login_required
def employee_list(request):
    if not request.user.employee.role == 'MANAGER':
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    employees = Employee.objects.select_related('user').all()
    return render(request, 'store_ops/employee_list.html', {'employees': employees})

@login_required
def employee_add(request):
    if not request.user.employee.role == 'MANAGER':
        messages.error(request, 'You do not have permission to add employees.')
        return redirect('employee_list')
        
    if request.method == 'POST':
        try:
            # Create user account
            user = User.objects.create_user(
                username=request.POST.get('username'),
                email=request.POST.get('email'),
                password=request.POST.get('password'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name')
            )
            
            # Create employee profile
            employee = Employee.objects.create(
                user=user,
                phone=request.POST.get('phone'),
                role=request.POST.get('role'),
                active=request.POST.get('active') == 'on'
            )
            messages.success(request, f'Employee {employee.user.get_full_name()} added successfully.')
        except Exception as e:
            messages.error(request, f'Error adding employee: {str(e)}')
    return redirect('employee_list')

@login_required
def employee_edit(request, pk):
    if not request.user.employee.role == 'MANAGER':
        messages.error(request, 'You do not have permission to edit employees.')
        return redirect('employee_list')
        
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        try:
            # Update user information
            employee.user.username = request.POST.get('username')
            employee.user.email = request.POST.get('email')
            employee.user.first_name = request.POST.get('first_name')
            employee.user.last_name = request.POST.get('last_name')
            
            # Update password if provided
            password = request.POST.get('password')
            if password:
                employee.user.set_password(password)
            
            employee.user.save()
            
            # Update employee information
            employee.phone = request.POST.get('phone')
            employee.role = request.POST.get('role')
            employee.active = request.POST.get('active') == 'on'
            employee.save()
            
            messages.success(request, f'Employee {employee.user.get_full_name()} updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating employee: {str(e)}')
    return redirect('employee_list')

@login_required
def employee_delete(request, pk):
    if not request.user.employee.role == 'MANAGER':
        messages.error(request, 'You do not have permission to delete employees.')
        return redirect('employee_list')
        
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        try:
            name = employee.user.get_full_name()
            employee.user.delete()  # This will also delete the employee due to CASCADE
            messages.success(request, f'Employee {name} deleted successfully.')
        except Exception as e:
            messages.error(request, f'Error deleting employee: {str(e)}')
    return redirect('employee_list')

@login_required
def profile(request):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        employee = None
    
    context = {
        'employee': employee
    }
    return render(request, 'store_ops/profile.html', context)
