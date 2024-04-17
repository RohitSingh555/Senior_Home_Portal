from django.db import models

class Residents(models.Model):
    resident_id = models.AutoField(primary_key=True)
    resident_first_name = models.CharField(max_length=100,blank=True, null=True)
    resident_last_name = models.CharField(max_length=100,blank=True, null=True)
    contact_name = models.CharField(max_length=20,blank=True, null=True)
    relation1 = models.CharField(max_length=100,blank=True, null=True)
    contact_name2 = models.CharField(max_length=20,blank=True, null=True)
    relation2 = models.CharField(max_length=100,blank=True, null=True)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100,blank=True, null=True)
    province = models.CharField(max_length=100,blank=True, null=True)
    postal_code = models.CharField(max_length=20,blank=True, null=True)
    phone_number = models.CharField(max_length=20,blank=True, null=True)
    work_number = models.CharField(max_length=20,blank=True, null=True)
    cell_number = models.CharField(max_length=20,blank=True, null=True)
    fax_number = models.CharField(max_length=20,blank=True, null=True)
    email_address = models.EmailField()
    address_contact2 = models.CharField(max_length=255)
    city_contact2 = models.CharField(max_length=100,blank=True, null=True)
    province_contact2 = models.CharField(max_length=100,blank=True, null=True)
    postal_code_contact2 = models.CharField(max_length=20,blank=True, null=True)
    phone_number_contact2 = models.CharField(max_length=20,blank=True, null=True)
    work_number_contact2 = models.CharField(max_length=20,blank=True, null=True)
    cell_number_contact2 = models.CharField(max_length=20,blank=True, null=True)
    fax_number_contact2 = models.CharField(max_length=20,blank=True, null=True)
    email_address_contact2 = models.EmailField()
    notes = models.TextField()
    room_number = models.CharField(max_length=50,blank=True, null=True)
    ohip = models.CharField(max_length=20,blank=True, null=True)
    date_of_birth = models.DateTimeField(default='1990-01-01 00:00:00', null=True)
    dnr = models.BooleanField(default=False)
    allergies = models.BooleanField(default=False)
    allergies_info = models.TextField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    weight_last = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    blood_pressure_last = models.CharField(max_length=20,blank=True, null=True)
    admission_date = models.DateTimeField(default='1990-01-01 00:00:00', null=True)

    def __str__(self):
        return f"{self.resident_first_name} {self.resident_last_name}"


class RentalFee(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    resident = models.ForeignKey(Residents, on_delete=models.CASCADE)
    month=models.IntegerField(null=True, default="01")
    date = models.DateField()

class PettyCash(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    resident = models.ForeignKey(Residents, on_delete=models.CASCADE)
    petty_cash_type = models.ForeignKey('PettyCashType', on_delete=models.CASCADE, default=1)  # Set default value here
    date = models.DateField()

class PettyCashType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type