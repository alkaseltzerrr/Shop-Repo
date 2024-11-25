from django.urls import path
from . import views
from .views import supplier_product_create, order_transaction_history

urlpatterns = [
    path('', views.supplier_list, name='supplier_list'),
    path('create/', views.supplier_create, name='supplier_create'),
    path('update/<int:pk>/', views.supplier_update, name='supplier_update'),
    path('delete/<int:pk>/', views.supplier_delete, name='supplier_delete'),

    #transaction URLS
    #buy features
    path('supplier_product_form/', supplier_product_create, name='supplier_product_form'),
    path('order_transaction_history/', order_transaction_history, name='order_transaction_history'),

]
