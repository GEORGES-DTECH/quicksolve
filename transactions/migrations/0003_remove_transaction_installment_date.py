# Generated by Django 3.1.3 on 2021-01-30 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20210130_1319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='installment_date',
        ),
    ]
