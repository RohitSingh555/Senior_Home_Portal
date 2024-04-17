# In your app's forms.py file

from django import forms
from .models import Residents
from .models import RentalFee, PettyCash

class ResidentForm(forms.ModelForm):
    class Meta:
        model = Residents
        fields = '__all__' 
        
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
        fields = ['amount', 'date', 'month']
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class PettyCashForm(forms.ModelForm):
    class Meta:
        model = PettyCash
        fields = ['amount', 'petty_cash_type', 'date']
        
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))