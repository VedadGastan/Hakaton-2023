from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from phonenumber_field.formfields import PhoneNumberField
from .models import *


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email' ,'password1', 'password2')


class RegisterProfileForm(ModelForm):
    profile_type = forms.ChoiceField(choices = (("Consultant", "Consultant"), ("Non-Consultant", "Non-Consultant")))
    phone_number = PhoneNumberField()
    address = forms.CharField(max_length=200)

    class Meta:
        model = Profile
        fields = ('profile_type', 'phone_number' , 'address',)
