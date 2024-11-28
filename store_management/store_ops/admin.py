from django.contrib import admin
from .models import (
    Category, Product, Supplier, Employee,
    Customer, Purchase, Sale, SaleItem
)

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'supplier', 'price', 'stock_quantity')
    list_filter = ('category', 'supplier')
    search_fields = ('name', 'sku')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'contact_person', 'email')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'hire_date', 'active')
    list_filter = ('role', 'active')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'loyalty_points')
    search_fields = ('first_name', 'last_name', 'email', 'phone')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'product', 'quantity', 'total_amount', 'purchase_date', 'received')
    list_filter = ('received', 'purchase_date')
    search_fields = ('supplier__name', 'product__name')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'payment_method', 'sale_date')
    list_filter = ('payment_method', 'sale_date')
    search_fields = ('customer__first_name', 'customer__last_name')

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'quantity', 'unit_price', 'subtotal')
    search_fields = ('sale__id', 'product__name')
