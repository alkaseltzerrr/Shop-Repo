from django.urls import path
from . import views

urlpatterns = [
    # Sale URLs
    path('sales/', views.sale_list, name='sale_list'),                 # List all sales
    path('sales/new/', views.sale_create, name='sale_create'),         # Create a new sale
    path('sales/<int:pk>/edit/', views.sale_update, name='sale_update'),# Update a sale
    path('sales/<int:pk>/delete/', views.sale_delete, name='sale_delete'), # Delete a sale

    # SaleDetail URLs
    path('sales/<int:sale_id>/details/', views.sale_detail_list, name='sale_detail_list'), # List sale details
    path('sales/<int:sale_id>/details/new/', views.sale_detail_create, name='sale_detail_create'), # Create sale detail
    path('details/<int:pk>/edit/', views.sale_detail_update, name='sale_detail_update'), # Update sale detail
    path('details/<int:pk>/delete/', views.sale_detail_delete, name='sale_detail_delete'), # Delete sale detail
]
