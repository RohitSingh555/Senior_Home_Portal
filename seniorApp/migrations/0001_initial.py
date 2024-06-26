# Generated by Django 4.2.13 on 2024-06-25 07:57

from django.db import migrations, models
import django.db.models.deletion


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
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('work_number', models.CharField(blank=True, max_length=20, null=True)),
                ('cell_number', models.CharField(blank=True, max_length=20, null=True)),
                ('email_address', models.EmailField(max_length=254)),
                ('POA_contact1', models.CharField(choices=[('POA Care', 'POA Care'), ('POA Financial', 'POA Financial'), ('POA Financial & Care', 'POA Financial & Care'), ('None', 'N/A')], default='POA Care', max_length=100, null=True)),
                ('contact_name2', models.CharField(blank=True, max_length=20, null=True)),
                ('relation2', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number_contact2', models.CharField(blank=True, max_length=20, null=True)),
                ('work_number_contact2', models.CharField(blank=True, max_length=20, null=True)),
                ('cell_number_contact2', models.CharField(blank=True, max_length=20, null=True)),
                ('POA_contact2', models.CharField(choices=[('POA Care', 'POA Care'), ('POA Financial', 'POA Financial'), ('POA Financial & Care', 'POA Financial & Care'), ('None', 'N/A')], default='POA Care', max_length=100, null=True)),
                ('email_address_contact2', models.EmailField(max_length=254)),
                ('notes', models.TextField()),
                ('room_number', models.CharField(blank=True, max_length=50, null=True)),
                ('ohip', models.CharField(blank=True, max_length=20, null=True)),
                ('date_of_birth', models.DateTimeField(default='1990-01-01 00:00:00', null=True)),
                ('DNR', models.BooleanField(default=False)),
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
                ('month', models.CharField(choices=[('Jan', 'January'), ('Feb', 'February'), ('Mar', 'March'), ('Apr', 'April'), ('May', 'May'), ('Jun', 'June'), ('Jul', 'July'), ('Aug', 'August'), ('Sep', 'September'), ('Oct', 'October'), ('Nov', 'November'), ('Dec', 'December'), ('LMD', 'Last Month Deposit')], default='Jan', max_length=10, null=True)),
                ('date', models.DateField()),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seniorApp.residents')),
            ],
        ),
        migrations.CreateModel(
            name='PettyCash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Withdrawl', 'Withdrawl'), ('Deposit', 'Deposit')], default='', max_length=20)),
                ('withdrawl', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('deposit', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('date', models.DateField()),
                ('petty_cash_type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='seniorApp.pettycashtype')),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seniorApp.residents')),
            ],
        ),
        migrations.CreateModel(
            name='EmailLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resident_name', models.CharField(blank=True, max_length=100, null=True)),
                ('emailed_report_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email_body', models.TextField()),
                ('date', models.DateTimeField()),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seniorApp.residents')),
            ],
        ),
    ]
