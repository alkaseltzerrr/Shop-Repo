from django.urls import path
from . import views

urlpatterns = [


    path('owners/', views.owner_list, name='owner_list'),
    path('owners/create/', views.owner_create, name='owner_create'),
    path('owners/<int:pk>/edit/', views.owner_update, name='owner_update'),
    path('owners/<int:pk>/delete/', views.owner_delete, name='owner_delete'),

    path('stores/', views.store_list, name='store_list'),
    path('stores/create/', views.store_create, name='store_create'),
    path('stores/<int:pk>/edit/', views.store_update, name='store_update'),
    path('stores/<int:pk>/delete/', views.store_delete, name='store_delete'),

    path('employees/', views.employee_list, name='employee_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/<int:pk>/edit/', views.employee_update, name='employee_update'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),

    path('login/', views.owner_login, name='login'),

    path('register/', views.owner_register, name='RegisterOwner'),
]

