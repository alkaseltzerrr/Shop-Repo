from django.urls import path
from . import views
from apps.em.views import owner_login

urlpatterns = [
    path('', owner_login    , name='login'),# Root URL for the homepage
    path('home/', views.home, name='home'),# once logged in it goes here

    path('crud/',views.crud, name='crud'),
]
