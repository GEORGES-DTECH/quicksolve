# Generated by Django 3.1.3 on 2021-01-30 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_remove_transaction_installment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='installment_description',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]
