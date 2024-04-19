# Generated by Django 5.0.4 on 2024-04-19 07:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PettyCashType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Residents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resident_first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('resident_last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_name', models.CharField(blank=True, max_length=20, null=True)),
                ('relation1', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_name2', models.CharField(blank=True, max_length=20, null=True)),
                ('relation2', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('work_number', models.CharField(blank=True, max_length=20, null=True)),
                ('cell_number', models.CharField(blank=True, max_length=20, null=True)),
                ('email_address', models.EmailField(max_length=254)),
                ('phone_number_contact2', models.CharField(blank=True, max_length=20, null=True)),
                ('work_number_contact2', models.CharField(blank=True, max_length=20, null=True)),
                ('cell_number_contact2', models.CharField(blank=True, max_length=20, null=True)),
                ('email_address_contact2', models.EmailField(max_length=254)),
                ('notes', models.TextField()),
                ('room_number', models.CharField(blank=True, max_length=50, null=True)),
                ('ohip', models.CharField(blank=True, max_length=20, null=True)),
                ('date_of_birth', models.DateTimeField(default='1990-01-01 00:00:00', null=True)),
                ('dnr', models.BooleanField(default=False)),
                ('admission_date', models.DateTimeField(default='1990-01-01 00:00:00', null=True)),
                ('discharge_date', models.DateTimeField(default='', null=True)),
                ('reason_for_discharge', models.CharField(choices=[('MOVED', 'Moved to another home'), ('PASSED_LCHAIM', "Passed away at L'chaim"), ('PASSED_HOSPITAL', 'Passed away in the hospital')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='RentalFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paid', models.BooleanField(default=True)),
                ('month', models.IntegerField(default='01', null=True)),
                ('date', models.DateField()),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seniorApp.residents')),
            ],
        ),
        migrations.CreateModel(
            name='PettyCash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('withdrawl', models.DecimalField(decimal_places=2, max_digits=10)),
                ('deposit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('petty_cash_type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='seniorApp.pettycashtype')),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seniorApp.residents')),
            ],
        ),
    ]
