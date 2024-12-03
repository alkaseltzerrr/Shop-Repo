from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, F, Q
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import json
from .models import (
    Category, Product, Supplier, Employee,
    Customer, Purchase, Sale, SaleItem, UserPreferences
)
from .forms import AdminRegistrationForm, PurchaseOrderForm
from django.http import JsonResponse
from functools import wraps
from decimal import Decimal

def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request.user, 'employee'):
                messages.error(request, 'Employee profile not found.')
                return redirect('dashboard')
            
            if request.user.employee.role == 'MANAGER' or request.user.employee.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('dashboard')
        return _wrapped_view
    return decorator

# Dashboard View
@login_required
def dashboard(request):
    # Get today's date
    today = timezone.now().date()
    first_day_of_month = today.replace(day=1)
    
    # Calculate first day of quarter
    current_month = today.month
    current_quarter = (current_month - 1) // 3 + 1
    first_month_of_quarter = 3 * (current_quarter - 1) + 1
    first_day_of_quarter = today.replace(month=first_month_of_quarter, day=1)
    
    # Calculate first day of year
    first_day_of_year = today.replace(month=1, day=1)
    
    # Calculate statistics
    total_sales_today = Sale.objects.filter(
        sale_date__date=today
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    sales_count_today = Sale.objects.filter(sale_date__date=today).count()
    
    # Product Statistics
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(
        stock_quantity__lte=F('reorder_level')
    )
    low_stock_count = low_stock_products.count()
    
    # Popular and Least Popular Products
    product_sales = SaleItem.objects.values('product__name', 'product_id').annotate(
        total_sales=Sum('subtotal'),
        total_quantity=Sum('quantity')
    ).order_by('-total_sales')
    popular_products = product_sales[:5]
    least_popular_products = product_sales.order_by('total_sales')[:5]
    
    # Customer Statistics
    total_customers = Customer.objects.count()
    new_customers_today = Customer.objects.filter(
        created_at__date=today
    ).count()
    
    # Most and Least Loyal Customers
    loyal_customers = Customer.objects.exclude(loyalty_points=0).order_by('-loyalty_points')[:5]
    least_loyal_customers = Customer.objects.exclude(loyalty_points=0).order_by('loyalty_points')[:5]
    
    # Order Statistics
    pending_orders = Purchase.objects.filter(received=False, cancelled=False).count()
    received_orders = Purchase.objects.filter(received=True).count()
    cancelled_orders = Purchase.objects.filter(cancelled=True).count()
    orders_today = Purchase.objects.filter(
        purchase_date__date=today
    ).count()
    
    # Calculate total sales and count for this month
    total_sales_month = Sale.objects.filter(
        sale_date__date__gte=first_day_of_month,
        sale_date__date__lte=today
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    sales_count_month = Sale.objects.filter(
        sale_date__date__gte=first_day_of_month,
        sale_date__date__lte=today
    ).count()
    
    # Calculate total sales and count for this quarter
    total_sales_quarter = Sale.objects.filter(
        sale_date__date__gte=first_day_of_quarter,
        sale_date__date__lte=today
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    sales_count_quarter = Sale.objects.filter(
        sale_date__date__gte=first_day_of_quarter,
        sale_date__date__lte=today
    ).count()
    
    # Calculate total sales and count for this year
    total_sales_year = Sale.objects.filter(
        sale_date__date__gte=first_day_of_year,
        sale_date__date__lte=today
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    sales_count_year = Sale.objects.filter(
        sale_date__date__gte=first_day_of_year,
        sale_date__date__lte=today
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
        'total_sales_month': total_sales_month,
        'sales_count_month': sales_count_month,
        'total_sales_quarter': total_sales_quarter,
        'sales_count_quarter': sales_count_quarter,
        'total_sales_year': total_sales_year,
        'sales_count_year': sales_count_year,
        'recent_sales': recent_sales,
        'low_stock_products': low_stock_products[:5],
        'sales_data': json.dumps(sales_data),
        'dates': json.dumps(dates),
        'popular_products': popular_products,
        'least_popular_products': least_popular_products,
        'loyal_customers': loyal_customers,
        'least_loyal_customers': least_loyal_customers,
        'received_orders': received_orders,
        'cancelled_orders': cancelled_orders,
    }
    
    return render(request, 'store_ops/dashboard.html', context)

# Product Views
@login_required
@role_required('MANAGER', 'STOCK_CLERK', 'CASHIER', 'SALES_ASSOCIATE')
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
        'stock_status': 'Low' if product.stock_quantity <= product.reorder_level else 'Normal',
    }
    return render(request, 'store_ops/product_detail.html', context)

@login_required
@role_required('MANAGER', 'STOCK_CLERK', 'CASHIER', 'SALES_ASSOCIATE')
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
@role_required('MANAGER', 'STOCK_CLERK')
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
@role_required('MANAGER', 'STOCK_CLERK')
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
@role_required('MANAGER')
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
@role_required('MANAGER', 'STOCK_CLERK')
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
@role_required('MANAGER', 'STOCK_CLERK')
def stock_in(request):
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=request.POST.get('product'))
            quantity = int(request.POST.get('quantity'))
            unit_cost = request.POST.get('unit_cost')
            
            if not unit_cost:
                raise ValueError("Unit cost is required")
                
            product.stock_quantity += quantity
            product.save()
            
            Purchase.objects.create(
                product=product,
                supplier=product.supplier,
                quantity=quantity,
                unit_price=Decimal(str(unit_cost)),
                total_amount=Decimal(str(unit_cost)) * Decimal(str(quantity)),
                received=True
            )
            messages.success(request, f'Successfully added {quantity} units to {product.name}')
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error processing stock in: {str(e)}')
    return redirect('inventory')

@login_required
@role_required('MANAGER', 'STOCK_CLERK')
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
@role_required('MANAGER', 'STOCK_CLERK')
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
@role_required('MANAGER', 'CASHIER', 'SALES_ASSOCIATE')
def lookup_customer(request):
    if request.method == 'GET':
        query = request.GET.get('query', '').strip()
        if query:
            # Split the query into words
            words = query.split()
            
            # Only proceed if we have at least 2 words (first name and last name)
            if len(words) >= 2:
                # Last word is the last name
                last_name = words[-1]
                # Everything before the last word is the first name
                first_name = ' '.join(words[:-1])
                
                # Only search for exact matches
                customers = Customer.objects.filter(
                    first_name__iexact=first_name,
                    last_name__iexact=last_name
                )[:5]
                
                results = []
                for customer in customers:
                    results.append({
                        'id': customer.id,
                        'name': customer.get_full_name(),
                        'email': customer.email,
                        'phone': customer.phone
                    })
                return JsonResponse({'results': results})
            
    return JsonResponse({'results': []})

@login_required
@role_required('MANAGER')
def delete_sale(request, pk):
    if request.method == 'POST':
        try:
            sale = get_object_or_404(Sale, pk=pk)
            sale.delete()
            return JsonResponse({'status': 'success', 'message': 'Sale deleted successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error deleting sale: {str(e)}'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

@login_required
@role_required('MANAGER', 'CASHIER', 'SALES_ASSOCIATE')
def sales(request):
    recent_sales = Sale.objects.select_related('customer').order_by('-sale_date')[:50]
    products = Product.objects.all().order_by('name')
    context = {
        'recent_sales': recent_sales,
        'products': products,
    }
    return render(request, 'store_ops/sales.html', context)

@login_required
@role_required('MANAGER', 'CASHIER', 'SALES_ASSOCIATE')
def process_sale(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.POST.get('items'))
            customer_id = request.POST.get('customer')
            payment_method = request.POST.get('payment_method')

            # Create sale
            sale = Sale.objects.create(
                customer_id=customer_id if customer_id else None,
                employee=request.user.employee,  # Set the logged-in employee
                payment_method=payment_method,
                total_amount=0  # Will be updated after adding items
            )

            total_amount = Decimal('0.00')
            # Process each item
            for item in data:
                product = Product.objects.get(id=item['product_id'])
                quantity = int(item['quantity'])
                
                # Check stock
                if product.stock_quantity < quantity:
                    sale.delete()
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Insufficient stock for {product.name}'
                    })
                
                # Calculate subtotal using Decimal
                subtotal = product.price * Decimal(str(quantity))
                
                # Create sale item
                SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity,
                    unit_price=product.price,
                    subtotal=subtotal
                )
                
                # Update stock
                product.stock_quantity -= quantity
                product.save()
                
                total_amount += subtotal
            
            # Update sale total
            sale.total_amount = total_amount
            sale.save()
            
            # Add loyalty points if customer exists
            if customer_id:
                customer = Customer.objects.get(id=customer_id)
                # Calculate points: 0.5 points per 100 pesos
                points_earned = int((total_amount / Decimal('100.00')) * Decimal('0.5'))
                if points_earned > 0:
                    customer.loyalty_points += points_earned
                    customer.save()
                    messages.success(request, f'Added {points_earned} loyalty points to {customer.get_full_name()}')
            
            messages.success(request, 'Sale processed successfully')
            return JsonResponse({
                'status': 'success',
                'sale_id': sale.id
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })

@login_required
@role_required('MANAGER', 'CASHIER', 'SALES_ASSOCIATE')
def sale_details(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    items = []
    for item in sale.items.select_related('product'):
        items.append({
            'product_name': item.product.name,
            'quantity': item.quantity,
            'unit_price': float(item.unit_price),
            'subtotal': float(item.subtotal)
        })
    
    data = {
        'id': sale.id,
        'date': sale.sale_date.strftime('%Y-%m-%d %H:%M:%S'),
        'customer': sale.customer.get_full_name() if sale.customer else 'Walk-in Customer',
        'customer_email': sale.customer.email if sale.customer else '',
        'customer_phone': sale.customer.phone if sale.customer else '',
        'employee': f"{sale.employee.user.first_name} {sale.employee.user.last_name}" if sale.employee else 'Unknown Employee',
        'employee_email': sale.employee.user.email if sale.employee else '',
        'employee_phone': sale.employee.phone if sale.employee else '',
        'payment_method': dict(Sale.PAYMENT_CHOICES).get(sale.payment_method),
        'total_amount': float(sale.total_amount),
        'items': items
    }
    return JsonResponse(data)

@login_required
@role_required('MANAGER', 'CASHIER', 'SALES_ASSOCIATE')
def get_product_details(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        data = {
            'supplier_name': product.supplier.name if product.supplier else '',
            'supplier_id': product.supplier.id if product.supplier else '',
            'price': str(product.price)  # Convert Decimal to string for JSON serialization
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

# Customer Views
@login_required
@role_required('MANAGER', 'CASHIER', 'SALES_ASSOCIATE')
def customer_list(request):
    customers = Customer.objects.all().order_by('first_name', 'last_name')
    return render(request, 'store_ops/customer_list.html', {'customers': customers})

@login_required
@role_required('MANAGER', 'CASHIER', 'SALES_ASSOCIATE')
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
@role_required('MANAGER', 'CASHIER', 'SALES_ASSOCIATE')
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
@role_required('MANAGER', 'CASHIER', 'SALES_ASSOCIATE')
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
@role_required('MANAGER', 'STOCK_CLERK')
def supplier_list(request):
    suppliers = Supplier.objects.all().order_by('name')
    return render(request, 'store_ops/supplier_list.html', {'suppliers': suppliers})

@login_required
@role_required('MANAGER')
def supplier_add(request):
    if request.method == 'POST':
        try:
            supplier = Supplier.objects.create(
                name=request.POST.get('name'),
                description=request.POST.get('description'),
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
@role_required('MANAGER')
def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        try:
            supplier.name = request.POST.get('name')
            supplier.description = request.POST.get('description')
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
@role_required('MANAGER')
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
@role_required('MANAGER')
def employee_list(request):
    employees = Employee.objects.select_related('user').all()
    return render(request, 'store_ops/employee_list.html', {'employees': employees})

@login_required
@role_required('MANAGER')
def employee_add(request):
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
                address=request.POST.get('address'),
                role=request.POST.get('role'),
                salary=request.POST.get('salary'),
                date_of_birth=request.POST.get('date_of_birth') or None,
                emergency_contact=request.POST.get('emergency_contact'),
                active=request.POST.get('active') == 'on'
            )
            messages.success(request, f'Employee {employee.user.get_full_name()} added successfully.')
        except Exception as e:
            if user:  # If user was created but employee creation failed
                user.delete()  # Clean up the user
            messages.error(request, f'Error adding employee: {str(e)}')
    return redirect('employee_list')

@login_required
@role_required('MANAGER')
def employee_edit(request, pk):
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
            employee.address = request.POST.get('address')
            employee.role = request.POST.get('role')
            employee.salary = request.POST.get('salary')
            employee.date_of_birth = request.POST.get('date_of_birth') or None
            employee.emergency_contact = request.POST.get('emergency_contact')
            employee.active = request.POST.get('active') == 'on'
            employee.save()
            
            messages.success(request, f'Employee {employee.user.get_full_name()} updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating employee: {str(e)}')
    return redirect('employee_list')

@login_required
@role_required('MANAGER')
def employee_delete(request, pk):
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
    context = {}
    
    if hasattr(request.user, 'employee'):
        employee = request.user.employee
        context['employee'] = employee
        
        # Calculate days employed
        days_employed = (timezone.now().date() - employee.hire_date).days
        context['days_employed'] = days_employed
        
        # Get sales statistics
        sales = Sale.objects.filter(employee=employee)
        context['total_sales'] = sales.count()
        context['total_revenue'] = sales.aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Get recent activities
        recent_activities = []
        
        # Add recent sales
        recent_sales = sales.order_by('-sale_date')[:5]
        for sale in recent_sales:
            recent_activities.append({
                'date': sale.sale_date,
                'description': f'Processed sale #{sale.id} for ${sale.total_amount}'
            })
        
        # Add recent logins
        if request.user.last_login:
            recent_activities.append({
                'date': request.user.last_login,
                'description': 'Logged into the system'
            })
        
        # Sort activities by date
        recent_activities.sort(key=lambda x: x['date'], reverse=True)
        context['recent_activities'] = recent_activities
        
    # Get user preferences
    preferences, created = UserPreferences.objects.get_or_create(user=request.user)
    context['preferences'] = preferences
    
    return render(request, 'store_ops/profile.html', context)

@login_required
def save_preferences(request):
    if request.method == 'POST':
        preferences, created = UserPreferences.objects.get_or_create(user=request.user)
        preferences.theme = request.POST.get('theme', 'light')
        preferences.time_format = request.POST.get('time_format', '24')
        preferences.date_format = request.POST.get('date_format', 'mdy')
        preferences.email_notifications = request.POST.get('email_notifications') == 'on'
        preferences.save()
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def register(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = AdminRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    return render(request, 'registration/logged_out.html')

# Purchase Order Views
@login_required
@role_required('MANAGER', 'STOCK_CLERK')
def purchase_orders(request):
    purchase_orders = Purchase.objects.all().order_by('-purchase_date')
    form = PurchaseOrderForm()
    
    context = {
        'purchase_orders': purchase_orders,
        'form': form,
    }
    return render(request, 'store_ops/purchase_orders.html', context)

@login_required
@role_required('MANAGER', 'STOCK_CLERK')
def create_purchase(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            purchase_order = form.save(commit=False)
            purchase_order.total_amount = purchase_order.quantity * purchase_order.unit_price
            purchase_order.save()
            messages.success(request, 'Purchase order created successfully')
        else:
            messages.error(request, 'Error creating purchase order')
    return redirect('purchase_orders')

@login_required
@role_required('MANAGER', 'STOCK_CLERK')
def receive_purchase(request, pk):
    if request.method == 'POST':
        try:
            purchase = Purchase.objects.get(id=pk)
            if not purchase.received:
                # Update product stock
                product = purchase.product
                product.stock_quantity += purchase.quantity
                product.save()
                
                # Mark purchase as received
                purchase.received = True
                purchase.received_date = timezone.now()
                purchase.save()
                
                messages.success(request, f'Purchase order #{purchase.id} marked as received')
            else:
                messages.error(request, 'Purchase order already received')
        except Purchase.DoesNotExist:
            messages.error(request, 'Purchase order not found')
    return redirect('purchase_orders')

@login_required
@role_required('MANAGER')
def delete_purchase(request, pk):
    if request.method == 'POST':
        try:
            purchase = Purchase.objects.get(id=pk)
            purchase.delete()
            messages.success(request, 'Purchase order deleted successfully')
        except Purchase.DoesNotExist:
            messages.error(request, 'Purchase order not found')
    return redirect('purchase_orders')

@login_required
@role_required('MANAGER', 'STOCK_CLERK')
def cancel_purchase(request, pk):
    if request.method == 'POST':
        try:
            purchase = Purchase.objects.get(id=pk)
            if not purchase.received and not purchase.cancelled:
                purchase.cancelled = True
                purchase.cancelled_date = timezone.now()
                purchase.save()
                messages.success(request, f'Purchase order #{purchase.id} cancelled successfully')
            else:
                messages.error(request, 'Cannot cancel received or already cancelled order')
        except Purchase.DoesNotExist:
            messages.error(request, 'Purchase order not found')
    return redirect('purchase_orders')
