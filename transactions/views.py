
from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin,UserPassesTestMixin
from .models import Transaction
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse




# ======================TRANSACTIONS=======================================


class TransactionHomeView(ListView):
    model = Transaction
    template_name = 'transactions/transactionshome.html'
    context_object_name = 'transactions'
    transactions = Transaction.objects.all()
    
    # def get_queryset(self):
        # enlister = self.request.user
        # queryset = Transaction.objects.filter(enlister=enlister)
        # return queryset
class AdminHomeView(LoginRequiredMixin,ListView):
    model = Transaction
    template_name = 'transactions/admin.html'
    context_object_name = 'transactions'
    transactions = Transaction.objects.all()

class AdminUserView(LoginRequiredMixin,ListView):
    model = User
    template_name = 'transactions/admin.html'
    context_object_name = 'users'
    paginate_by = 30
         

class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = 'transactions/transactionshome.html'
    fields = [
    'clients_loan_repayment',
    'clients_name',
    'clients_id',
    'clients_phone',
    'loan_amount',
    'interest_charged',
    'repayment_period',

 ]
 
    def form_valid(self, form):
        form.instance.lender = self.request.user
        return super().form_valid(form)
   
class TransactionUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Transaction
    template_name = 'transactions/transactionshome.html'
    fields = [
    'clients_loan_repayment',
    'clients_name',
    'clients_id',
    'clients_phone',
    'loan_amount',
    'interest_charged',
    'repayment_period',
    ]

    def form_valid(self, form):
        form.instance.lender = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        transaction=self.get_object()
        
        if self.request.user==transaction.lender\
            or self.request.user.username == 'root'\
            or self.request.user.username == 'admin':
            return True
        else:
            return False    


class TransactionDeleteView(LoginRequiredMixin,UserPassesTestMixin,  DeleteView,):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    context_object_name = 'transaction'
    success_url = reverse_lazy('reports_home')
    
    def test_func(self):
        transaction=self.get_object()
        
        if self.request.user==transaction.lender\
            or self.request.user.username == 'root'\
            or self.request.user.username == 'admin':
            return True
        else:
            return False    
    



class ResultView(LoginRequiredMixin,ListView):
    model = Transaction
    context_object_name = 'transaction'
    template_name = 'transactions/reports.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Transaction.objects.filter(
            Q(clients_name__icontains=query) | Q(clients_phone__icontains=query) | Q(clients_id__icontains=query))
        return object_list


class ReportHome(LoginRequiredMixin,ListView):
    model = Transaction
    reports = Transaction.objects.all()
    template_name = 'transactions/disbursements.html'
    context_object_name = 'reports'
    paginate_by=50
    ordering = ['-lending_date']
    
    
    
   
    

