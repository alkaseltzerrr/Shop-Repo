from django.contrib import admin
from .models import Customer, LoyaltyProgram

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customername', 'contactinformation', 'loyaltypoints')
    search_fields = ('customername',)

@admin.register(LoyaltyProgram)
class LoyaltyProgramAdmin(admin.ModelAdmin):
    list_display = ('loyaltytype', 'pointsaccumulated', 'customer')
    search_fields = ('loyaltytype',)
