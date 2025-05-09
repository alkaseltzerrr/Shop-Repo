from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True, help_text="Description of who the supplier is and what they supply")
    contact_person = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    stock_quantity = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"

class Employee(models.Model):
    ROLE_CHOICES = [
        ('MANAGER', 'Manager'),
        ('CASHIER', 'Cashier'),
        ('STOCK_CLERK', 'Stock Clerk'),
        ('SALES_ASSOCIATE', 'Sales Associate'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(null=True)
    hire_date = models.DateField(auto_now_add=True)  
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    date_of_birth = models.DateField(null=True, blank=True)  
    emergency_contact = models.CharField(max_length=100, null=True, blank=True)  

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role}"

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(null=True)
    loyalty_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
    received = models.BooleanField(default=False)
    received_date = models.DateTimeField(null=True, blank=True)
    cancelled = models.BooleanField(default=False)
    cancelled_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Purchase {self.id} - {self.product.name}"

class Sale(models.Model):
    PAYMENT_CHOICES = [
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('MOBILE', 'GCash Payment'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='sales', null=True, blank=True)
    sale_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    original_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Total amount before loyalty points discount")
    points_used = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Amount of loyalty points used for discount")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='CASH')
    
    def __str__(self):
        return f"Sale {self.id} - {self.sale_date.strftime('%Y-%m-%d %H:%M')}"

    @property
    def points_discount(self):
        """Returns the discount amount from loyalty points"""
        if self.original_amount is None:
            return Decimal('0.00')
        return self.original_amount - self.total_amount

    def save(self, *args, **kwargs):
        # Set original_amount to total_amount if not set
        if self.original_amount is None:
            self.original_amount = self.total_amount
        super().save(*args, **kwargs)

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    theme = models.CharField(max_length=10, choices=[
        ('light', 'Light Mode'),
        ('dark', 'Dark Mode'),
        ('auto', 'System Default')
    ], default='light')
    time_format = models.CharField(max_length=2, choices=[
        ('24', '24-hour'),
        ('12', '12-hour')
    ], default='24')
    date_format = models.CharField(max_length=3, choices=[
        ('mdy', 'MM/DD/YYYY'),
        ('dmy', 'DD/MM/YYYY'),
        ('ymd', 'YYYY/MM/DD')
    ], default='mdy')
    email_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s preferences"
