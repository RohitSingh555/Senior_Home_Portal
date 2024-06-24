# In your app's forms.py file

from django import forms
from .models import Residents
from .models import RentalFee, PettyCash

class ResidentForm(forms.ModelForm):
    class Meta:
        model = Residents
        fields = '__all__'
    
    discharge_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    admission_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resident_first_name'].required = True
        self.fields['date_of_birth'].required = True  
        for field_name in self.fields:
            if field_name not in ['resident_first_name', 'date_of_birth']:
                self.fields[field_name].required = False


class RentalFeeForm(forms.ModelForm):
    class Meta:
        model = RentalFee
        fields = '__all__' 
        fields = ['amount','paid', 'date', 'month']
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

# class PettyCashForm(forms.ModelForm):
#     class Meta:
#         model = PettyCash
#         fields = ['type', 'deposit', 'withdrawal', 'petty_cash_type', 'date']
#     deposit = forms.DecimalField(required=False)
#     withdrawal = forms.DecimalField(required=False)
#     # type = forms.CharField(required=False)
#     date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


class PettyCashForm(forms.ModelForm):
    class Meta:
        model = PettyCash
        fields = ['type', 'deposit', 'withdrawl', 'petty_cash_type', 'date']
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    