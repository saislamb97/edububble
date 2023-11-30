from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, PaymentApplication

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'text-black border p-2 mt-4 mb-4 rounded w-full', 'placeholder': 'Enter your email.'}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'text-black border p-2 mt-4 mb-4 rounded w-full', 'placeholder': 'Enter your password.'}),
    )
    show_password = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'ml-2'}),
        label="Show Password",
    )

    class Meta:
        model = User
        fields = ['username', 'password']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'fullname']

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'border p-2 mt-4 mb-4 rounded w-full'}),
            'username': forms.TextInput(attrs={'class': 'border p-2 mt-4 mb-4 rounded w-full'}),
            'fullname': forms.TextInput(attrs={'class': 'border p-2 mt-4 mb-4 rounded w-full'}),
        }
        labels = {
            'email': 'Email',
            'username': 'Username',
            'fullname': 'Full Name',
        }

class PaymentApplicationForm(forms.ModelForm):
    class Meta:
        model = PaymentApplication
        fields = ['paying_amount', 'payslip']

        widgets = {
            'paying_amount': forms.NumberInput(attrs={'class': 'border p-2 m-4 rounded w-full'}),
            'payslip': forms.FileInput(attrs={'class': 'p-2 m-4 w-full', 'accept': 'image/png, image/jpeg, .pdf'}),
        }
        labels = {
            'paying_amount': 'Payment Amount',
            'payslip': 'Payment Receipt',
        }
