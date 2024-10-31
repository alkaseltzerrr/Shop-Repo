from django.db import models

# Create your models here.
from django.db import models

class Supplier(models.Model):
    SupplierID = models.AutoField(primary_key=True)
    SupplierName = models.CharField(max_length=50)
    ContactInformation = models.CharField(max_length=50)
    Address = models.CharField(max_length=50)

    def __str__(self):
        return self.SupplierName
