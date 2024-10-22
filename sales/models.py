from django.db import models

class Sale(models.Model):
    SaleID = models.AutoField(primary_key=True)
    SaleDate = models.DateField()
    # Foreign keys to Employee and Customer can be re-added once those models are defined
    # EmployeeID = models.ForeignKey('Employee', models.DO_NOTHING)
    # CustomerID = models.ForeignKey('Customer', models.DO_NOTHING)
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        # Return a more meaningful string, such as the sale date and total amount
        return f"Sale {self.SaleID} - {self.SaleDate} - ${self.TotalAmount}"

class SaleDetail(models.Model):
    SaleDetailID = models.AutoField(primary_key=True)
    SaleID = models.ForeignKey(Sale, models.DO_NOTHING, related_name='details')
    # Foreign key to Product (to be defined later)
    # ProductID = models.ForeignKey('Product', models.DO_NOTHING)
    Quantity = models.IntegerField()
    UnitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    PaymentType = models.CharField(max_length=50)

    def __str__(self):
        # Display SaleDetail with associated Sale and key details
        return f"SaleDetail {self.SaleDetailID} - Sale {self.SaleID_id} - {self.Quantity} items"
