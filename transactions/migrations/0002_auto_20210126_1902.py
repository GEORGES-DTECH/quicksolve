# Generated by Django 3.1.3 on 2021-01-26 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='interest_charged',
            field=models.IntegerField(default=0),
        ),
    ]