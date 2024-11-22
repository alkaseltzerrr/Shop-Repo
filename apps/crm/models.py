from django.db import models

class Customer(models.Model):
    customerid = models.AutoField(primary_key=True)
    customername = models.CharField(max_length=100)
    contactinformation = models.TextField()
    loyaltypoints = models.DecimalField(max_digits=10, decimal_places=2)
    Address = models.CharField(max_length=255)

    def __str__(self):
        return self.customername


class LoyaltyProgram(models.Model):
    loyaltyprogramid = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loyaltytype = models.CharField(max_length=50)
    pointsaccumulated = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.loyaltytype} for {self.customer.customername}"
