# Generated by Django 3.1.3 on 2021-01-27 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0008_auto_20210127_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='interest_charged',
            field=models.FloatField(default=0.0),
        ),
    ]