from django.db import models
from apps.em.models import Owner, Employee
from apps.crm.models import Customer
from apps.inventory.models import Product

class Sale(models.Model):
    SaleID = models.AutoField(primary_key=True)
    SaleDate = models.DateField()
    Employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name='sales', null=False,blank=False)
    CustomerID = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, default=1)
    #Customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='purchases',null=False,blank=False)
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Sale {self.SaleID} - {self.SaleDate} - ${self.TotalAmount}"

class SaleDetail(models.Model):
    SaleDetailID = models.AutoField(primary_key=True)
    SaleID = models.ForeignKey(Sale, models.DO_NOTHING, related_name='details')
    ProductID = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='product', null=False, blank=False)
    Quantity = models.IntegerField()
    UnitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    PaymentType = models.CharField(max_length=50)

    def __str__(self):
        return f"SaleDetail {self.SaleDetailID} - Sale {self.SaleID_id} - {self.Quantity} items"