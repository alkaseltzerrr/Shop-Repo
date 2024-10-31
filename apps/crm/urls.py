from django.urls import path
from .views import (
    CustomerListView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView,
    LoyaltyProgramListView, LoyaltyProgramCreateView, LoyaltyProgramUpdateView, LoyaltyProgramDeleteView
)

urlpatterns = [
    # Customer URLs
    path('customers/', CustomerListView.as_view(), name='customer_list'),
    path('customers/create/', CustomerCreateView.as_view(), name='customer_create'),
    path('customers/update/<int:pk>/', CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/delete/<int:pk>/', CustomerDeleteView.as_view(), name='customer_delete'),

    # LoyaltyProgram URLs
    path('loyaltyprograms/', LoyaltyProgramListView.as_view(), name='lp_list'),
    path('loyaltyprograms/create/', LoyaltyProgramCreateView.as_view(), name='loyaltyprogram_create'),
    path('loyaltyprograms/update/<int:pk>/', LoyaltyProgramUpdateView.as_view(), name='loyaltyprogram_update'),
    path('loyaltyprograms/delete/<int:pk>/', LoyaltyProgramDeleteView.as_view(), name='loyaltyprogram_delete'),
]
