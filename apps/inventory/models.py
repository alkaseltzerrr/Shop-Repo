
from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

# Category Model
class Category(models.Model):
    categoryID = models.AutoField(primary_key=True)  # Auto-incrementing ID
    categoryName = models.CharField(max_length=255)  # VARCHAR for category name

    def __str__(self):
        return self.categoryName

# Product Model
class Product(models.Model):
    productID = models.AutoField(primary_key=True)  # Auto-incrementing ID
    productName = models.CharField(max_length=255)  # VARCHAR for product name
    description = models.TextField(blank=True, null=True)  # TEXT for description
    price = models.FloatField()  # FLOAT for price
    expireyDate = models.DateField()  # Date field for expiry date
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)  # Foreign key to Category

    def __str__(self):
        return self.productName

# Inventory Model
class Inventory(models.Model):
    inventoryID = models.AutoField(primary_key=True)  # Auto-incrementing ID
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)  # Foreign key to Product
    quantity = models.IntegerField()  # Change to IntegerField for quantity
    lastUpdate = models.DateField(default=timezone.now)  # Date for last update, with default to current date

    def __str__(self):
        return f"{self.productID.productName} - Inventory {self.quantity}"
