from django import forms
from .models import User

from .models import Order
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'items']
