from django import forms
import string
import random
from .models import Passwords


class PasswordForm(forms.Form):
    password = forms.CharField(max_length=50, required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
        cleaned_data['password'] = password
        return cleaned_data


class EditEntryForm(forms.Form):
    url = forms.CharField(max_length=200)
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
