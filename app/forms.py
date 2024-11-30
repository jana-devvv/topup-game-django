from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Package

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your password'}))

class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PackageForm(forms.Form):
    player_id = forms.IntegerField(
        label='Your ID',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    server_id = forms.IntegerField(
        label='Your server ID',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    packages = forms.ModelChoiceField(
        queryset=Package.objects.none(),
        widget=forms.RadioSelect,
        label='Select a Package'
    )

class PaymentForm(forms.Form):
    METHOD_CHOICES = [
        ('gopay', 'GoPay'),
        ('dana', 'Dana'),
        ('ovo', 'OVO'),
        ('shopeepay', 'ShopeePay'),
    ]

    payment = forms.ChoiceField(
        choices=METHOD_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Choose Payment Method'
    )