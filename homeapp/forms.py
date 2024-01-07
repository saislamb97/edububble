from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import TextbookStatus, User

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': 'text-black border p-2 mb-4 rounded w-full'}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'text-black border p-2 mb-4 rounded w-full'}),
    )

    class Meta:
        model = User
        fields = ['username', 'password']

class TextbookStatusForm(forms.ModelForm):
    class Meta:
        model = TextbookStatus
        fields = ['collected', 'returned']
        widgets = {
            'collected': forms.CheckboxInput(attrs={'class': 'ml-2 checkbox'}),
            'returned': forms.CheckboxInput(attrs={'class': 'ml-2 checkbox'}),
        }