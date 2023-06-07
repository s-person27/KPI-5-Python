from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User , ShippingAddress




class LoginForm(forms.Form):
    login = forms.CharField(label='Login:', max_length=25)
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    # birthday = forms.DateField()
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ["username", "email", "birth_date"]
        # "password1", "password2"



class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'birth_date', 'sex')


class ShippingAddressForm(forms.ModelForm):

    class Meta :
        model = ShippingAddress
        fields = ('city','address','phone')