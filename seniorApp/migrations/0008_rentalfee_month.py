# Generated by Django 5.0.4 on 2024-04-17 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seniorApp', '0007_pettycash_petty_cash_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalfee',
            name='month',
            field=models.IntegerField(default='01', null=True),
        ),
    ]
