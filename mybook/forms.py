import json
from django import forms


class LoginForm(forms.Form):
    ent_email = forms.EmailField(label='Email')
    ent_pass = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):

        cleaned_data = super(LoginForm, self).clean()
        if not self.errors:
            self.email = cleaned_data['ent_email']
            self.password = cleaned_data['ent_pass']

        return cleaned_data

    def get_user(self):
        return {'email': self.email, 'password': self.password}
