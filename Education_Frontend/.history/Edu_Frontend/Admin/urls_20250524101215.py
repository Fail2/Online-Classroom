from django import forms

class AdminLoginForm(forms.Form):
    username = forms.CharField
    password = forms.CharField(widget=forms.PasswordInput)

class AdminRegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
