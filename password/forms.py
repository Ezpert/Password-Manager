from django import forms
import string
import random

class PasswordForm(forms.Form):
    password = forms.CharField(max_length=50, required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
        cleaned_data['password'] = password
        return cleaned_data
