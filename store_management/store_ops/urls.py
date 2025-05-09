from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('verify-password/', views.verify_current_password, name='verify_current_password'),
    path('save-preferences/', views.save_preferences, name='save_preferences'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/stock-in/', views.stock_in, name='stock_in'),
    path('inventory/stock-out/', views.stock_out, name='stock_out'),
    path('inventory/<int:pk>/adjust/', views.adjust_stock, name='adjust_stock'),
    
    path('sales/', views.sales, name='sales'),
    path('sales/process/', views.process_sale, name='process_sale'),
    path('sales/<int:pk>/details/', views.sale_details, name='sale_details'),
    path('sales/<int:pk>/delete/', views.delete_sale, name='delete_sale'),
    path('lookup_customer/', views.lookup_customer, name='lookup_customer'),
    
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_add, name='customer_add'),
    path('customers/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.supplier_add, name='supplier_add'),
    path('suppliers/<int:pk>/edit/', views.supplier_edit, name='supplier_edit'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),
    
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('employees/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    
    path('api/product/<int:product_id>/details/', views.get_product_details, name='get_product_details'),
    
    # Purchase Order URLs
    path('purchase-orders/', views.purchase_orders, name='purchase_orders'),
    path('purchase-orders/create/', views.create_purchase, name='create_purchase'),
    path('purchase-orders/<int:pk>/receive/', views.receive_purchase, name='receive_purchase'),
    path('purchase-orders/<int:pk>/delete/', views.delete_purchase, name='delete_purchase'),
    path('purchase-orders/<int:pk>/cancel/', views.cancel_purchase, name='cancel_purchase'),
    
    path('register/', views.register, name='register'),
    path('logout/', views.custom_logout, name='logout'),
]
