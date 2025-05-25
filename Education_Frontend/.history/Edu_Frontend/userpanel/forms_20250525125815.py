from django import forms

ROLE_CHOICES = [
    ('', 'Select Role'),
    ('STUDENT', 'Student'),
    ('TEACHER', 'Teacher'),
]

class UserRegisterForm(forms.Form):
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    

class UserLoginForm(forms.Form):
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
   
