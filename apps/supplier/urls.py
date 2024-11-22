from django.urls import path
from . import views
from .views import supplier_product_create

urlpatterns = [
    path('', views.supplier_list, name='supplier_list'),
    path('create/', views.supplier_create, name='supplier_create'),
    path('update/<int:pk>/', views.supplier_update, name='supplier_update'),
    path('delete/<int:pk>/', views.supplier_delete, name='supplier_delete'),

    path('supplier_product_form/', supplier_product_create, name='supplier_product_form'),



    path('buy/', views.buy_view, name='buy'),

]
