from django.contrib.auth.models import User
from django.contrib import admin
from .models import Transaction,Report

admin.site.register(Transaction)
admin.site.register(Report)


