from django.db import models

class Residents(models.Model):
    REASON_CHOICES = [
        ('MOVED', 'Moved to another home'),
        ('PASSED_LCHAIM', 'Passed away at L\'chaim'),
        ('PASSED_HOSPITAL', 'Passed away in the hospital'),
    ]
    resident_first_name = models.CharField(max_length=100,blank=True, null=True)
    resident_last_name = models.CharField(max_length=100,blank=True, null=True)
    contact_name = models.CharField(max_length=20,blank=True, null=True)
    relation1 = models.CharField(max_length=100,blank=True, null=True)
    contact_name2 = models.CharField(max_length=20,blank=True, null=True)
    relation2 = models.CharField(max_length=100,blank=True, null=True)
    phone_number = models.CharField(max_length=20,blank=True, null=True)
    work_number = models.CharField(max_length=20,blank=True, null=True)
    cell_number = models.CharField(max_length=20,blank=True, null=True)
    email_address = models.EmailField()
    phone_number_contact2 = models.CharField(max_length=20,blank=True, null=True)
    work_number_contact2 = models.CharField(max_length=20,blank=True, null=True)
    cell_number_contact2 = models.CharField(max_length=20,blank=True, null=True)
    email_address_contact2 = models.EmailField()
    notes = models.TextField()
    room_number = models.CharField(max_length=50,blank=True, null=True)
    ohip = models.CharField(max_length=20,blank=True, null=True)
    date_of_birth = models.DateTimeField(default='1990-01-01 00:00:00', null=True)
    dnr = models.BooleanField(default=False)
    admission_date = models.DateTimeField(default='1990-01-01 00:00:00', null=True)
    discharge_date = models.DateTimeField(default='', null=True)
    reason_for_discharge = models.CharField(max_length=20, choices=REASON_CHOICES)

    def __str__(self):
        return f"{self.resident_first_name} {self.resident_last_name}"


class RentalFee(models.Model):
    MONTH_CHOICES = [
    ('Jan', 'January'),
    ('Feb', 'February'),
    ('Mar', 'March'),
    ('Apr', 'April'),
    ('May', 'May'),
    ('Jun', 'June'),
    ('Jul', 'July'),
    ('Aug', 'August'),
    ('Sep', 'September'),
    ('Oct', 'October'),
    ('Nov', 'November'),
    ('Dec', 'December'),
]
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    resident = models.ForeignKey(Residents, on_delete=models.CASCADE)
    paid = models.BooleanField(default=True)
    month = models.CharField(max_length=10, choices=MONTH_CHOICES, null=True, default='Jan')
    date = models.DateField()

class PettyCash(models.Model):
    ACTION_TYPES = [
        ('Withdrawl', 'Withdrawl'),
        ('Deposit', 'Deposit'),
    ]
    type = models.CharField(max_length=20, choices=ACTION_TYPES ,default="")
    withdrawl = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True, default=0)
    deposit = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True,default=0)
    resident = models.ForeignKey(Residents, on_delete=models.CASCADE)
    petty_cash_type = models.ForeignKey('PettyCashType', on_delete=models.CASCADE, default=1)  # Set default value here
    date = models.DateField()

class PettyCashType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type