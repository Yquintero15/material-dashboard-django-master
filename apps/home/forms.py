# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.models import User
from apps.home.models import Profile
from django.core.validators import validate_email, RegexValidator


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(validators=[validate_email], widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField( max_length = 50,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField( max_length = 50,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['email','first_name','last_name']

class UpdateProfileForm(forms.ModelForm):
	address = forms.CharField( max_length = 100,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
	city = forms.CharField( max_length = 50,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
	country = forms.CharField( max_length = 100,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
	zip_code = forms.CharField( max_length = 5,validators=[RegexValidator('^[0-9]{5}$', ('Invalid postal code, formats 12345'))],
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
	bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

	class Meta:
		model = Profile
		fields = ['address','city', 'country','zip_code','bio']



