from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Owner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50)
    contact_information = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    email_id = models.CharField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.full_name

    def to_dict(self):
        return {
            'owner_id': self.owner_id,
            'full_name': self.full_name,
            'contact_information': self.contact_information,
            'email_id': self.email_id,
        }


class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=50)
    store_address = models.CharField(max_length=50)
    contact_information = models.CharField(max_length=50)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return self.store_name


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    store_id = models.ForeignKey(Store, on_delete=models.DO_NOTHING, related_name='employees',null=False,blank=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
