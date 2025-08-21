from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    

    class Meta:
        model =User
        fields = ("username","password1","password2","email")


class Userpassword(forms.Form):
    # femail = forms.EmailField(label="이메일")     
    # fields = ("femail")
    femail = forms.EmailField(label='이메일')


class UserPasswordChangeForm(forms.Form):

        old_pwd = forms.PasswordInput
        new_pwd = forms.PasswordInput
        new_pwd_confirm = forms.PasswordInput
   