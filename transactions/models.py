from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.functional import cached_property
from django.db.models import Sum,Count
from django.utils import timezone
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import calendar


class TransactionManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('lender')




period =(

('1month','1month'),
('2months','2months'),
('3months','3months'),
)

CHOICES = (
        ('mon', 'mon'),
        ('tue', 'tue'),
        ('wed', 'wed'),
        ('thur', 'thur'),
        ('fri', 'fri'),
        ('sat', 'sat'),
        ('sun', 'sun'),
    )


class Transaction(models.Model):
    clients_loan_repayment = models.IntegerField(default=0)
    repayment_day=models.CharField(max_length=200,choices=CHOICES,default="")
    lending_date=models.DateTimeField(default=timezone.now)
    clients_name=models.CharField(max_length=200)
    clients_id=models.CharField(max_length=200)
    clients_location=models.CharField(max_length=200,default="")
    mpesa_bank_ref=models.CharField(max_length=200,default="",blank=True)
    clients_phone=models.CharField(max_length=20)
    loan_amount=models.IntegerField(default=0)
    interest_charged = models.FloatField(default=0.0)
    repayment_period = models.CharField(choices=period,max_length=100)
    office_expenses = models.IntegerField(default=0)
    salary_expenses = models.IntegerField(default=0)
    bad_debts = models.IntegerField(default=0)
    lender=models.ForeignKey(User,on_delete=models.CASCADE)
    objects = TransactionManager()


    

    def __str__(self):
        return self.clients_name

    def get_absolute_url(self):
        return reverse("repayments")    

    @cached_property
    def the_date_today(self):
       return self.lending_date.now  

    
    @cached_property
    def total_borrowed_amount(self):
        result = Transaction.objects.aggregate(total=Sum('loan_amount'))
        return result['total']
    
    @cached_property
    def total_interest(self):
        result = Transaction.objects.aggregate(total=Sum('interest_charged'))
        return result['total']

    @cached_property
    def total_repayed_amount(self):
        result = Transaction.objects.aggregate(total=Sum('clients_loan_repayment'))
        return result['total']
    @cached_property
    def operating_cash(self):
        method1 = self.total_repayed_amount
        method2 = self.total_borrowed_amount
        return method1 - method2
    
    @cached_property
    def total_clients(self):
        result = Transaction.objects.aggregate(total=Count('clients_name'))
        return result['total']
    
    @cached_property
    def interest_due(self):
        method1 = self.loan_amount
        method2 = self.interest_charged
        return method1 * method2
    
    @cached_property
    def due_date(self):
        date = self.lending_date
        if self.repayment_period == '1month':
           due = date + relativedelta(months=+1)
           return due
        elif self.repayment_period == '2months':
           due = date + relativedelta(months=+2)
           return due
        else:
           due = date + relativedelta(months=+3)
           return due   

    @cached_property
    def due_amount(self):
        method1 = self.interest_due
        method2 = self.loan_amount
        return method1 + method2

    @cached_property
    def balance_due(self):
        method1 = self.due_amount
        method2 = self.clients_loan_repayment
        return abs(method2 - method1)                

    @cached_property
    def loans_payable(self):
        method1 = self.total_borrowed_amount
        method2 = self.interest_charged
        total = method1 * method2
        return method1 + total

    @cached_property
    def unrealized_interest(self):
        method1 = self.loans_payable
        method2 = self.total_borrowed_amount
        return method1 - method2
    
    @cached_property
    def total_bad_debts(self):
        result = Transaction.objects.aggregate(total=Sum('bad_debts'))
        return result['total']

    @cached_property
    def salary(self):
        result = Transaction.objects.aggregate(total=Sum('salary_expenses'))
        return result['total']    
    
    @cached_property
    def office_expense(self):
        result = Transaction.objects.aggregate(total=Sum('office_expenses'))
        return result['total']    


    @cached_property
    def realized_interest(self):
        method1 = self.total_repayed_amount
        method2 = self.total_bad_debts
        return method1 - method2
    
    @cached_property
    def income(self):
        method1 = self.realized_interest
        method2 = self.office_expense
        method3 = self.salary
        income = method1 - (method2+method3)
        if income > 0:
            return 'A profit of ' + str(income)
        elif income < 0:
            return 'A loss of ' + str(income)
        elif income == 0:
            return 'A breakeven of ' + str(income)       
   
