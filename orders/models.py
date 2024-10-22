from django.db import models

# Create your models here.

class order(models.Model):
    OrderID = models.AutoField(primary_key=True)
    OrderDate = models.DateField()
    #SupplierID = models.ForeignKey('Supplier', models.DO_NOTHING)
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.OrderID} - {self.OrderDate} - ${self.TotalAmount}"

class orderDetail(models.Model):
    OrderDetailID = models.AutoField(primary_key=True)
    OrderID = models.ForeignKey(order, models.DO_NOTHING, related_name='details')
    #ProductID = models.ForeignKey('Product', models.DO_NOTHING)
    Quantity = models.IntegerField()
    UnitPrice = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderDetail {self.OrderDetailID} - Order {self.OrderID_id} - {self.Quantity} items - ${self.UnitPrice} each"