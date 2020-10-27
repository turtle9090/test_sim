from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SimForm(forms.ModelForm):
    class Meta:
        model = VSIMData
        fields = '__all__'
        widgets = {
            'operator': forms.Select(attrs={'class': 'form-control'}),
            'sim_status': forms.Select(attrs={'class': 'form-control'}),
            #'package_name': forms.Select(attrs={'class': 'form-control'}),
            'vsim_iccid': forms.TextInput(attrs={'class': 'form-control'}),
            'vsim_imsi': forms.TextInput(attrs={'class': 'form-control'}),
            #'country_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country_or_region': forms.TextInput(attrs={'class': 'form-control'}),
            #'gb_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            #'cost_per_gb': forms.NumberInput(attrs={'class': 'form-control'}),

        }


class CarrierForm(forms.ModelForm):
    class Meta:
        model = Carrier
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }


#class CreateUserForm(UserCreationForm):
    #class Meta:
       # model = User
       # fields = ['username', 'email', 'password1', 'password2']

class CsvModelForm(forms.ModelForm):
    class Meta:
        model = Csv
        exclude = ('activated','uploaded')
        fields = '__all__'

