# Generated by Django 5.0.4 on 2024-04-17 06:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seniorApp', '0005_alter_residents_admission_date'),
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
            name='PettyCash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seniorApp.residents')),
            ],
        ),
        migrations.CreateModel(
            name='RentalFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seniorApp.residents')),
            ],
        ),
    ]
