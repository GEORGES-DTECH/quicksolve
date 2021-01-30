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
    first_installment = models.IntegerField(default=0)
    second_installment = models.IntegerField(default=0)
    third_installment =models.IntegerField(default=0)
    fourth_installment = models.IntegerField(default=0)
    fifth_installment = models.IntegerField(default=0)
    sixth_installment =models.IntegerField(default=0)
    seventh_installment = models.IntegerField(default=0)
    eighth_installment =models.IntegerField(default=0)
    loan_payable =models.IntegerField(default=0)
    installment_description=models.CharField(max_length=1000,default="",blank=True)
    repayment_day=models.CharField(max_length=200,choices=CHOICES,default="",blank=True)
    lending_date=models.DateTimeField(default=timezone.now)
    clients_name=models.CharField(max_length=200,blank=True)
    clients_id=models.CharField(max_length=200,blank=True)
    clients_location=models.CharField(max_length=200,default="",blank=True)
    clients_phone=models.CharField(max_length=20,blank=True)
    loan_amount=models.IntegerField(default=0)
    interest_charged =models.FloatField(default=0.0)
    repayment_period = models.CharField(choices=period,max_length=100,blank=True)
    office_expenses = models.IntegerField(default=0)
    salary_expenses = models.IntegerField(default=0)
    expense_description = models.CharField(max_length=100,default="",blank=True)
    bad_debts =models.IntegerField(default=0)
    mode_of_payment = models.CharField(choices=MODE,max_length=100,default="",blank=True)
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
    def first_ins(self):
        result = Transaction.objects.aggregate(total=Sum('first_installment'))
        return result['total']
    
    @cached_property
    def second_ins(self):
        result = Transaction.objects.aggregate(total=Sum('second_installment'))
        return result['total']
    
    @cached_property
    def third_ins(self):
        result = Transaction.objects.aggregate(total=Sum('third_installment'))
        return result['total']
    
    @cached_property
    def fourth_ins(self):
        result = Transaction.objects.aggregate(total=Sum('fourth_installment'))
        return result['total']
    
    @cached_property
    def fifth_ins(self):
        result = Transaction.objects.aggregate(total=Sum('fifth_installment'))
        return result['total']
    
    @cached_property
    def sixth_ins(self):
        result = Transaction.objects.aggregate(total=Sum('sixth_installment'))
        return result['total']
    
    @cached_property
    def seventh_ins(self):
        result = Transaction.objects.aggregate(total=Sum('seventh_installment'))
        return result['total']
    
    @cached_property
    def eighth_ins(self):
        result = Transaction.objects.aggregate(total=Sum('eighth_installment'))
        return result['total']
    
    
    @cached_property
    def total_repayed_amount(self):
      method1=self.first_ins
      method2=self.second_ins
      method3=self.third_ins
      method4=self.fourth_ins
      method5=self.fifth_ins
      method6=self.sixth_ins
      method7=self.seventh_ins
      method8=self.eighth_ins
      total=method1+method2+method3+method4+method5+method6+method7+method8
      return total     
    
    
    @cached_property
    def total_clients(self):
        result = Transaction.objects.aggregate(total=Count('clients_name'))
        return result['total']
    

    @cached_property
    def date_check(self):
      method1=self.first_installment
      method2=self.second_installment
      method3=self.third_installment
      method4=self.fourth_installment
      method5=self.fifth_installment
      method6=self.sixth_installment
      method7=self.seventh_installment
      method8=self.eighth_installment
      check = method1 or method2 or method3 or method4 or method5 or method6 or method7 or method8
      if check > 0 :
          return self.lending_date
      else:
          return "" 
   
    

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
    def due_day(self):
        date = self.lending_date
        if self.repayment_period == '1month':
           due = date + relativedelta(months=+1)
           return calendar.day_name[due.weekday()]
        elif self.repayment_period == '2months':
           due = date + relativedelta(months=+2)
           return calendar.day_name[due.weekday()]
        else:
           due = date + relativedelta(months=+3)
           return calendar.day_name[due.weekday()]       

    @cached_property
    def due_amount(self):
        method1 = self.interest_due
        method2 = self.loan_amount
        return method1 + method2

    @cached_property
    def balance_due(self):
        method1 = self.due_amount
        method2 = self.first_installment
        method3 = self.second_installment
        method4 = self.third_installment
        method5 = self.fourth_installment
        method6 = self.fifth_installment
        method7 = self.sixth_installment
        method8 = self.seventh_installment
        method9 = self.eighth_installment
        return abs(method2 + method3 +method4+method5+method6+method7+method8+method9-method1)                
    
    @cached_property
    def loan_status(self):
        method=self.balance_due
        if method == 0.0:
            return "cleared"
        else:
            return "pending"    
    
   
   
    @cached_property
    def total_loans_payable(self):
        result = Transaction.objects.aggregate(total=Sum('loan_payable'))
        return result['total']
    
       
        


    @cached_property
    def unrealized_interest(self):
        method1 = self.total_loans_payable
        method2 = self.total_borrowed_amount
        return method1- method2
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

class ReportManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('author')




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
    income=models.IntegerField(default=0)
    objects=ReportManager()
    
    
    def __str__(self):
        return self.month

    def get_absolute_url(self):
        return reverse('report')    

    @cached_property
    def loans_given(self):
        result=Report.objects.aggregate(total=Sum('total_loans_given'))
        return result['total']
    
    @cached_property
    def loans_payable(self):
        result=Report.objects.aggregate(total=Sum('total_payable_loans'))
        return result['total']
    
    @cached_property
    def repayments(self):
        result=Report.objects.aggregate(total=Sum('loan_repayments'))
        return result['total']
    
    @cached_property
    def unrealized_interest(self):
        result=Report.objects.aggregate(total=Sum('unrealized_interest_income'))
        return result['total']
    
    @cached_property
    def debts(self):
        result=Report.objects.aggregate(total=Sum('bad_debts'))
        return result['total']
    
    @cached_property
    def realized_interest(self):
        result=Report.objects.aggregate(total=Sum('realized_interest_income'))
        return result['total']
    
    @cached_property
    def office(self):
        result=Report.objects.aggregate(total=Sum('office_expenses'))
        return result['total']
    
    @cached_property
    def salary(self):
        result=Report.objects.aggregate(total=Sum('salary_expenses'))
        return result['total']
    
    @cached_property
    def total_income(self):
        result=Report.objects.aggregate(total=Sum('income'))
        return result['total']


    