from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Customer, LoyaltyProgram

# CRUD for Customer
class CustomerListView(ListView):
    model = Customer
    template_name = 'customer_list.html'
    context_object_name = 'customers'

class CustomerCreateView(CreateView):
    model = Customer
    template_name = 'customer_form.html'
    fields = ['customername', 'contactinformation', 'loyaltypoints']
    success_url = reverse_lazy('customer_list')

class CustomerUpdateView(UpdateView):
    model = Customer
    template_name = 'customer_form.html'
    fields = ['customername', 'contactinformation', 'loyaltypoints']
    success_url = reverse_lazy('customer_list')

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')

# CRUD for LoyaltyProgram
class LoyaltyProgramListView(ListView):
    model = LoyaltyProgram
    template_name = 'lp_list.html'
    context_object_name = 'loyaltyprograms'

class LoyaltyProgramCreateView(CreateView):
    model = LoyaltyProgram
    template_name = 'loyaltyprogram_form.html'
    fields = ['customer', 'loyaltytype', 'pointsaccumulated']
    success_url = reverse_lazy('lp_list')

class LoyaltyProgramUpdateView(UpdateView):
    model = LoyaltyProgram
    template_name = 'loyaltyprogram_form.html'
    fields = ['customer', 'loyaltytype', 'pointsaccumulated']
    success_url = reverse_lazy('lp_list')

class LoyaltyProgramDeleteView(DeleteView):
    model = LoyaltyProgram
    template_name = 'loyaltyprogram_confirm_delete.html'
    success_url = reverse_lazy('lp_list')
