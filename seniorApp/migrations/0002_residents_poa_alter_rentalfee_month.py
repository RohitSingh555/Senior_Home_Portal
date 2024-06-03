# Generated by Django 5.0.4 on 2024-05-30 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seniorApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='residents',
            name='poa',
            field=models.CharField(choices=[('POA Care', 'POA Care'), ('POA Financial', 'POA Financial'), ('POA Financial & Care', 'POA Financial & Care')], default='POA Care', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='rentalfee',
            name='month',
            field=models.CharField(choices=[('Jan', 'January'), ('Feb', 'February'), ('Mar', 'March'), ('Apr', 'April'), ('May', 'May'), ('Jun', 'June'), ('Jul', 'July'), ('Aug', 'August'), ('Sep', 'September'), ('Oct', 'October'), ('Nov', 'November'), ('Dec', 'December'), ('LMD', 'Last Month Deposit')], default='Jan', max_length=10, null=True),
        ),
    ]
