# orders/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Order URLs
    path('orders/', views.order_list, name='order_list'),
    path('orders/new/', views.order_create, name='order_create'),
    path('orders/<int:pk>/edit/', views.order_update, name='order_update'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),

    # OrderDetail URLs
    path('orders/<int:order_id>/orderdetails/', views.order_detail_list, name='order_detail_list'),
    path('orders/<int:order_id>/orderdetails/new/', views.order_detail_create, name='order_detail_create'),
    path('orderdetails/<int:pk>/edit/', views.order_detail_update, name='order_detail_update'),
    path('orderdetails/<int:pk>/delete/', views.order_detail_delete, name='order_detail_delete'),
]