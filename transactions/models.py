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
('2month','2month'),
('3month','3month'),



)

class Transaction(models.Model):
    clients_loan_repayment = models.IntegerField(default=0)
    lending_date=models.DateTimeField(default=timezone.now)
    clients_name=models.CharField(max_length=200)
    clients_id=models.CharField(max_length=200)
    clients_phone=models.CharField(max_length=20)
    loan_amount=models.IntegerField(default=0)
    interest_charged = models.DecimalField(default=0.0,max_digits=19,decimal_places=3)
    repayment_period = models.CharField(choices=period,max_length=100)
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
    def total_repayed_amount(self):
        result = Transaction.objects.aggregate(total=Sum('clients_loan_repayment'))
        return result['total']
    
    
    @cached_property
    def total_clients(self):
        result = Transaction.objects.aggregate(total=Count('clients_name'))
        return result['total']
   