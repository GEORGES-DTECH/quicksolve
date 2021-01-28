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

MODE =(

('cash','cash'),
('mpesa','mpesa'),
('bank','bank'),
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
    repayment_day=models.CharField(max_length=200,choices=CHOICES,default="",blank=True)
    lending_date=models.DateTimeField(default=timezone.now)
    clients_name=models.CharField(max_length=200,blank=True)
    clients_id=models.CharField(max_length=200,blank=True)
    clients_location=models.CharField(max_length=200,default="",blank=True)
    mpesa_bank_ref=models.CharField(max_length=200,default="",blank=True)
    clients_phone=models.CharField(max_length=20,blank=True)
    loan_amount=models.IntegerField(default=0)
    interest_charged = models.FloatField(default=0.0)
    repayment_period = models.CharField(choices=period,max_length=100,blank=True)
    office_expenses = models.IntegerField(default=0)
    salary_expenses = models.IntegerField(default=0)
    expense_description = models.CharField(max_length=100,default="",blank=True)
    bad_debts = models.IntegerField(default=0)
    mode_of_payment = models.CharField(choices=MODE,max_length=100,default="",blank=True)
    lender=models.ForeignKey(User,on_delete=models.CASCADE)
    objects = TransactionManager()


    

    def __str__(self):
        return self.clients_name

    def get_absolute_url(self):
        return reverse("transaction_home")    

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
    #=====================expenses total================================== 
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
    # ===================expenses conditions=============================
    @cached_property
    def office_expense_condition(self):
        if self.office_expenses > 0:
            return self.office_expenses

    @cached_property
    def salary_expense_condition(self):
        if self.salary_expenses > 0:
            return self.salary_expenses

    @cached_property
    def debts_expense_condition(self):
        if self.bad_debts > 0:
            return self.bad_debts

#  ================disbursemnts condition=====================
    @cached_property
    def loan_condition(self):
        if self.loan_amount > 0:
            return self.loan_amount
    
# ===========================repayments condition==================
    
    @cached_property
    def repayment_condition(self):
        method=self.due_amount
        if method > 0:
            return method
    


    
# ==========================income calculation========================
    @cached_property
    def realized_interest(self):
        method1 = self.unrealized_interest
        method2 = self.total_bad_debts
        return method1 - method2
    
    @cached_property
    def operating_cash(self):
        method1 = self.total_repayed_amount
        method2 = self.total_borrowed_amount
        method3 = self.total_bad_debts
        method4 = self.salary
        method5 = self.office_expense
        return method1 - (method2 + method3 +method4 +method5)

    @cached_property
    def income(self):
        method1 = self.realized_interest
        method2 = self.office_expense
        method3 = self.salary
        income = method1 - (method2+method3)
        if income > 0:
            return 'A profit of ' + str(income)
        elif income < 0:
            return 'A loss of ' + str(abs(income))
        elif income == 0:
            return 'A breakeven of ' + str(income)       

CHOICES=(
    ('Jan','Jan'),
    ('Feb','Feb'),
    ('Mar','Mar'),
    ('Apr','Apr'),
    ('May','May'),
    ('June','June'),
    ('July','July'),
    ('Aug','Aug'),
    ('Sep','Sep'),
    ('Oct','Oct'),
    ('Nov','Nov'),
    ('Dec','Dec'),      
)


class Report(models.Model):
    month=models.CharField(max_length=200,choices=CHOICES)
    total_payable_loans=models.IntegerField(default=0)
    total_loans_given=models.IntegerField(default=0)
    loan_repayments=models.IntegerField(default=0)
    unrealized_interest_income=models.IntegerField(default=0)
    bad_debts=models.IntegerField(default=0)
    realized_interest_income=models.IntegerField(default=0)
    office_expenses=models.IntegerField(default=0)
    salary_expenses=models.IntegerField(default=0)
    author = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,default="")
    
    
    def __str__(self):
        return self.month

    def get_absolute_url(self):
        return reverse('report')    