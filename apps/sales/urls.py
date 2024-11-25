from django.urls import path
from . import views
from .views import customer_product_create, sale_transaction_history

urlpatterns = [
    # Sale URLs
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/new/', views.sale_create, name='sale_create'),
    path('sales/<int:pk>/edit/', views.sale_update, name='sale_update'),
    path('sales/<int:pk>/delete/', views.sale_delete, name='sale_delete'),

    # SaleDetail URLs
    path('sales/<int:sale_id>/details/', views.sale_detail_list, name='sale_detail_list'),
    path('sales/<int:sale_id>/details/new/', views.sale_detail_create, name='sale_detail_create'),
    path('details/<int:pk>/edit/', views.sale_detail_update, name='sale_detail_update'),
    path('details/<int:pk>/delete/', views.sale_detail_delete, name='sale_detail_delete'),

    #transactions
    path('customer_product_form/', customer_product_create, name='customer_product_form'),
    path('sale_transaction_history/', sale_transaction_history, name='sale_transaction_history'),
]